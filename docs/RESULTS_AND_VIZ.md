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

## 11. predictive-maintenance — Applied ML & Ops

- **What it is:** the full predictive-maintenance loop on synthetic, seeded sensor data — 20
  machines × 60 days of correlated multivariate readings, two anomaly detectors trained on
  healthy-only windows (numpy PCA-SVD baseline vs a small PyTorch autoencoder), a 0–100
  health index (labelled a heuristic, **not** an RUL prediction), and CP-SAT crew scheduling
  against a named FIFO baseline.
- **Measured results (seed 42, default config):** PCA **ROC-AUC 0.937 / PR-AUC 0.926** vs
  autoencoder 0.921 / 0.909; precision@50 = 1.000 for both; **10/10** faulty machines
  detected, mean delay **3.4 days** after true onset (PCA) vs 4.8 (AE); validation FPR 5.4%
  at a 5% budget. Scheduling: CP-SAT total weighted delay **778 vs 1013 FIFO (−23.2%)**,
  proven **OPTIMAL**. The pre-stated policy (simpler unless beaten by >0.03 PR-AUC) picks
  the PCA baseline — the AE lost by 0.017. 21 tests.
- **Visualizations:** `deliverables/pdm_report.pdf` (cover with disclaimer, PR curves, health
  ranking, before/after Gantt) and `deliverables/pdm_workbook.xlsx` (Machines, Alerts,
  HealthIndex, Schedule, Comparison sheets).
- **Use case:** an operations team ranking degrading machines and scheduling scarce
  maintenance crews so the riskiest work happens first.
- **Open improvements (its own framing):** (1) fault signatures are the author's own designs,
  so detection delay would not transfer as-is to real telemetry; (2) the scheduling model is
  deliberately small (single-day jobs, uniform crews, no travel/parts) to keep optimality
  provable.

## 12. fraud-detection-ops — Applied ML & Ops

- **What it is:** fraud detection framed around the operational decisions, not the score —
  from-scratch NumPy logistic regression (focal loss vs weighted BCE), Platt calibration, a
  cost-based alert threshold, and a HiGHS-optimized analyst review queue. ~60,000 synthetic
  time-ordered transactions at ~1.45% fraud prevalence, strict time-based split.
- **Measured results (seed 7, test window):** **PR-AUC 0.270** vs 0.034 for the
  amount-rule baseline and 0.013 random, with the generator's own probabilities as an oracle
  ceiling at 0.367; ROC-AUC 0.878; **precision@100 = 0.40** at 1.4% prevalence. Calibration:
  **ECE 0.366 → 0.003** after Platt (Brier 0.158 → 0.012). Chosen threshold t* = 0.047 is
  **43.3% cheaper** than the naive 0.5 default ($8,841 vs $15,587) under labelled cost
  assumptions ($8/review; missed fraud = amount). Queue: the constrained LP gives up only
  0.6% expected value to keep all 8 merchant segments watched; top-K-by-probability recovers
  13% less. 18 tests.
- **Visualizations:** executive PDF + Excel workbook via `python -m fdo --deliverables`
  (matplotlib PdfPages / openpyxl); reliability and cost-curve tables in the report.
- **Use case:** a small analyst team deciding which alerts fire and which 100 of 608 fired
  alerts actually get reviewed.
- **Open improvements (its own framing):** (1) constructed fraud patterns guarantee
  learnability in a way production never does — the oracle ceiling makes that explicit;
  (2) no adversarial adaptation — the generator's drift is scheduled, not responsive.

## 13. energy-demand-forecast — Applied ML & Ops

- **What it is:** day-ahead load forecasting for a synthetic two-shift plant plus battery
  peak shaving as a linear program — all from scratch on numpy/scipy/pandas (Holt-Winters as
  ~30 lines of recursions, regression via `lstsq`, LP via `linprog`/HiGHS on a hand-assembled
  constraint matrix).
- **Measured results (rolling-origin CV, 14 folds):** temperature + calendar regression
  **MASE 0.497 / MAPE 4.8%, 14/14 folds won** vs seasonal-naive 1.369/17.6% and Holt-Winters
  3.040/37.6% (the H-W loss to the naive is reported, not hidden; the Boxing Day fold that
  inflates the naive's mean to 8.40 is unpacked). Peak shaving (400 kWh / 120 kW battery,
  2025): mean monthly peak **368.2 → 291.1 kW (−77.1 kW / 20.9%)**; **~EUR 11,100/yr**
  demand-charge saving at an **assumed** EUR 12/kW-month tariff; the fixed evening-timer
  baseline saved EUR 0. 19 tests.
- **Visualizations:** `deliverables/energy_report.pdf` (6-page executive PDF with the
  per-fold table) and `deliverables/energy_workbook.xlsx` (4 sheets).
- **Use case:** a light-industrial site cutting the demand-charge line of its electricity
  bill — forecast first, then dispatch the battery against the monthly peak.
- **Open improvements (its own framing):** (1) the LP knows the month in advance, so its
  saving is an upper bound — a deployed controller would run on the day-ahead forecast;
  (2) the regression consumes the actual next-day temperature (a "perfect weather forecast"
  assumption).

## 14. quality-anomaly-vision — Applied ML & Ops

- **What it is:** surface-defect screening on 64×64 synthetic procedural textures (scratches,
  blobs, texture-breaks with exact ground-truth masks): local statistics vs PCA reconstruction
  vs a small conv autoencoder (105,521 params), all trained on 600 clean images only and
  scored by one shared rule fixed in advance.
- **Measured results (seed 7, 300 test images):** overall ROC-AUC — local stats 0.687, PCA
  **0.772**, autoencoder **0.779**; PR-AUC 0.812/0.813 (PCA/AE); **TPR @ 5% FPR: PCA 0.407 vs
  AE 0.393**; mean IoU: PCA 0.207 best (random heatmaps: 0.011). The pre-stated rule
  (simplest method within 0.02 ROC-AUC wins) **recommends PCA** — the AE is only 0.007 ahead.
  Reported surprises: 30 epochs halves training loss but drops AUC 0.779 → 0.738 (blobs
  0.828 → 0.610); texture-breaks are the hard class — only the AE is meaningfully above
  chance (0.609), and the best localization on them is IoU 0.043. 15 tests, two full runs
  bit-identical.
- **Visualizations:** `figures/gallery.png` (per-method heatmaps), `figures/roc_pr.png`,
  `figures/per_type_auc.png`; `deliverables/qa_defect_report.pdf` (5-page) and
  `deliverables/qa_defect_metrics.xlsx` (incl. every raw score so the curves can be
  re-derived).
- **Use case:** a visual QA station deciding whether a deep model earns its keep over the
  boring methods before anyone ships a neural network.
- **Open improvements (its own framing):** (1) the autoencoder is untuned — a better recipe
  might clear the 0.02 margin; (2) no lighting/perspective/focus variation, the classic real
  failure modes, by construction.

## 15. quantum-explainer — Teaching (live PWA)

- **What it is:** an installable, offline-first PWA that teaches one- and two-qubit quantum
  computing on a hand-written state-vector simulator (`sim.js`, ~300 lines, zero
  dependencies) — circuit playground, draggable Bloch sphere (reduced states in two-qubit
  mode), lessons including "What quantum computers are NOT". Live at
  <https://dimitres-kisimov.github.io/quantum-explainer/>.
- **Measured results:** **42 physics/behaviour assertions** pass in plain Node (H|0⟩ gives
  50/50, H·H interference, Bell-state probabilities {00: 0.5, 11: 0.5} with a failing
  factorability check, RY(π) ≈ X up to global phase, norms stay 1 to 1e-10); **57 structural
  checks** in `tools/verify.mjs` prove the manifest, precache list and that the app references
  **no external asset of any kind**; zero runtime network calls after first load.
- **Visualizations:** the app itself — live amplitude/probability readouts, the canvas Bloch
  sphere, the 1000-shot seeded histogram; original SVG-sourced icons.
- **Use case:** a curious person building correct quantum intuition without matrix walls or
  "tries every answer at once" hype; every claim demonstrated live or cited (Nielsen &
  Chuang, Preskill's NISQ paper, and five more references).
- **Open improvements:** (1) two qubits is the honest ceiling for full state display — a
  three-qubit mode would need a different visual language; (2) lessons could link out to
  exercises, kept offline-first.

## 16. logistics-flow-studio — Logistics & Optimization (WarehouseTwin + LSP Planner)

- **What it is:** a game-like warehouse digital-twin PWA (WarehouseTwin) plus a network-level
  planning game (LSP Planner at `lsp/`) — hand-written HTML/CSS/JS, no build step, fully
  offline, installable, with a seeded deterministic simulation, an explainable rule-based
  advisor, an A/B predictor, a one-click layout optimizer, twelve storage systems,
  material-flow chains, push-vs-pull inventory, and a demo/full tier gate honestly documented
  as a showcase gate (not DRM). **All five passes shipped (P1–P5).**
- **Measured results (pinned in `docs/MEASUREMENTS.md`, seed 42, starter demo layout):** the
  golden-zone optimizer cuts average pick travel **36.70 → 18.85 m/order (−48.6%)**,
  reproducible headlessly via `node measure_optimizer.js`; **ABC 80/20 beats random slotting
  by ~21%** (46.71 → 36.70 m/order) — the measurement behind the advisor's suggestion. LSP
  Planner's `lsp/verify.js` harness proves determinism and the level lessons (L3 pull beats
  push, L4 a cross-dock pays off) on every run.
- **Visualizations:** the live canvas floor plan and network map themselves;
  `docs/img/warehousetwin.png` and `docs/img/lsp-planner.png`; KPI panels, A/B diff panels,
  optimizer ghost previews.
- **Use case:** learning warehouse/network trade-offs (selectivity vs density, slotting,
  push vs pull, risk pooling, FTL vs LTL) by playing with them — a teaching twin, not a WMS.
- **Open improvements (its own framing):** (1) simulation simplifications are documented in
  `docs/DOMAIN_NOTES.md` — it charges handling deltas, not a full labour model; (2) the
  Android path ships as a Bubblewrap/TWA scaffold only — signing and store submission are the
  owner's steps.

## 17. 3DpicToIFCModeling (SCS Studio) — Flagship (BIM / AEC)

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
