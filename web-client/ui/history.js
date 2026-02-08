export function createHistoryView({ store, historyEl, bufferSelectEl, a11y }) {
  function render() {
    const bufferName = store.state.historyBuffer;
    const lines = store.state.historyBuffers[bufferName] || [];
    historyEl.value = lines.join("\n");
    historyEl.scrollTop = historyEl.scrollHeight;
  }

  function addEntry(text, options = {}) {
    const {
      buffer = "misc",
      announce = true,
      assertive = false,
    } = options;

    store.addHistory(buffer, text);
    if (announce) {
      a11y.announce(text, { assertive });
    }
  }

  if (bufferSelectEl) {
    bufferSelectEl.addEventListener("change", () => {
      store.setHistoryBuffer(bufferSelectEl.value);
    });
  }

  store.subscribe(render);
  render();

  return { addEntry, render };
}
