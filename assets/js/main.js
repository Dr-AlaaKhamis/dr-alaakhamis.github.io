/* Site behaviour: theme, mobile nav, back-to-top, publication filtering. */
(function () {
  "use strict";

  /* ---- Theme ---------------------------------------------------------- */
  var root = document.documentElement;

  function currentTheme() {
    var set = root.getAttribute("data-theme");
    if (set) return set;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    try { localStorage.setItem("theme", theme); } catch (e) { /* private mode */ }
    var btn = document.querySelector(".theme-toggle");
    if (btn) {
      btn.setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
      btn.setAttribute("aria-pressed", String(theme === "dark"));
    }
  }

  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    applyTheme(currentTheme());
    toggle.addEventListener("click", function () {
      applyTheme(currentTheme() === "dark" ? "light" : "dark");
    });
  }

  /* ---- Mobile navigation ---------------------------------------------- */
  var navBtn = document.querySelector(".nav-toggle");
  var nav = document.getElementById("primary-nav");
  if (navBtn && nav) {
    navBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      navBtn.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        nav.classList.remove("is-open");
        navBtn.setAttribute("aria-expanded", "false");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        navBtn.setAttribute("aria-expanded", "false");
        navBtn.focus();
      }
    });
  }

  /* ---- Back to top ----------------------------------------------------- */
  var toTop = document.querySelector(".to-top");
  if (toTop) {
    var onScroll = function () {
      toTop.classList.toggle("is-visible", window.scrollY > 600);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* ---- Filterable list (publications, teaching, news) ------------------ */
  var toolbar = document.querySelector("[data-filter-root]");
  if (!toolbar) return;

  var scopeSel = toolbar.getAttribute("data-filter-root");
  var scope = document.querySelector(scopeSel);
  if (!scope) return;

  var input = toolbar.querySelector("input[type='search']");
  var chips = Array.prototype.slice.call(toolbar.querySelectorAll(".chip"));
  var status = toolbar.querySelector(".filter-status");
  var groups = Array.prototype.slice.call(scope.querySelectorAll("[data-group]"));
  var items = Array.prototype.slice.call(scope.querySelectorAll("[data-item]"));

  items.forEach(function (li) {
    li.dataset.text = (li.textContent || "").toLowerCase();
  });

  var activeGroup = "all";
  var query = "";

  function refresh() {
    var shown = 0;

    items.forEach(function (li) {
      var section = li.closest("[data-group]");
      var groupOk = activeGroup === "all" || (section && section.dataset.group === activeGroup);
      var textOk = !query || li.dataset.text.indexOf(query) !== -1;
      var visible = groupOk && textOk;
      li.classList.toggle("is-hidden", !visible);
      if (visible) shown++;
    });

    groups.forEach(function (g) {
      var any = g.querySelector("[data-item]:not(.is-hidden)");
      g.classList.toggle("is-hidden", !any);
    });

    if (status) {
      status.textContent = (query || activeGroup !== "all")
        ? shown + (shown === 1 ? " entry" : " entries")
        : items.length + " entries";
    }

    var empty = scope.querySelector(".empty-state");
    if (empty) empty.classList.toggle("is-hidden", shown !== 0);
  }

  if (input) {
    var timer;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        query = input.value.trim().toLowerCase();
        refresh();
      }, 110);
    });
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) {
        c.classList.remove("is-active");
        c.setAttribute("aria-pressed", "false");
      });
      chip.classList.add("is-active");
      chip.setAttribute("aria-pressed", "true");
      activeGroup = chip.dataset.group || "all";
      refresh();
    });
  });

  refresh();
})();
