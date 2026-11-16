(() => {
  const cases = [...document.querySelectorAll(".case")];
  const groups = [...document.querySelectorAll(".case-group")];
  const search = document.querySelector("#case-search");
  const group = document.querySelector("#case-group");
  const priority = document.querySelector("#case-priority");
  const reset = document.querySelector("#case-reset");
  const count = document.querySelector("#case-count");
  const empty = document.querySelector("#no-cases");
  const expand = document.querySelector("#case-expand");
  const searchableText = new Map(cases.map(item => [
    item, item.textContent.toLocaleLowerCase("ru").replace(/\s+/g, " ")
  ]));
  let visible = cases;
  let printState;

  const syncToggleLabel = () => {
    const allOpen = visible.every(item => item.open);
    expand.textContent = allOpen ? "Свернуть все" : "Раскрыть все";
  };

  const updateFilters = () => {
    const words = search.value.trim().toLocaleLowerCase("ru").split(/\s+/);
    visible = cases.filter(item => {
      const matches = (!group.value || item.dataset.group === group.value)
        && (!priority.value || item.dataset.priority === priority.value)
        && words.every(word => searchableText.get(item).includes(word));
      item.hidden = !matches;
      return matches;
    });
    groups.forEach(section => {
      section.hidden = !section.querySelector(".case:not([hidden])");
    });
    count.textContent = `Показано ${visible.length} из ${cases.length}`;
    empty.hidden = visible.length > 0;
    expand.hidden = visible.length === 0;
    syncToggleLabel();
  };

  const clearFilters = () => {
    search.value = "";
    group.value = "";
    priority.value = "";
    updateFilters();
  };

  const revealCase = () => {
    const id = location.hash.slice(1);
    if (!/^CHAT-\d{2}$/.test(id)) return;

    const target = document.getElementById(id);
    if (!target) return;
    if (target.hidden) clearFilters();
    target.open = true;
    target.scrollIntoView({ block: "start" });
  };

  search.addEventListener("input", updateFilters);
  group.addEventListener("change", updateFilters);
  priority.addEventListener("change", updateFilters);
  reset.addEventListener("click", () => {
    clearFilters();
    search.focus();
  });
  expand.addEventListener("click", () => {
    const open = visible.some(item => !item.open);
    visible.forEach(item => { item.open = open; });
    syncToggleLabel();
  });
  cases.forEach(item => {
    item.open = false;
    item.addEventListener("toggle", syncToggleLabel);
  });

  window.addEventListener("hashchange", revealCase);
  document.querySelector(".table-wrap").addEventListener("click", event => {
    const link = event.target.closest("a");
    if (link && link.hash === location.hash) revealCase();
  });
  window.addEventListener("beforeprint", () => {
    if (printState) return;
    printState = cases.map(item => item.open);
    cases.forEach(item => { item.open = true; });
  });
  window.addEventListener("afterprint", () => {
    if (!printState) return;
    cases.forEach((item, index) => { item.open = printState[index]; });
    printState = undefined;
  });
  document.querySelector(".filters").hidden = false;
  document.querySelector(".case-toolbar").hidden = false;
  updateFilters();
  revealCase();
})();
