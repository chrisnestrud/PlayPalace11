export function createMenuView({
  store,
  listEl,
  onActivate,
  onSelectionSound,
  onActivateSound,
  onBoundaryRepeat,
}) {
  let renderVersion = 0;
  let searchBuffer = "";
  let lastTypeTime = 0;
  const typeTimeoutSeconds = 0.15;

  function currentOptionId(index) {
    return `menu-option-${renderVersion}-${index}`;
  }

  function setSelection(next) {
    const count = store.state.currentMenu.items.length;
    if (!count) {
      store.setMenu({ selection: 0 });
      return;
    }
    const bounded = Math.max(0, Math.min(count - 1, next));
    if (bounded === store.state.currentMenu.selection) {
      return;
    }
    store.setMenu({ selection: bounded });
    if (onSelectionSound) {
      onSelectionSound();
    }
  }

  function moveSelection(delta) {
    const menu = store.state.currentMenu;
    const count = menu.items.length;
    if (!count) {
      return;
    }
    const current = menu.selection;
    const bounded = Math.max(0, Math.min(count - 1, current + delta));
    if (bounded === current) {
      if (onSelectionSound) {
        onSelectionSound();
      }
      const currentItem = menu.items[current];
      if (currentItem && onBoundaryRepeat) {
        onBoundaryRepeat(currentItem.text);
      }
      return;
    }
    setSelection(bounded);
  }

  function handleTypeNavigation(char) {
    const menu = store.state.currentMenu;
    const count = menu.items.length;
    if (!count || !char) {
      return;
    }

    const now = performance.now() / 1000;
    if (now - lastTypeTime > typeTimeoutSeconds) {
      searchBuffer = "";
    }
    searchBuffer += char.toLowerCase();
    lastTypeTime = now;

    const current = menu.selection;
    const currentItem = menu.items[current];
    const currentText = String(currentItem?.text || "").toLowerCase();

    // Match desktop behavior: if extended buffer already matches current item, stay on it.
    if (searchBuffer.length > 1 && currentText.startsWith(searchBuffer)) {
      return;
    }

    const start = current >= 0 ? current : 0;
    for (let offset = 1; offset <= count; offset += 1) {
      const i = (start + offset) % count;
      const text = String(menu.items[i]?.text || "").toLowerCase();
      if (text.startsWith(searchBuffer)) {
        setSelection(i);
        return;
      }
    }
  }

  function activateSelection() {
    const menu = store.state.currentMenu;
    if (!menu.items.length) {
      return;
    }
    const item = menu.items[menu.selection];
    if (!item) {
      return;
    }
    if (onActivateSound) {
      onActivateSound();
    }
    onActivate(item, menu.selection);
  }

  function render() {
    const menu = store.state.currentMenu;
    renderVersion += 1;
    searchBuffer = "";
    lastTypeTime = 0;
    listEl.innerHTML = "";

    menu.items.forEach((item, index) => {
      const li = document.createElement("li");
      li.id = currentOptionId(index);
      li.className = "menu-item";
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", index === menu.selection ? "true" : "false");
      if (index === menu.selection) {
        li.classList.add("active");
      }
      li.dataset.index = String(index);
      li.textContent = item.text;
      li.addEventListener("click", () => {
        setSelection(index);
      });
      li.addEventListener("dblclick", () => {
        setSelection(index);
        activateSelection();
      });
      listEl.appendChild(li);
    });
    if (menu.items.length > 0) {
      listEl.setAttribute(
        "aria-activedescendant",
        currentOptionId(Math.max(0, Math.min(menu.selection, menu.items.length - 1)))
      );
    } else {
      listEl.removeAttribute("aria-activedescendant");
    }

  }

  listEl.addEventListener("focus", () => {
    render();
  });

  store.subscribe(render);
  render();

  return {
    setSelection,
    moveSelection,
    handleTypeNavigation,
    activateSelection,
    getElement() {
      return listEl;
    },
    getCurrentItemText() {
      const menu = store.state.currentMenu;
      if (!menu.items.length) {
        return "";
      }
      const currentItem = menu.items[Math.max(0, Math.min(menu.selection, menu.items.length - 1))];
      return currentItem?.text || "";
    },
  };
}
