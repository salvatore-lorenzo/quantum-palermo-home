// Behaviour of the site. Every page also works without JavaScript: these are enhancements.

const root = document.documentElement;

// Light / dark theme toggle (the choice is remembered; by default the system theme is used)
function currentTheme() {
  return root.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
}
document.querySelector(".theme-toggle")?.addEventListener("click", () => {
  const next = currentTheme() === "dark" ? "light" : "dark";
  root.dataset.theme = next;
  try { localStorage.setItem("theme", next); } catch (e) { /* private mode: not remembered */ }
});

// Menu on small screens
const menuButton = document.querySelector(".menu-toggle");
const nav = document.getElementById("main-nav");
if (menuButton && nav) {
  const setOpen = (open) => {
    menuButton.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("open", open);
  };
  menuButton.addEventListener("click", () => setOpen(menuButton.getAttribute("aria-expanded") !== "true"));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("open")) { setOpen(false); menuButton.focus(); }
  });
}

// "Back" links: when we arrived from that same list (e.g. filtered publications), go back in
// history so the filters and the scroll position are kept; otherwise follow the link
document.querySelectorAll("a[data-back]").forEach((link) => {
  link.addEventListener("click", (e) => {
    let from;
    try { from = new URL(document.referrer); } catch (err) { return; }
    if (from.origin === location.origin && from.pathname === new URL(link.href).pathname && history.length > 1) {
      e.preventDefault();
      history.back();
    }
  });
});

// Copy buttons (e.g. BibTeX)
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const source = document.querySelector(button.dataset.copy);
    const label = button.querySelector("span");
    try {
      await navigator.clipboard.writeText(source.textContent);
      if (label) {
        const text = label.textContent;
        label.textContent = "Copied!";
        setTimeout(() => { label.textContent = text; }, 1800);
      }
    } catch (e) {
      // No clipboard access: select the text so it can be copied by hand
      const range = document.createRange();
      range.selectNodeContents(source);
      getSelection().removeAllRanges();
      getSelection().addRange(range);
    }
  });
});

// Publication filters. The state lives in the URL (?q=…&year=…&research=…&member=…&type=…),
// so filtered lists can be linked to, and "Back" returns to the same selection.
const form = document.getElementById("pub-filters");
if (form) {
  const items = [...document.querySelectorAll(".pub-list .pub")];
  const groups = [...document.querySelectorAll(".pub-list [data-group]")];
  const count = form.querySelector("[data-count]");
  const empty = document.querySelector(".pub-list .empty");
  const names = ["q", "year", "research", "member", "type"];

  const params = new URLSearchParams(location.search);
  for (const name of names) {
    if (params.has(name)) form.elements[name].value = params.get(name);
  }

  const apply = (updateUrl) => {
    const f = Object.fromEntries(names.map((n) => [n, form.elements[n].value.trim()]));
    const words = f.q.toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const item of items) {
      const d = item.dataset;
      const match = (!f.year || d.year === f.year)
        && (!f.type || d.type === f.type)
        && (!f.research || d.research.split(" ").includes(f.research))
        && (!f.member || d.members.split(" ").includes(f.member))
        && words.every((w) => d.text.includes(w));
      item.hidden = !match;
      if (match) shown++;
    }
    for (const group of groups) group.hidden = !group.querySelector(".pub:not([hidden])");
    count.textContent = shown;
    empty.hidden = shown > 0;
    for (const name of names) form.elements[name].classList.toggle("is-set", Boolean(f[name]));
    if (updateUrl) {
      const query = new URLSearchParams(names.filter((n) => f[n]).map((n) => [n, f[n]])).toString();
      history.replaceState(null, "", query ? `?${query}` : location.pathname);
    }
  };

  let timer;
  form.addEventListener("input", (e) => {
    clearTimeout(timer);
    timer = setTimeout(() => apply(true), e.target.name === "q" ? 150 : 0);
  });
  form.addEventListener("submit", (e) => { e.preventDefault(); apply(true); });
  form.addEventListener("reset", () => setTimeout(() => apply(true)));
  apply(false);
}

// LaTeX in paper titles and abstracts ($…$), on the pages that load KaTeX
window.addEventListener("load", () => {
  if (!window.renderMathInElement) return;
  window.renderMathInElement(document.getElementById("main"), {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
    ],
    ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
    throwOnError: false,
  });
});
