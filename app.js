/* Portfolio site - original hand-written vanilla JS.
   No dependencies, no external requests. Two jobs:
   1. filter the project grid by focus area (role)
   2. build the "impact at a glance" bar chart from inline JSON data
   The site works fully offline; this script only reads inline data + the DOM. */

(function () {
  "use strict";

  // ---- 1. Project filter ------------------------------------------------
  var filters = document.querySelectorAll(".filter");
  var cards = document.querySelectorAll(".card");

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

  // ---- 2. Hand-built bar chart -----------------------------------------
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
      chart.textContent = "No impact figures available.";
      return;
    }

    var max = rows[0].impact_eur;
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
      val.textContent = euro(p.impact_eur) + " / yr";

      row.appendChild(name);
      row.appendChild(track);
      row.appendChild(val);
      frag.appendChild(row);
    });

    chart.innerHTML = "";
    chart.appendChild(frag);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildChart);
  } else {
    buildChart();
  }
})();
