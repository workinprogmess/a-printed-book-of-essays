(async () => {
  await document.fonts.ready;
  const src = document.getElementById("src");
  const out = document.getElementById("out");
  const previewer = new Paged.Previewer();
  const styles = (document.body.dataset.styles || "../../tool/styles.css").split(",");
  await previewer.preview(src.innerHTML, styles, out);
  // lines marked data-fit="<mm>" get a font-size that makes them exactly that wide
  for (const el of out.querySelectorAll("[data-fit]")) {
    const target = parseFloat(el.dataset.fit) * 3.7795;
    el.style.fontSize = "100px";
    const w = el.getBoundingClientRect().width;
    if (w > 0) el.style.fontSize = `${(100 * target) / w}px`;
  }
  document.body.dataset.rendered = "true";
})();
