window.addEventListener("DOMContentLoaded", () => {
  const $root = document.getElementById("root");
  const lsKey = "powerkanji_selected_kanji";
  const attrIdKey = "data-ext-id";
  const classNameSelected = "kanji-cell_selected";

  let dataSelected;

  try {
    dataSelected = (localStorage.getItem(lsKey) || []).split(";");
  } catch (err) {
    dataSelected = [];
  }

  if (dataSelected.length > 0) {
    const initialSelector = dataSelected
      .map((val) => `[data-ext-id="${val}"]`)
      .join(",");

    document.querySelectorAll(initialSelector).forEach(($el) => {
      $el.classList.add(classNameSelected);
    });
  }

  $root.addEventListener("click", (event) => {
    const target = event.target;

    if (target && target.classList.contains("kanji-cell")) {
      const { extId } = target.dataset;

      if (dataSelected.includes(extId)) {
        target.classList.remove(classNameSelected);
        dataSelected = dataSelected.filter((x) => x !== extId);
      } else {
        target.classList.add(classNameSelected);
        dataSelected.push(extId);
      }

      localStorage.setItem(lsKey, dataSelected.join(";"));
    }
  });
});
