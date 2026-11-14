// Top-bar buttons that hide the left menu and the right page overview.
// The choice is kept per browser in localStorage.
(function () {
  const buttons = [
    { key: "nav", label: "Hide or show the menu",
      icon: '<path d="M3 4h18v16H3zm2 2v12h4V6zm6 0v12h8V6z"/>' },
    { key: "toc", label: "Hide or show the page overview",
      icon: '<path d="M3 4h18v16H3zm2 2v12h8V6zm10 0v12h4V6z"/>' },
  ];

  const read = (key) => {
    try { return localStorage.getItem("aw-hide-" + key) === "1"; } catch { return false; }
  };
  const write = (key, hidden) => {
    try { localStorage.setItem("aw-hide-" + key, hidden ? "1" : "0"); } catch {}
  };

  function setup() {
    for (const b of buttons) document.body.classList.toggle("aw-hide-" + b.key, read(b.key));
    const header = document.querySelector(".md-header__inner");
    if (!header || header.querySelector(".aw-layout-toggle")) return;
    const anchor = header.querySelector(".md-search") || header.querySelector(".md-header__source");
    for (const b of buttons) {
      const btn = document.createElement("button");
      btn.className = "md-header__button md-icon aw-layout-toggle";
      btn.title = b.label;
      btn.setAttribute("aria-label", b.label);
      btn.setAttribute("aria-pressed", String(read(b.key)));
      btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true">' + b.icon + "</svg>";
      btn.addEventListener("click", () => {
        const hidden = !document.body.classList.contains("aw-hide-" + b.key);
        document.body.classList.toggle("aw-hide-" + b.key, hidden);
        btn.setAttribute("aria-pressed", String(hidden));
        write(b.key, hidden);
      });
      header.insertBefore(btn, anchor);
    }
  }

  if (typeof document$ !== "undefined") document$.subscribe(setup);
  else document.addEventListener("DOMContentLoaded", setup);
})();
