// Page actions (docs/overrides/partials/actions.html) and the home page's "Copy docs for your AI".
(function () {
  async function copy(text) {
    try {
      await navigator.clipboard.writeText(text);
    } catch (e) {  // not a secure context (file://): the old way
      const t = document.createElement("textarea");
      t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove();
    }
  }
  function flash(button, text) {
    const label = button.querySelector("[data-ob-copy-label]") || button.closest("[data-ob-actions]")?.querySelector("[data-ob-copy-label]");
    if (!label) return;
    const old = label.dataset.old || label.textContent;
    label.dataset.old = old; label.textContent = text;
    button.classList.add("ob-done");
    setTimeout(() => { label.textContent = old; button.classList.remove("ob-done"); }, 1600);
  }
  function close() {
    document.querySelectorAll(".ob-actions__more.open").forEach(m => {
      m.classList.remove("open"); m.querySelector("[data-ob-menu]").setAttribute("aria-expanded", "false");
    });
  }
  function setup() {
    document.querySelectorAll("[data-ob-menu]").forEach(b => b.onclick = e => {
      e.stopPropagation();
      const m = b.parentElement, open = !m.classList.contains("open");
      close();
      if (open) { m.classList.add("open"); b.setAttribute("aria-expanded", "true"); }
    });
    const md = document.querySelector("[data-ob-md]");
    document.querySelectorAll("[data-ob-copy]").forEach(b => b.onclick = async () => {
      await copy(md ? md.value : document.title);
      flash(b, "Copied");
      close();
    });
    document.querySelectorAll("[data-ob-copy-all]").forEach(b => b.onclick = async () => {
      try {
        const r = await fetch(b.dataset.obCopyAll);
        await copy(await r.text());
        flash(b, "Copied all docs");
      } catch (e) {
        window.open(b.dataset.obCopyAll, "_blank");  // file:// can't fetch: show it instead
      }
      close();
    });
    document.querySelectorAll("[data-ob-open]").forEach(a => {
      const prompt = `Read ${location.origin + location.pathname} (AllSense docs) and help me with it.`;
      a.href = a.dataset.obOpen + encodeURIComponent(prompt);
    });
  }
  document.addEventListener("click", e => { if (!e.target.closest(".ob-actions__menu")) close(); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") close(); });
  if (window.document$) document$.subscribe(setup); else document.addEventListener("DOMContentLoaded", setup);
})();
