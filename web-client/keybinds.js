function keyFromEvent(event) {
  if (event.key === " ") {
    return "space";
  }
  if (event.key === "Escape") {
    return "escape";
  }
  if (event.key === "Backspace") {
    return "backspace";
  }
  if (event.key === "Enter") {
    return "enter";
  }
  if (event.key.startsWith("F") && /^F\d+$/.test(event.key)) {
    return event.key.toLowerCase();
  }

  const lower = event.key.toLowerCase();
  if (/^[a-z0-9]$/.test(lower)) {
    return lower;
  }
  if (["arrowup", "arrowdown", "arrowleft", "arrowright"].includes(lower)) {
    return lower.replace("arrow", "");
  }
  return null;
}

function isTypingTarget(element) {
  if (!element) {
    return false;
  }
  const tag = element.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || element.isContentEditable;
}

export function installKeybinds({ store, menuView, sendMenuSelection, sendEscape, sendKeybind, isModalOpen }) {
  document.addEventListener("keydown", (event) => {
    if (isModalOpen && isModalOpen()) {
      return;
    }

    const menu = store.state.currentMenu;
    const typing = isTypingTarget(document.activeElement);
    const menuFocused = document.activeElement === menuView.getElement();
    const activeElement = document.activeElement;

    if (
      event.key === "Backspace"
      && activeElement
      && (activeElement.tagName === "TEXTAREA" || activeElement.tagName === "INPUT")
      && activeElement.readOnly
    ) {
      // Avoid browser back navigation when focus is on readonly history.
      event.preventDefault();
      return;
    }

    if (menuFocused) {
      if (event.key === "ArrowUp") {
        event.preventDefault();
        menuView.moveSelection(-1);
        return;
      }
      if (event.key === "ArrowDown") {
        event.preventDefault();
        menuView.moveSelection(1);
        return;
      }
      if (event.key === "Home") {
        event.preventDefault();
        menuView.setSelection(0);
        return;
      }
      if (event.key === "End") {
        event.preventDefault();
        menuView.setSelection(Math.max(0, menu.items.length - 1));
        return;
      }
      if (event.key === "Enter" && !event.altKey && !event.ctrlKey && !event.shiftKey) {
        event.preventDefault();
        menuView.activateSelection();
        return;
      }

      const typedChar = event.key.length === 1 ? event.key.toLowerCase() : "";
      const isTypeNavChar = /^[a-z0-9 ]$/.test(typedChar);
      if (
        menu.multiletterEnabled
        && isTypeNavChar
        && !event.altKey
        && !event.ctrlKey
        && !event.metaKey
        && !event.shiftKey
      ) {
        event.preventDefault();
        menuView.handleTypeNavigation(typedChar);
        return;
      }
    }

    if (!menuFocused && !typing) {
      return;
    }

    if (event.key === "Escape" || (event.key === "Backspace" && menuFocused)) {
      if (event.key === "Backspace" && menu.menuId === "main_menu") {
        event.preventDefault();
        return;
      }
      event.preventDefault();
      if (menu.escapeBehavior === "escape_event") {
        sendEscape();
        return;
      }
      if (menu.escapeBehavior === "select_last_option") {
        const lastIndex = menu.items.length - 1;
        if (lastIndex >= 0) {
          menuView.setSelection(lastIndex);
          sendMenuSelection(lastIndex);
        }
        return;
      }
      // keybind behavior: send as "escape" (desktop behavior for Backspace outside main menu).
      const menuIndex = menu.items.length ? menu.selection + 1 : null;
      const currentItem = menu.items[menu.selection] || null;
      sendKeybind({
        key: "escape",
        control: event.ctrlKey,
        alt: event.altKey,
        shift: event.shiftKey,
        menu_id: menu.menuId,
        menu_index: menuIndex,
        menu_item_id: currentItem?.id ?? null,
      });
      return;
    }

    if ((typing || !menuFocused) && event.key !== "Escape") {
      return;
    }

    const key = keyFromEvent(event);
    if (!key) {
      return;
    }

    const menuIndex = menu.items.length ? menu.selection + 1 : null;
    const currentItem = menu.items[menu.selection] || null;

    const isFunctionLike = [
      "escape",
      "space",
      "backspace",
      "enter",
      "up",
      "down",
      "left",
      "right",
      "f1",
      "f2",
      "f3",
      "f4",
      "f5",
    ].includes(key);

    const shouldSend = isFunctionLike || !menu.multiletterEnabled || event.altKey || event.ctrlKey || event.shiftKey;
    if (!shouldSend) {
      return;
    }

    event.preventDefault();
    sendKeybind({
      key,
      control: event.ctrlKey,
      alt: event.altKey,
      shift: event.shiftKey,
      menu_id: menu.menuId,
      menu_index: menuIndex,
      menu_item_id: currentItem?.id ?? null,
    });
  });
}
