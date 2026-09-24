/* Tabs enhance readable stacked panels; without JavaScript every panel remains visible. */
function initEditorialTabs() {
document.querySelectorAll('[data-tabs]').forEach((root) => {
  const list = root.querySelector('[role="tablist"]');
  const tabs = [...root.querySelectorAll('[role="tab"]')];
  const panels = [...root.querySelectorAll('[role="tabpanel"]')];
  if (!list || tabs.length < 2 || tabs.length !== panels.length) return;

  const activate = (index, moveFocus = false) => {
    tabs.forEach((tab, position) => {
      const selected = position === index;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      panels[position].hidden = !selected;
    });
    if (moveFocus) tabs[index].focus();
  };

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activate(index));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) {
        event.preventDefault();
        tabs[next].focus();
      }
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        activate(index);
      }
    });
  });
  activate(0);
  list.hidden = false;
});
}
document.readyState === 'loading'
  ? document.addEventListener('DOMContentLoaded', initEditorialTabs)
  : initEditorialTabs();
