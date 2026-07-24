# Results & Visualizations — master catalog

This is the portfolio's single consolidated results document. For **each project** it
records: what it is, the measured result(s), the visualization(s) it produces (with the
output file names), the use case, and 1–2 honest open improvements.

> **All metrics are measured on synthetic, self-generated data** (except FlyHash, which
> uses public MNIST). They demonstrate method, not results on any real company's business.
> The SCS Studio / 3D-to-IFC figures are described from that project's public framing.
> Mentions of Würth or Schwarz are independent analysis of public information, not
> affiliated.

Filenames are as reported in each source repository's README; a `—` marks a figure the
source describes qualitatively rather than as a single number.

---

## 1. revops-optimizer — Analytics (Job #2)

- **What it is:** a revenue-and-operations decision engine that forecasts demand, estimates
  price elasticity and decline risk, then feeds those into four optimizers (assortment,
  inventory, pricing, promotion) to produce one prescriptive plan with a single € uplift.
- **Measured results (240 SKUs, 8 categories):** expected uplift **~€159,966/yr** (pricing
  €35,220 + promo €18,584 + assortment MILP €106,162); carries 29 of 240 SKUs under a
  €56,152/€60,000 capital budget; **forecast MASE 0.75** (seasonal-naive 1.01);
  **decline-risk ROC-AUC 0.99**.
- **Visualizations:** `docs/img/uplift_waterfall.png` (baseline→optimized waterfall);
  executive PDF/PPTX deck (assortment before/after, inventory frontier, price-move
  distribution, promo allocation, model-quality slide); `web/index.html` offline dashboard
  (hand-drawn SVG, light/dark, promo what-if slider); Power BI star schema + DAX.
- **Use case:** a mid-size industrial distributor's quarterly assortment/pricing/inventory
  decision, argued with one € number and a named action list.
- **Open improvements:** (1) the MILP-vs-greedy advantage collapses without the shelf
  constraint — worth making that sensitivity explicit in the UI; (2) models are the
  smallest credible version of each (small MLP, from-scratch ridge/logistic).

## 2. sales-kpi-analytics — Analytics (Job #2)

- **What it is:** 24 months of B2B wholesale orders turned into a QBR — KPIs, margin bridge,
  ABC-XYZ, RFM, out-of-sample forecast, replenishment buy-list. Analytics core is **pure
  Python stdlib** (csv/sqlite3/statistics/json).
- **Measured results:** models a **€21.8M-revenue** distributor; surfaces a **€2.6M/yr
  discount-leakage** lever; forecast evaluated with rolling-origin CV and MASE (honest that
  MASE is above 1 on 24 monthly points); a SQL-vs-Python revenue rollup asserted equal to
  the cent; the margin bridge reconciles `price + volume + mix == total` (test-enforced).
- **Visualizations:** `deliverables/forecast.png` (revenue history + 3-month forecast);
  `deliverables/executive_review.pdf` (8-slide EBR) and `.pptx`; `deliverables/kpi_workbook.xlsx`;
  `deliverables/reorder_list.csv`; offline `web/index.html` dashboard.
- **Use case:** the QBR a distributor's BI team prepares for leadership.
- **Open improvements:** (1) longer/real history so the smarter forecasters earn their keep;
  (2) SKU-grain forecasting with prediction intervals instead of category-grain.

## 3. distributor-intelligence-platform — Analytics (Job #2)

- **What it is:** the MRO command center — describe / forecast / optimize (price, assortment,
  routing) behind one Flask API and one dashboard, composed into a single annual € uplift.
- **Measured results (≈200 SKUs, 8 categories, 52 customers, 24 months):** revenue €4,788,971;
  gross margin €3,257,507 (68.0%); YoY +9.9%; **forecast MASE 0.38** over 9 rolling folds
  (Holt-Winters additive); assortment MILP €935,527 vs greedy €934,503 (**+€1,024**, honestly
  small); pricing uplift **+€95,609**; routing **420 km vs 560 km = 140 km / 25.0% saved**;
  **expected annual uplift €136,972 (4.2% of GM)**.
- **Visualizations:** executive PDF (`deliverables/executive_review.pdf`) + Excel; a hand-built
  command-center dashboard (`templates/`, `static/`); screenshot slots in `docs/img/`.
- **Use case:** one place where descriptive numbers, the forecast and the optimization of
  price/assortment/routing all live together.
- **Open improvements:** (1) the MILP barely beats greedy under this cost structure — worth an
  instance where the gap is material; (2) OTIF is a modelled proxy, not observed service data.

## 4. route-optimizer — Logistics & Optimization (Job #2)

- **What it is:** a Capacitated Vehicle Routing Problem (CVRP) solver measuring how much a
  real optimizer beats the heuristic a dispatcher reaches for by hand.
- **Measured results (60-customer instance, 448 demand, capacity-50 vans):**
  nearest-neighbour 1,445.8 → Clarke-Wright savings 1,046.2 → **OR-Tools (GLS, 8s) 998.3** —
  **−4.6% below Clarke-Wright, −31% below the naive sweep**; both parked 2 of 12 vans. On the
  100-customer instance the gap narrows to ~1% (shown, not hidden).
- **Visualizations:** `deliverables/routes.png` (OR-Tools routes on the 60-customer instance);
  `deliverables/route_plan.csv`; `deliverables/summary.md`; `web/index.html` interactive
  Canvas map with a savings-heuristic overlay toggle and light/dark.
- **Use case:** the last-mile delivery plan a distributor builds every morning.
- **Open improvements:** (1) Euclidean distance, not road-network — add an OSRM/Valhalla
  matrix; (2) single depot, homogeneous fleet, no time windows yet (OR-Tools supports all).

## 5. agentic-automation-lab — Automation (Job #1)

- **What it is:** the same RFQ-intake agent built low-code (n8n) and full-code over **identical
  tool logic**, then scored on nine dimensions.
- **Measured results:** scorecard averages **full-code 4.44, n8n 3.33, Power Automate 2.33**
  (only the runtime figures are measured; the 1–5 ratings are reasoned judgements with cited
  sources); business model estimates **~€625k/yr** of quote-drafting time returned on a
  "a rep still reviews every draft" basis. A mock run drafts Quote Q-15325 in ~13 steps / 12
  tool calls.
- **Visualizations:** `benchmarks/results/scorecard.png` (nine-dimension comparison);
  `benchmarks/results/scorecard.md`; `deliverables/executive_onepager.pdf`; agent trace output.
- **Use case:** deciding low-code vs full-code (vs hybrid) for an agentic automation, with the
  trade-off measured rather than asserted.
- **Open improvements:** (1) a parallel n8n run over the same emails to put measured latency +
  cost beside the Python path; (2) more than one catalog/domain before generalizing the ranking.

## 6. agent-flow-studio — Automation (Job #1)

- **What it is:** a tiny in-browser visual agent-workflow builder — drag nodes, wire ports,
  Run, and watch a mock agent walk the graph and pick tools. No backend, no build step.
- **Measured results:** engine covered by **16 tests** (pure logic; the same `engine.js` runs
  in the browser and under `node --test`); real topological sort (Kahn's algorithm) with cycle
  detection; five node types; business model estimates **~€47k/yr** of engineering time freed
  by letting business users assemble simple flows themselves.
- **Visualizations:** the live canvas itself (hand-drawn SVG wires, node highlighting, live
  wire animation, streamed trace); two example flows in `examples/` (RFQ triage, ticket router);
  `deliverables/executive_onepager.pdf`.
- **Use case:** understanding a low-code agent canvas "from the inside."
- **Open improvements:** (1) a real provider behind the agent node (keep the mock as default);
  (2) no retries/timeouts/parallel branches/sub-flows/loops yet — flows must be acyclic.

## 7. doc-extract-agent — Automation (Job #1)

- **What it is:** unstructured business document in, structured record out — a five-stage
  pipeline (detect → header → line_items → totals → confidence) with a confidence gate.
- **Measured results:** takes per-document handling from **~4 minutes to under 1 second**;
  models a ~60,000-document/yr AP scenario freeing **~€110k/yr** of capacity; totals
  cross-checked against summed line items; two parsing bugs (VAT 19.95 vs 19; Subtotal read as
  Total) pinned by regression tests; EU (`1.234,56`) and US (`1,234.56`) number parsing.
- **Visualizations:** the web UI trace view (per-stage events, confidence scores) served by
  `python -m docextract.server`; JSON/CSV exports; `deliverables/executive_onepager.pdf`.
- **Use case:** an AP & order-desk team keying supplier invoices, order confirmations and
  delivery notes into the ERP.
- **Open improvements:** (1) diff the heuristic against the Anthropic provider to see where
  regex quietly loses; (2) calibrate confidence scores rather than hand-pick thresholds.

## 8. automation-roi-explorer — Automation (Job #1)

- **What it is:** which back-office process to automate first, with the math shown — hours,
  euros, payback and 3-year ROI, ranked by value.
- **Measured results (5 seeded processes):** invoice matching first at **€171,300/yr net,
  2.8-month payback, 769.3% 3y ROI**; full portfolio **13,460 hours and €383,300/yr net**;
  NPV at a flat 8% discount rate. The browser `compute()` mirrors the Python `compute()` line
  for line.
- **Visualizations:** `web/index.html` offline dashboard with **hand-drawn `<canvas>`** bar and
  payback charts (light/dark, live sliders); CLI ranked table; JSON/CSV export.
- **Use case:** a COO with budget to automate one process at a time choosing the order.
- **Open improvements:** (1) model dependencies between processes (shared platform cost, one
  automation unlocking another); (2) ramp-up/seasonality instead of flat volumes.

## 9. bio-efficient-ai — Research

- **What it is:** an honest study that brain-inspired circuits can be *more efficient* than
  conventional methods on narrow tasks. Two experiments.
- **Measured results (public MNIST + synthetic signal, 3 seeds):** **FlyHash precision@10** at
  4/16/64/128 bits = 0.152 / 0.352 / 0.552 / **0.614** vs classical LSH 0.017 / 0.093 / 0.309 /
  0.419 — FlyHash wins at every budget. **Liquid CfC** cell: 3,233 params vs GRU 3,393; clean
  MSE 0.0142 vs 0.0147; MSE @ σ=0.4 noise 0.162 vs 0.168 (equal-or-lower at every noise level
  under noise-trained protocol; honest that clean-only training flips the robustness edge).
- **Visualizations:** the FlyHash precision-vs-bits plot (regenerated by
  `experiments/bench_flyhash.py`); `liquid_robustness.png` (by `experiments/bench_liquid.py`);
  full write-up `paper/bio_efficient_ai.pdf`.
- **Use case:** evaluating whether a bio-inspired primitive earns its place at equal compute.
- **Open improvements:** (1) benchmark against modern ANN search (HNSW/FAISS), currently out of
  scope by design; (2) energy is a proxy, not measured joules — small benchmarks may not
  extrapolate.

## 10. ml-models-lab — Research

- **What it is:** five small models that train locally in seconds; each adapts a published
  method with one principled improvement and an honest metric.
- **Measured results (methodology specs; each model's own README carries final numbers):**
  (1) demand-forecast net — DeepAR-lite global MLP + negative-binomial head, MASE/RMSSE under
  rolling-origin CV; (2) SKU text classifier — fastText core + char-TextCNN, **macro-F1** +
  confusion matrix; (3) order-anomaly AE — undercomplete autoencoder vs a PCA-SVD baseline,
  ROC-AUC + **PR-AUC** + precision@k; (4) churn/at-risk — from-scratch logistic + Platt
  calibration, **PR-AUC** + Brier + ECE + reliability curve; (5) price-elasticity regressor —
  ridge/lasso log-log with hierarchical shrinkage, RMSE/R² **and** simulated profit uplift/regret.
- **Visualizations:** per-model confusion matrix, reliability curve, PR curve, and
  elasticity/profit plots (produced by each model's training script); `docs/METHODOLOGY.md`.
- **Use case:** a reusable pattern library for small, honestly-evaluated B2B distributor models.
- **Open improvements:** (1) consolidate the five into one comparable evaluation harness;
  (2) larger held-out sets so the class-imbalance metrics are tighter.

## 11. logistics-digital-twin — Logistics & Optimization *(in progress)*

- **What it is:** a warehouse digital twin — 3D bin-packing, slotting optimization and a
  discrete-event simulation quantifying the legacy-vs-modern operations gap.
- **Measured results:** **in progress** — the repository is still under construction; the
  package (`logitwin/`) currently holds the synthetic data generator and packing module, with
  the simulation and slotting layers landing next. Metrics to be reported once the DES runs.
- **Visualizations:** a hand-built warehouse-map view and charts (inline SVG / HTML Canvas in
  the web UI, matplotlib for the PDF) are planned/partly built; `deliverables/` is the target
  output directory.
- **Use case:** quantifying the throughput/cost gap between legacy and modern warehouse ops
  under the same demand.
- **Open improvements:** (1) publish the README with the first measured legacy-vs-modern gap;
  (2) wire the packing + slotting output into the discrete-event simulation.

## 12. 3DpicToIFCModeling (SCS Studio) — Flagship (BIM / AEC)

- **What it is:** a finished flagship — one photo in, a furnished, German-workplace-law-compliant
  BIM building out. Photo → AI 3D → ergonomic room and whole-building layout → optimized IFC4.
  Described here from the project's public framing (README only).
- **Reported results (public framing):** an **805-piece** populated 8-storey office tower placed
  by a CP-SAT solver under German **ASR** workplace law; five image-to-3D engines benchmarked on
  **187 photos** against ground-truth meshes by F-score (e.g. TripoSG 0.390, TRELLIS 0.346);
  **measured ROI** one room 59% time saved, a 6-storey office 95.3%, the whole fleet **95.9%**;
  0 real clashes across the bundled buildings (exact polygon-intersection checks); IFC4 round-trips
  that survive Revit; DIN 277 classification in four languages.
- **Visualizations:** `docs/img/hero_xray.jpg` (X-ray of the 805-piece tower); the live 3D
  building explorer and Multi-AI Visualizer in `/hub.html`; engine benchmark tables; before/after
  galleries (chair-graft, smoothing, IFC optimizer); `deliverable/research_export.zip`.
- **Use case:** turning a photo/architectural IFC into a furnished, standards-compliant BIM model.
- **Open improvements (per its own docs):** (1) look-alike product retrieval proved genuinely
  hard — three graded iterations with a roadmap; (2) geometry-only engine exports carry no
  textures and get per-category material tones instead.
