/* Portfolio site - original hand-written vanilla JS.
   No dependencies, no external requests. Three jobs:
   1. filter the project grid by focus area (role)
   2. build the "impact at a glance" bar chart from inline JSON data
   3. drive the EN <-> DE language toggle (same URL, no reload)
   The site works fully offline; this script only reads inline data + the DOM. */

(function () {
  "use strict";

  var STORAGE_KEY = "portfolio-lang";
  var SUPPORTED = { en: true, de: true };

  // Strings the JS itself injects (the chart) - shipped inline, no network.
  var I18N = {
    perYear: { en: " / yr", de: " / Jahr" },
    noImpact: {
      en: "No impact figures available.",
      de: "Keine Impact-Zahlen verfügbar."
    }
  };

  var currentLang = "en";

  var filters = document.querySelectorAll(".filter");
  var cards = document.querySelectorAll(".card");
  var langButtons = document.querySelectorAll(".lang-btn");

  // ---- 1. Project filter ------------------------------------------------
  function applyFilter(value) {
    cards.forEach(function (card) {
      var match = value === "all" || card.getAttribute("data-role") === value;
      card.classList.toggle("is-hidden", !match);
    });
    filters.forEach(function (btn) {
      var active = btn.getAttribute("data-filter") === value;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  filters.forEach(function (btn) {
    btn.addEventListener("click", function () {
      applyFilter(btn.getAttribute("data-filter"));
    });
  });

  // ---- 2. Language toggle (EN <-> DE, same URL, no reload) --------------
  function pickLang(value) {
    return value === "de" || value === "en" ? value : null;
  }

  // Precedence: ?lang= wins for THIS visit; else the user's persisted choice;
  // else navigator.language ("de*" -> German, otherwise English). The canonical
  // shareable URL stays plain - we never redirect or touch the URL.
  function detectLang() {
    try {
      var params = new URLSearchParams(window.location.search);
      var q = pickLang(params.get("lang"));
      if (q) return q;
    } catch (e) { /* URLSearchParams missing: fall through */ }
    try {
      var stored = pickLang(window.localStorage.getItem(STORAGE_KEY));
      if (stored) return stored;
    } catch (e) { /* localStorage blocked: fall through */ }
    var nav = (navigator.language || navigator.userLanguage || "").toLowerCase();
    return nav.indexOf("de") === 0 ? "de" : "en";
  }

  function applyLang(lang) {
    if (!SUPPORTED[lang]) lang = "en";
    currentLang = lang;
    document.documentElement.setAttribute("lang", lang);

    // Swap every paired element's text in place.
    var nodes = document.querySelectorAll("[data-en]");
    for (var i = 0; i < nodes.length; i++) {
      var el = nodes[i];
      var val = el.getAttribute("data-" + lang);
      if (val !== null) el.textContent = val;
    }

    langButtons.forEach(function (btn) {
      var on = btn.getAttribute("data-lang") === lang;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });

    // The JS-built chart carries a translated unit suffix, so rebuild it.
    buildChart();
  }

  langButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      var lang = pickLang(btn.getAttribute("data-lang")) || "en";
      try {
        window.localStorage.setItem(STORAGE_KEY, lang);
      } catch (e) { /* persistence is best-effort */ }
      applyLang(lang);
    });
  });

  // ---- 3. Hand-built bar chart -----------------------------------------
  function readData() {
    var node = document.getElementById("projects-data");
    if (!node) return [];
    try {
      return JSON.parse(node.textContent || "[]");
    } catch (e) {
      return [];
    }
  }

  function euro(n) {
    if (n >= 1000000) return "EUR " + (n / 1000000).toFixed(n % 1000000 === 0 ? 0 : 1) + "M";
    if (n >= 1000) return "EUR " + Math.round(n / 1000) + "k";
    return "EUR " + n;
  }

  function buildChart() {
    var chart = document.getElementById("chart");
    if (!chart) return;

    var rows = readData()
      .filter(function (p) { return typeof p.impact_eur === "number" && p.impact_eur > 0; })
      .sort(function (a, b) { return b.impact_eur - a.impact_eur; });

    if (!rows.length) {
      chart.textContent = I18N.noImpact[currentLang] || I18N.noImpact.en;
      return;
    }

    var max = rows[0].impact_eur;
    var suffix = I18N.perYear[currentLang] || I18N.perYear.en;
    var frag = document.createDocumentFragment();

    rows.forEach(function (p) {
      var row = document.createElement("div");
      row.className = "bar-row";

      var name = document.createElement("div");
      name.className = "bar-name";
      name.textContent = p.name;

      var track = document.createElement("div");
      track.className = "bar-track";
      var fill = document.createElement("div");
      fill.className = "bar-fill";
      var pct = Math.max(2, (p.impact_eur / max) * 100);
      fill.style.width = pct.toFixed(1) + "%";
      track.appendChild(fill);

      var val = document.createElement("div");
      val.className = "bar-val";
      val.textContent = euro(p.impact_eur) + suffix;

      row.appendChild(name);
      row.appendChild(track);
      row.appendChild(val);
      frag.appendChild(row);
    });

    chart.innerHTML = "";
    chart.appendChild(frag);
  }

  // ---- init -------------------------------------------------------------
  // app.js is loaded at the end of <body>, so the DOM is ready here.
  // applyLang() also builds the chart, so no separate initial call is needed.
  applyLang(detectLang());
})();
