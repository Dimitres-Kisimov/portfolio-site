# Results & Visualizations — master catalog

This is the portfolio's single consolidated results document. For **each project** it
records: what it is, the measured result(s), the visualization(s) it produces (with the
output file names), the use case, and 1–2 honest open improvements.

> **All metrics are measured on synthetic, self-generated data** (except FlyHash, which
> uses public MNIST, and two projects that run the real public UCI Online Retail II
> dataset: `retail-analytics-real`, which analyzes it end to end, and `decision-chain`,
> which runs it through a provenance-tagged pipeline — its real and synthetic-assigned
> quantities are labelled per line). They demonstrate method, not results on any real
> company's business. The SCS Studio / 3D-to-IFC figures are described from that
> project's public framing. Mentions of Würth or Schwarz are independent analysis of
> public information, not affiliated.

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
  **decline-risk ROC-AUC 0.99**. The euro headline is stress-tested two ways: a one-way
  tornado ranks the eight drivers (the capital budget swings the uplift most, €41,935; the
  promo budget least, €138), and a joint fixed-seed Monte-Carlo (256 draws) puts the
  **P10–P90 band at €145,091–170,723/yr** with only a **~43% chance** of clearing the
  €159,966 point estimate — reported, not hidden, and labelled illustrative planning
  ranges on synthetic data, not a forecast.
- **Visualizations:** `docs/img/uplift_waterfall.png` (baseline→optimized waterfall);
  `deliverables/sensitivity_tornado.svg` + `.csv` (driver tornado);
  `deliverables/uplift_distribution.svg` + `uplift_simulation.csv` (Monte-Carlo band);
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
  ABC-XYZ, RFM, pacing to plan, out-of-sample forecast, replenishment buy-list. Analytics
  core is **pure Python stdlib** (csv/sqlite3/statistics/json).
- **Measured results:** models a **€21.8M-revenue** distributor; surfaces a **€2.6M/yr
  discount-leakage** lever; forecast evaluated with rolling-origin CV and MASE (honest that
  MASE is above 1 on 24 monthly points); a SQL-vs-Python revenue rollup asserted equal to
  the cent; the margin bridge reconciles `price + volume + mix == total` (test-enforced).
  Pacing to plan with an empirical prediction interval: the run-rate projection
  (**€10.91M, 95.7%** of the assumed plan) carries an 80% interval built from the model's
  own backtest errors — and the module shows the back-check, the realised year landing at
  **98.9% of plan just above the band**: an honest miss an 80% interval is expected to
  make about one year in five.
- **Visualizations:** `deliverables/forecast.png` (revenue history + 3-month forecast);
  `deliverables/pacing_bullet.svg` (pacing bullet chart, euro labels asserted equal to the
  computed figures); `deliverables/executive_review.pdf` (8-slide EBR) and `.pptx`;
  `deliverables/kpi_workbook.xlsx`; `deliverables/reorder_list.csv`; offline
  `web/index.html` dashboard.
- **Use case:** the QBR a distributor's BI team prepares for leadership.
- **Open improvements:** (1) longer/real history so the smarter forecasters earn their keep;
  (2) SKU-grain forecasting with prediction intervals instead of category-grain.

## 3. distributor-intelligence-platform — Analytics (Job #2)

- **What it is:** the MRO command center — describe / forecast / optimize (price, assortment,
  routing, inventory) behind one Flask API and one dashboard, composed into a single annual
  € uplift.
- **Measured results (≈200 SKUs, 8 categories, 52 customers, 24 months):** revenue €4,788,971;
  gross margin €3,257,507 (68.0%, 24-month); YoY +9.9%; **forecast MASE 0.38** over 9 rolling
  folds (Holt-Winters additive); assortment MILP €935,527 vs greedy €934,503 (**+€1,024**,
  honestly small); pricing uplift **+€95,609**; routing **420 km vs 560 km = 140 km / 25.0%
  saved**; **expected annual uplift €136,972 (8.4% of annual gross margin — the 24-month
  history halved)**. A continuous-review inventory policy (ROP/EOQ over 200 SKUs) prices
  safety stock from an ABC-XYZ service matrix (A/X lines protected to 98%, long-tail C/Z
  to 88%): **€127,421 working capital, 5.5x turns, 99.9% demand-weighted fill rate** —
  with the 25%/yr carrying rate and €50 order cost stated as planning assumptions.
- **Visualizations:** executive PDF (`deliverables/executive_review.pdf`) + Excel; a hand-built
  command-center dashboard (`templates/`, `static/`); the inventory policy served via
  `GET /api/inventory` (per-SKU rows + a nine-cell ABC-XYZ roll-up); screenshot slots in
  `docs/img/`.
- **Use case:** one place where descriptive numbers, the forecast and the optimization of
  price/assortment/inventory/routing all live together.
- **Open improvements:** (1) the MILP barely beats greedy under this cost structure — worth an
  instance where the gap is material; (2) OTIF is a modelled proxy, not observed service data.

## 4. retail-analytics-real — Analytics (Job #2)

- **What it is:** the real-data counterpart to the synthetic portfolio — the full public UCI
  *Online Retail II* dataset (a UK online giftware retailer, Dec 2009–Dec 2011, CC BY 4.0)
  through cleaning, RFM, cohorts, from-scratch BG/NBD + Gamma-Gamma CLV, forecasting,
  baskets and returns — with the mess kept in view instead of averaged away. Built on
  pandas/NumPy/SciPy only; the mining and CLV cores are from scratch.
- **Measured results (real data, 1,067,371 raw rows):** **94.0% retained** after cleaning
  (1,003,340 sales rows), **GBP 19.6M** gross product revenue. Returns as a first-class
  reverse-logistics stream: **3.65% of gross value** (GBP 716,426) across 17,914 return
  lines (4.18% of units), **95.0% of returned value matched to a prior purchase** at a
  median of 10 days — and the famous 80,995-unit same-day cancellation surfaces exactly
  where it should. The from-scratch CLV is back-tested out of sample: **7,594 predicted
  holdout transactions vs 7,562 actual (0.4% over)**, per-customer correlation 0.85 — and
  CLV is labelled gross revenue, not profit. The honest headline stays up front:
  **seasonal-naive wins the forecasting bake-off** (mean MASE 1.094 vs 1.187 for
  Holt-Winters); **22.77% of rows have no CustomerID** and are flagged rather than
  dropped; the data-quality report card (raw C → cleaned A) is labelled a heuristic
  scorecard with stated weights, not a certification of data correctness. 97 tests.
- **Visualizations:** `deliverables/retail_analytics_executive.pdf`;
  `deliverables/retail_analytics.xlsx` (11 sheets, CleaningReport → DataQuality);
  `deliverables/cohort_retention.csv`, `customer_lifetime_value.csv`,
  `returns_analysis.csv`, `data_quality_report_card.md`; `figures/` chart set
  (`monthly_revenue.png`, `cohort_retention.svg`, `clv_validation.png`,
  `returns_analysis.png`, and six more).
- **Use case:** honest, leakage-safe retail analytics on real transactions — the project
  that shows what the synthetic-portfolio methods do when the data is genuinely messy.
- **Open improvements (its own framing):** (1) a single UK retailer with one full seasonal
  cycle — exactly why seasonal-naive wins, and the smarter forecasters would need longer
  history to earn their keep; (2) CLV is gross and undiscounted over a finite 180-day
  horizon, and RFM/cohort/CLV cover only the 86.9% of revenue attributable to a known
  customer.

## 5. market-basket-analysis — Analytics (Job #2)

- **What it is:** association-rule mining and cross-sell for a fictional B2B maintenance &
  construction supplies distributor (14 product categories), implemented entirely from
  scratch on numpy/pandas — no scikit-learn, no mlxtend, no mining libraries. Everything
  runs on seeded synthetic data with planted co-purchase bundles as ground truth.
- **Measured results (seed 42, 6,000 orders, min support 2%):** **224 frequent itemsets**
  and **254 rules** kept at confidence ≥ 30% and lift ≥ 1.10; an independent FP-growth
  implementation returns the **exact same itemsets and supports** (test-asserted); all six
  planted category pairs are recovered at lift ≥ 1.5. The recommender is back-tested
  leave-one-out on held-out baskets (70/30 arrival-order split): **hit-rate@3 60.2% vs
  34.4%** for a popularity baseline (**1.75x**; MRR 0.455 vs 0.311). Rule stability across
  4 time windows: 18 of the top 20 rules stable, 2 flagged window-specific. The category
  affinity network: **14 categories, 27 lift-weighted edges, 3 communities at weighted
  modularity 0.58** (greedy modularity maximisation, Newman 2004) with 4 bridge edges —
  and the communities mirror the three k-means segments found independently. 55 tests.
- **Visualizations:** `deliverables/cross_sell_briefing.pdf` (7 pages: rules table,
  lift heatmap, affinity communities, segments, stability, back-test);
  `deliverables/market_basket_analysis.xlsx` (7 sheets); hand-drawn SVG + CSV pairs:
  `rule_stability`, `recommender_backtest`, `affinity_network`.
- **Use case:** which category a rep should offer next given what is already in the order —
  plus the category groups a category manager uses for bundles, planogram adjacency and
  the promo calendar.
- **Open improvements (its own framing):** (1) the synthetic generator is stationary, so
  durable rules are expected to persist — the identical stability check on real order
  history is what would separate durable rules from seasonal artefacts; (2) the cross-sell
  euro uplift is an ESTIMATE with a stated assumption — real attach rates would have to
  come from an A/B test, and lift is co-purchase frequency, not causation.

## 6. route-optimizer — Logistics & Optimization (Job #2)

- **What it is:** a Capacitated Vehicle Routing Problem (CVRP) solver measuring how much a
  real optimizer beats the heuristic a dispatcher reaches for by hand.
- **Measured results (60-customer instance, 448 demand, capacity-50 vans):**
  nearest-neighbour 1,445.8 → Clarke-Wright savings 1,046.2 → **OR-Tools (GLS, 8s) 998.3** —
  **−4.6% below Clarke-Wright, −31% below the naive sweep**; both parked 2 of 12 vans. On the
  100-customer instance the gap narrows to ~1% (shown, not hidden). A robustness stress test
  drives each plan through **200 seeded demand scenarios** (a labelled ±15% noise
  assumption): both zero-buffer plans hit a capacity failure in **~96%** of them, and the
  optimizer stays ahead by recovering cheaper (**117 vs 178 km** expected recourse per day);
  re-planning with just **5% capacity headroom** costs +3.0% planned km but cuts failing
  scenarios to **44%** — the cheapest expected day in the sweep. 36 tests.
- **Visualizations:** `deliverables/routes.png` (OR-Tools routes on the 60-customer instance);
  `deliverables/route_plan.csv`; `deliverables/summary.md`; `deliverables/robustness.svg` +
  `.csv` + `.md` (the scenario sweep); `web/index.html` interactive Canvas map with a
  savings-heuristic overlay toggle and light/dark.
- **Use case:** the last-mile delivery plan a distributor builds every morning — now with the
  buffer question ("how much headroom is worth paying for?") answered with a measured sweep.
- **Open improvements:** (1) Euclidean distance, not road-network — add an OSRM/Valhalla
  matrix; (2) single depot, homogeneous fleet, no time windows yet (OR-Tools supports all).

## 7. supply-network-opt — Logistics & Optimization (Job #2)

- **What it is:** three classic supply-network questions wired together on one seeded
  synthetic dataset (seed 42; 3 plants, 8 candidate DCs, 30 customer zones, 17,880 units):
  where to put the DCs (capacitated facility-location MILP), how product should flow
  (min-cost flow, cross-checked), and how much safety stock each tier needs — plus CO2,
  disruption-resilience and service-level-frontier sensitivity views.
- **Measured results:** the MILP (OR-Tools CBC) opens **3 of 8** candidate DCs for
  **$310,666** total cost vs a named greedy baseline at **$394,216** (opens 4) —
  **$83,550 / 21.2% lower**, not "the best anyone could do". The plant→DC→customer
  min-cost flow ($105,245.59) is solved twice — as a graph and as a HiGHS transportation
  LP — **agreeing to $0.00**. Risk pooling at 95% service: **23,168 → 7,946 safety-stock
  units (−65.7%)** pooled into the 3 opened DCs (fully centralized 4,608, −80.1%). The
  service-level frontier prices diminishing returns: lifting service **97.5% → 99.0%
  costs ~$14,750/yr per point — ~6.3x** the first increment. The CO2 sweep re-solves the
  MILP at every network density: every density is Pareto-optimal on (cost, CO2), and a
  4th DC cuts modelled CO2 18.6% for +26.9% cost. The N-1 screen is blunt: the
  cost-optimal 3-DC network is **not N-1 resilient** — every opened DC is critical; the
  worst single outage drops service to 59.6% and costs $157,016 to restore. 53 tests.
- **Visualizations:** executive PDF (cover with disclaimer, network map of opened DCs and
  flows, cost-breakdown bar, pooling chart, cost-vs-CO2 Pareto page, resilience page,
  service-frontier page) + Excel workbook (9 sheets, Summary → Assignment);
  `deliverables/co2_cost_frontier.svg` + `co2_sensitivity.csv`;
  `deliverables/service_frontier.svg` + `.csv` (all SVGs hand-drawn).
- **Use case:** the network-design conversation a distributor has every few years — where
  to put DCs, how product should flow, how much stock each tier needs — with service, CO2
  and robustness priced instead of asserted.
- **Open improvements (its own framing):** (1) the resilience screen models capacity as the
  only hard limit with deterministic demand — a planning screen, not an SLA; (2) the
  economics are labelled illustrative ($50/unit, 25%/yr carrying, a placeholder CO2
  factor) and the "same inventory buys more service" read sits deep in the normal tail —
  a direction, not a service guarantee.

## 8. agentic-automation-lab — Automation (Job #1)

- **What it is:** the same RFQ-intake agent built low-code (n8n) and full-code over **identical
  tool logic**, then scored on nine dimensions.
- **Measured results:** scorecard averages **full-code 4.44, n8n 3.33, Power Automate 2.33**
  (only the runtime figures are measured; the 1–5 ratings are reasoned judgements with cited
  sources); business model estimates **~€625k/yr** of quote-drafting time returned on a
  "a rep still reviews every draft" basis. A mock run drafts Quote Q-15325 in ~13 steps / 12
  tool calls. A token & cost model prices the same nine task fixtures against a dated
  per-model price sheet: at the ~104,000-email annual volume the flagship agent costs
  **~$846/yr on Claude Haiku 4.5 (~$4,232 on Opus 4.8)** next to the ~€625k of labour the
  business case says it offsets — tokens from the deterministic mock's chars/4 estimate,
  an order-of-magnitude planning model, not a bill.
- **Visualizations:** `benchmarks/results/scorecard.png` (nine-dimension comparison);
  `benchmarks/results/scorecard.md`; `eval/cost_scorecard.md` (+ `.json`/`.csv`, byte-stable);
  `deliverables/executive_onepager.pdf`; agent trace output.
- **Use case:** deciding low-code vs full-code (vs hybrid) for an agentic automation, with the
  trade-off measured rather than asserted — and the model bill estimated before anyone runs it.
- **Open improvements:** (1) a parallel n8n run over the same emails to put measured latency +
  cost beside the Python path; (2) more than one catalog/domain before generalizing the ranking.

## 9. agent-flow-studio — Automation (Job #1)

- **What it is:** a tiny in-browser visual agent-workflow builder — drag nodes, wire ports,
  Run, and watch a mock agent walk the graph and pick tools. No backend, no build step.
- **Measured results:** covered by **60 tests** (engine logic, undo history, snapshot
  rendering, flow linter, dependency analyzer — pure logic; the same `engine.js` runs in
  the browser and under `node --test`); real topological sort (Kahn's algorithm) with cycle
  detection; five node types. A static data-dependency / provenance analyzer (`analysis.js`)
  computes each node's upstream/downstream closure, the parallelisable stages, the critical
  path and which Trigger's payload can reach every Output — honest that it describes the
  data flow the wiring permits, not the single path one input takes, and it withholds the
  order-dependent fields when the graph is not a DAG. Business model estimates **~€47k/yr**
  of engineering time freed by letting business users assemble simple flows themselves.
- **Visualizations:** the live canvas itself (hand-drawn SVG wires, node highlighting, live
  wire animation, streamed trace); two example flows in `examples/` (RFQ triage, ticket router);
  `deliverables/executive_onepager.pdf`.
- **Use case:** understanding a low-code agent canvas "from the inside."
- **Open improvements:** (1) a real provider behind the agent node (keep the mock as default);
  (2) no retries/timeouts/parallel branches/sub-flows/loops yet — flows must be acyclic.

## 10. doc-extract-agent — Automation (Job #1)

- **What it is:** unstructured business document in, structured record out — a five-stage
  pipeline (detect → header → line_items → totals → confidence) with a confidence gate and
  a business-rule validation layer.
- **Measured results:** takes per-document handling from **~4 minutes to under 1 second**;
  models a ~60,000-document/yr AP scenario freeing **~€110k/yr** of capacity; totals
  cross-checked against summed line items. Only documents that reconcile, clear the
  confidence gate and pass the business rules post automatically — requiring the rules as
  well as the gate lifts measured auto-post precision from **70% to 87.5%**, and the README
  says plainly that 87.5% is not 100%, naming the multicurrency case it still misses. Two
  parsing bugs (VAT 19.95 vs 19; Subtotal read as Total) pinned by regression tests; EU
  (`1.234,56`) and US (`1,234.56`) number parsing.
- **Visualizations:** the web UI trace view (per-stage events, confidence scores) served by
  `python -m docextract.server`; JSON/CSV exports; `deliverables/executive_onepager.pdf`.
- **Use case:** an AP & order-desk team keying supplier invoices, order confirmations and
  delivery notes into the ERP.
- **Open improvements:** (1) diff the heuristic against the Anthropic provider to see where
  regex quietly loses; (2) calibrate confidence scores rather than hand-pick thresholds.

## 11. automation-roi-explorer — Automation (Job #1)

- **What it is:** which back-office process to automate first, with the math shown — hours,
  euros, payback and 3-year ROI, ranked by value.
- **Measured results (5 seeded processes):** invoice matching first at **€171,300/yr net,
  2.8-month payback, 769.3% 3y ROI**; full portfolio **13,460 hours and €383,300/yr net**;
  NPV at a flat 8% discount rate. The browser `compute()` mirrors the Python `compute()` line
  for line. A phased-rollout module lays the same economics onto a monthly timeline: a
  6-month linear adoption ramp pushes the top pick's payback from an idealised 2.8 months
  to **month 6** and forgoes **~€37,200** of 3-year net benefit (€436,700 ramped vs
  €473,900) — with the linear ramp labelled an illustrative assumption, not a measured
  adoption curve.
- **Visualizations:** `web/index.html` offline dashboard with **hand-drawn `<canvas>`** bar and
  payback charts (light/dark, live sliders); `deliverables/rollout_cashflow.svg` + `.csv`
  (the ramped monthly cashflow); CLI ranked table; JSON/CSV export.
- **Use case:** a COO with budget to automate one process at a time choosing the order.
- **Open improvements:** (1) model dependencies between processes (shared platform cost, one
  automation unlocking another); (2) seasonality and volume variation — the ramp-up half of
  the old "flat volumes" gap is now built as the phased-rollout module.

## 12. bio-efficient-ai — Research

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

## 13. ml-models-lab — Research

- **What it is:** five small models that train locally in seconds; each adapts a published
  method with one principled improvement and an honest metric.
- **Measured results (methodology specs; each model's own README carries final numbers):**
  (1) demand-forecast net — DeepAR-lite global MLP + negative-binomial head, MASE/RMSSE under
  rolling-origin CV; (2) SKU text classifier — fastText core + char-TextCNN, **macro-F1** +
  confusion matrix; (3) order-anomaly AE — undercomplete autoencoder vs a PCA-SVD baseline,
  ROC-AUC + **PR-AUC** + precision@k; (4) churn/at-risk — from-scratch logistic + Platt
  calibration, **PR-AUC** + Brier + ECE + reliability curve; (5) price-elasticity regressor —
  ridge/lasso log-log with hierarchical shrinkage, RMSE/R² **and** simulated profit uplift/regret.
  A non-parametric percentile bootstrap puts 95% confidence intervals on the skill scores of
  the two numpy models — churn **+0.457 [+0.381, +0.528]**, elasticity-RMSE
  **+0.918 [+0.904, +0.934]**, both entirely above zero — covering only the deterministic
  numpy models on purpose, so the intervals are bit-reproducible and CI-verifiable.
- **Visualizations:** per-model confusion matrix, reliability curve, PR curve, and
  elasticity/profit plots (produced by each model's training script); `docs/METHODOLOGY.md`.
- **Use case:** a reusable pattern library for small, honestly-evaluated B2B distributor models.
- **Open improvements:** (1) consolidate the five into one comparable evaluation harness;
  (2) larger held-out sets so the class-imbalance metrics are tighter.

## 14. predictive-maintenance — Applied ML & Ops

- **What it is:** the full predictive-maintenance loop on synthetic, seeded sensor data — 20
  machines × 60 days of correlated multivariate readings, two anomaly detectors trained on
  healthy-only windows (numpy PCA-SVD baseline vs a small PyTorch autoencoder), a 0–100
  health index (labelled a heuristic, **not** an RUL prediction), CP-SAT crew scheduling
  against a named FIFO baseline, and a Weibull-based maintenance-policy optimizer.
- **Measured results (seed 42, default config):** PCA **ROC-AUC 0.937 / PR-AUC 0.926** vs
  autoencoder 0.921 / 0.909; precision@50 = 1.000 for both; **10/10** faulty machines
  detected, mean delay **3.4 days** after true onset (PCA) vs 4.8 (AE); validation FPR 5.4%
  at a 5% budget. Scheduling: CP-SAT total weighted delay **778 vs 1013 FIFO (−23.2%)**,
  proven **OPTIMAL**. The pre-stated policy (simpler unless beaten by >0.03 PR-AUC) picks
  the PCA baseline — the AE lost by 0.017. A two-parameter Weibull fitted by censored
  maximum likelihood on 6 observed failures and 14 suspensions (shape 4.81 — wear-out)
  prices three maintenance policies per machine-day: age replacement at **T\* = 44.4 days
  cuts modelled cost 51.7%** vs run-to-failure — and the optimizer's own base-case check
  reports that for memoryless lifetimes no finite replacement age beats run-to-failure.
  63 tests.
- **Visualizations:** `deliverables/pdm_report.pdf` (cover with disclaimer, PR curves, health
  ranking, before/after Gantt) and `deliverables/pdm_workbook.xlsx` (Machines, Alerts,
  HealthIndex, Schedule, Comparison sheets).
- **Use case:** an operations team ranking degrading machines and scheduling scarce
  maintenance crews so the riskiest work happens first.
- **Open improvements (its own framing):** (1) fault signatures are the author's own designs,
  so detection delay would not transfer as-is to real telemetry; (2) the scheduling model is
  deliberately small (single-day jobs, uniform crews, no travel/parts) to keep optimality
  provable.

## 15. fraud-detection-ops — Applied ML & Ops

- **What it is:** fraud detection framed around the operational decisions, not the score —
  from-scratch NumPy logistic regression (focal loss vs weighted BCE), Platt calibration, a
  cost-based alert threshold, a HiGHS-optimized analyst review queue, and a
  champion/challenger retrain policy. ~60,000 synthetic time-ordered transactions at ~1.45%
  fraud prevalence, strict time-based split.
- **Measured results (seed 7, test window):** **PR-AUC 0.270** vs 0.034 for the
  amount-rule baseline and 0.013 random, with the generator's own probabilities as an oracle
  ceiling at 0.367; ROC-AUC 0.878; **precision@100 = 0.40** at 1.4% prevalence. Calibration:
  **ECE 0.366 → 0.003** after Platt (Brier 0.158 → 0.012). Chosen threshold t* = 0.047 is
  **43.3% cheaper** than the naive 0.5 default ($8,841 vs $15,587) under labelled cost
  assumptions ($8/review; missed fraud = amount). Queue: the constrained LP gives up only
  0.6% expected value to keep all 8 merchant segments watched; top-K-by-probability recovers
  13% less. A champion/challenger retrain on a rolling window is judged by a swap-set
  analysis, not headline metrics alone: the challenger swaps in just 2 alerts and catches 4
  fewer frauds — it wins by shedding 139 low-yield alerts, a net **$210 (2.4%) cheaper** —
  and five pre-declared gates (labelled policy knobs, not statistical laws) all pass, so
  the measured verdict is **PROMOTE**. 42 tests.
- **Visualizations:** executive PDF + Excel workbook via `python -m fdo --deliverables`
  (matplotlib PdfPages / openpyxl); reliability and cost-curve tables in the report.
- **Use case:** a small analyst team deciding which alerts fire, which 100 of 608 fired
  alerts actually get reviewed, and whether the retrained model earns its promotion.
- **Open improvements (its own framing):** (1) constructed fraud patterns guarantee
  learnability in a way production never does — the oracle ceiling makes that explicit;
  (2) no adversarial adaptation — the generator's drift is scheduled, not responsive.

## 16. energy-demand-forecast — Applied ML & Ops

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
  baseline saved EUR 0. A causal, forecast-driven dispatch backtest measures **72.7%
  capture** of that perfect-foresight bound (**EUR 8,066** of the EUR 11,100/yr),
  decomposed into EUR 2,054/yr lost to forecast error and EUR 980/yr to the one-day
  horizon. 59 tests.
- **Visualizations:** `deliverables/energy_report.pdf` (6-page executive PDF with the
  per-fold table) and `deliverables/energy_workbook.xlsx` (4 sheets).
- **Use case:** a light-industrial site cutting the demand-charge line of its electricity
  bill — forecast first, then dispatch the battery against the monthly peak.
- **Open improvements (its own framing):** (1) the perfect-foresight LP stays an explicit
  upper bound — the causal backtest now measures what a deployed, forecast-driven
  controller captures of it (72.7%); (2) the regression consumes the actual next-day
  temperature (a "perfect weather forecast" assumption).

## 17. quality-anomaly-vision — Applied ML & Ops

- **What it is:** surface-defect screening on 64×64 synthetic procedural textures (scratches,
  blobs, texture-breaks with exact ground-truth masks): local statistics vs PCA reconstruction
  vs a small conv autoencoder (105,521 params), all trained on 600 clean images only and
  scored by one shared rule fixed in advance — plus an SPC monitoring layer over the
  screening output.
- **Measured results (seed 7, 300 test images):** overall ROC-AUC — local stats 0.687, PCA
  **0.772**, autoencoder **0.779**; PR-AUC 0.812/0.813 (PCA/AE); **TPR @ 5% FPR: PCA 0.407 vs
  AE 0.393**; mean IoU: PCA 0.207 best (random heatmaps: 0.011). The pre-stated rule
  (simplest method within 0.02 ROC-AUC wins) **recommends PCA** — the AE is only 0.007 ahead.
  Reported surprises: 30 epochs halves training loss but drops AUC 0.779 → 0.738 (blobs
  0.828 → 0.610); texture-breaks are the hard class — only the AE is meaningfully above
  chance (0.609), and the best localization on them is IoU 0.043. The screening output
  feeds an SPC p-chart with limits frozen from Phase I (center line 1.31%, UCL 2.07%) and
  the four Western Electric run rules: a true 1.5% → 2.5% defect-rate shift is **caught at
  subgroup 43 by a run rule while the naked 3-sigma rule never fires** in the monitored
  window, and a camera-brightness drift with an unchanged true defect rate still alarms —
  the cost of that sensitivity stated as in-control ARL ~92 vs ~370 for 3-sigma alone.
  45 tests, two full runs bit-identical.
- **Visualizations:** `figures/gallery.png` (per-method heatmaps), `figures/roc_pr.png`,
  `figures/per_type_auc.png`; `deliverables/qa_defect_report.pdf` (5-page) and
  `deliverables/qa_defect_metrics.xlsx` (incl. every raw score so the curves can be
  re-derived).
- **Use case:** a visual QA station deciding whether a deep model earns its keep over the
  boring methods before anyone ships a neural network — then watching the line for drift.
- **Open improvements (its own framing):** (1) the autoencoder is untuned — a better recipe
  might clear the 0.02 margin; (2) no lighting/perspective/focus variation, the classic real
  failure modes, by construction.

## 18. quantum-explainer — Teaching (live PWA)

- **What it is:** an installable, offline-first PWA that teaches one- and two-qubit quantum
  computing on a hand-written state-vector simulator (`sim.js`, ~300 lines, zero
  dependencies) — circuit playground, draggable Bloch sphere (reduced states in two-qubit
  mode), lessons including "What quantum computers are NOT" and Deutsch's algorithm. Live at
  <https://dimitres-kisimov.github.io/quantum-explainer/>.
- **Measured results:** **107 physics/behaviour assertions** pass in plain Node (H|0⟩ gives
  50/50, H·H interference, Bell-state probabilities {00: 0.5, 11: 0.5} with a failing
  factorability check, RY(π) ≈ X up to global phase, norms stay 1 to 1e-10); the Deutsch
  lesson is checked for all four oracles — a single query yields the correct
  constant/balanced verdict with certainty, and the oracle leaves the state a product state
  (concurrence 0): phase kickback, not entanglement, even when the oracle is a CNOT.
  **79 structural checks** in `tools/verify.mjs` prove the manifest, precache list and that
  the app references **no external asset of any kind**, plus a **39-check in-app self-test**;
  zero runtime network calls after first load.
- **Visualizations:** the app itself — live amplitude/probability readouts, the canvas Bloch
  sphere, the 1000-shot seeded histogram; original SVG-sourced icons.
- **Use case:** a curious person building correct quantum intuition without matrix walls or
  "tries every answer at once" hype; every claim demonstrated live or cited (Nielsen &
  Chuang, Preskill's NISQ paper, and five more references).
- **Open improvements:** (1) two qubits is the honest ceiling for full state display — a
  three-qubit mode would need a different visual language; (2) lessons could link out to
  exercises, kept offline-first.

## 19. logistics-flow-studio — Logistics & Optimization (WarehouseTwin — WMS + Plant Simulator, v2.0.0)

- **What it is:** an offline, browser-based warehouse / WMS digital twin and plant-flow
  simulator (WarehouseTwin) — hand-written HTML/CSS/JS, no build step, fully offline,
  installable as a PWA, zero network calls. Describe a plant in plain keywords and a
  transparent, deterministic **AI environment generator** (`generate.js` + `nlcommands.js`)
  builds a full valid layout, steerable with plain-language commands (e.g. *"include 2 more
  RGVs in the picking sector"*) — a rule/heuristic engine with an offline NL parser, **not a
  trained model**, and unknown phrasing gets an honest "didn't understand". **23 example
  scenarios**, each synthetic and one-click loadable, with per-example JSON/CSV export. It then
  **simulates the WMS operation** (`wms.js`: receiving → put-away → replenishment → picking →
  packing → shipping) with **ISO 22400-grounded KPIs** and the bottleneck stage named, a **live
  animated material flow** (`flowsim.js`: stations, queues, conveyor-path routing) and a **live
  KPI dashboard** (`kpicharts.js`). Storage & inventory (golden-zone slotting, occupancy,
  retrieval), automation modelling (AS/RS, shuttle, RGV, AGV, conveyor), an **editable
  standards knowledge base** (edit the DIN/ASR/EN/VDI/ISO values the compliance check, advisor
  and generator use), a one-click **Story Mode** cinematic guided tour that flies the camera
  zone-by-zone through the plant, a **user-definable object library** (derive your own object
  types, *Siemens Plant Simulation UserObjects*-style, and they join the palette **and** the
  simulation), zoom/pan on a canvas up to **400 × 250 m**, and **29 equipment types each
  with a 2D schematic and a 3D representation** (press **P** to switch) rendered in detail down
  to rack pallets, floor markings and metre rulers, plus
  the real-world pass: **import your own article/order CSVs** (100% in-browser, row-numbered
  validation, orders replayed exactly, honest "Data: yours" vs "Data: synthetic demo" badge)
  and a **floor-plan image underlay** with two-point metric calibration. A companion **LSP
  Planner** (`lsp/`) network-planning game ships alongside.
- **Measured results (pinned in `docs/MEASUREMENTS.md`, seed 42, starter demo layout):** the
  golden-zone optimizer cuts average pick travel **36.70 → 18.85 m/order (−48.6%)**,
  reproducible headlessly via `node measure_optimizer.js`; **ABC 80/20 beats random slotting
  by ~21%** (46.71 → 36.70 m/order) — the measurement behind the advisor's suggestion. **35
  headless verification harnesses** (`test/run-all.mjs`, no stubs) plus an **in-browser
  self-test (57/57)** back every documented behaviour.
- **Visualizations:** the live canvas floor plan, the animated material flow and the KPI
  cockpit themselves; `docs/img/warehousetwin.png`; compliance highlights, optimizer ghost
  previews, the pick-travel heatmap and the 2D/3D equipment scene (P toggles the 3D view).
- **Use case:** experimenting with warehouse layout, slotting, WMS flow, automation and
  standards trade-offs before touching a real hall — a teaching-scale WMS twin and plant
  simulator, **not** a production WMS or a certification.
- **Outputs & honesty:** a consolidated printable **WMS Report** plus JSON/CSV and a scoped
  **IFC4** export; every figure is synthetic and seeded unless you import your own data; the
  standards work (ISO 22400, DIN 15185, ASR, EN, VDI) is **"informed by, not a certification"**;
  the demo/full tier gate is documented as a client-side showcase gate, not DRM. Runs locally
  via `python -m http.server` or installs as a PWA; the Android path ships as a Bubblewrap/TWA
  scaffold only.

## 20. 3DpicToIFCModeling (SCS Studio) — Flagship (BIM / AEC)

- **What it is:** a finished flagship — one photo in, a furnished, German-workplace-law-compliant
  BIM building out. Photo → AI 3D → ergonomic room and whole-building layout → optimized IFC4.
  Described here from the project's public framing (README only).
- **Reported results (public framing):** an **805-piece** populated 8-storey office tower placed
  by a CP-SAT solver under German **ASR** workplace law; five image-to-3D engines benchmarked on
  **187 photos** against ground-truth meshes by F-score (e.g. TripoSG 0.390, TRELLIS 0.346);
  **measured ROI** one room 59% time saved, a 6-storey office 95.3%, the whole fleet **95.9%**;
  0 real clashes across the bundled buildings (exact polygon-intersection checks), validated
  across a **15-building fleet** (1,506 rooms); IFC4 round-trips that survive Revit; DIN 277
  classification in four languages; shipped through four tagged releases (v1 → v4).
- **Visualizations:** `docs/img/hero_xray.jpg` (X-ray of the 805-piece tower); the live 3D
  building explorer and Multi-AI Visualizer in `/hub.html`; engine benchmark tables; before/after
  galleries (chair-graft, smoothing, IFC optimizer); `deliverable/research_export.zip`.
- **Use case:** turning a photo/architectural IFC into a furnished, standards-compliant BIM model.
- **Open improvements (per its own docs):** (1) look-alike product retrieval proved genuinely
  hard — three graded iterations with a roadmap; (2) geometry-only engine exports carry no
  textures and get per-category material tones instead.

## 21. decision-chain — Flagship (Supply-Chain Integration)

- **What it is:** the integration capstone — **one real dataset** (UCI Online Retail II,
  **1,067,371 raw rows**, two years of a UK giftware distributor) through the **whole
  distributor decision chain**: ingest → forecast → inventory → warehouse → transport →
  costing, closed by a **reconciliation ledger** (stage 6) of machine-checked identity
  assertions that print both numbers at every seam. Every quantity carries a provenance tag
  (`real` | `derived` | `synthetic-assigned`); a derived quantity inherits the **weakest**
  provenance of its inputs.
- **Measured results (full run, all 13 artifact identities PASS, plus 2 additive):** cleaned
  revenue reproduced across two repositories **to the penny — GBP 19,643,861.62**; the
  ledger's window revenue equal to the cleaned data's to the penny (GBP 1,047,042.41); the
  cost ledger summing to the cent (253,427.16); every pick (256,787 lines), carton (70,820)
  and route drop (4,151) conserved. Two additive identities close the remaining seams:
  identity (n) — cost-driver reconstruction — rebuilds each cost line from its physical
  driver × published rate to the cent, and identity (o) — forecast-error containment —
  proves the arc-elasticity of total cost to a whole-book forecast surge equals the
  holding-cost share **exactly (0.0580** on the committed full run**)**, so a doubling of
  forecast demand would raise modelled cost-to-serve by 5.80% while every delivered-cost
  line and the real revenue stay unmoved. Honest findings kept in the headline: on lumpy
  demand **nothing beats the one-week naive walk** (MASE 1.782); the exact Hungarian
  slotting optimum is worth only **−1.6% vs classic ABC** (183.2 → 180.2 m/invoice; the
  rearrangement-inequality math is explained); OR-Tools CVRP beats 1964 Clarke-Wright by
  only **−0.2%** (252,713.5 vs 253,201.2 km) and loses 19 of 48 days; the synthetic
  4-picker crew is **18% utilized**. Every cost rate is INVENTED and labelled — the ledger
  makes **no profit claims**. The fixture-based pytest suite gives each identity a
  deliberate-corruption FAIL path (full-data tests skip without the raw data).
- **Visualizations:** the offline Flask **CHAIN DASHBOARD** (port 5077, no CDNs — guarded by a
  test): provenance-colored stage flow, the 13-identity reconciliation panel, boundary map,
  cost-to-serve ledger, slotting bars, CVRP-vs-Clarke-Wright per-day SVG chart;
  `deliverables/chain_report.pdf` + `chain_ledger.xlsx`, regenerated **byte-identically** from
  the committed run artifact `artifacts/full_run.json` (sha256 code-fingerprinted; consumers
  flag it STALE if the code drifts).
- **Use case:** proving the chain closes — that the forecast, the warehouse and the cost
  ledger all run on the *same* numbers — which is the integration failure mode real
  distributors actually have.
- **Open improvements (its own framing):** (1) stages 4–5 run on a stated representative
  8-week window, not all 104 weeks (the per-day CVRP stage is slow — the full run is ~51
  minutes); (2) the physical layers (geometry, coordinates, rates) are synthetic-assigned by
  design, so the cost side stands on labelled invented inputs and stays a cost-structure
  view, never a margin statement.

## 22. chain-mcp — Automation (Job #1, agentic integration)

- **What it is:** the agentic-integration layer over the portfolio — a standard-conformant
  **MCP server** (official `mcp` Python SDK, FastMCP wiring, JSON-RPC over stdio) exposing
  six real engines as tools an AI assistant (Claude Desktop, Claude Code, any MCP client) can
  call mid-conversation: `forecast_demand` (decision-chain), `optimize_slotting` and
  `pack_cartons` (logistics-digital-twin), `route_deliveries` (route-optimizer),
  `analyze_discount_leakage` (sales-kpi-analytics), `portfolio_status` (portfolio-ops).
- **Measured results:** **116 tests — tool calls, an input-validation matrix, a live JSON-RPC
  handshake, and contract validation**; every tool validates input and returns structured
  error results on any failure (bad input, missing source repo, engine error) — the server
  never crashes on a tool call; source repos are imported read-only with env-overridable
  paths. A machine-checked contract layer introspects the six served tools and asserts that
  the registry, the implementations and the published catalog stay in agreement, that every
  served `inputSchema` is a valid JSON Schema, and that a sample request/response
  round-trips against the real served contract.
- **Visualizations:** none of its own — the deliverable is the protocol integration; ships
  ready-to-paste configs for Claude Desktop (`claude_desktop_config.json`) and Claude Code
  (`claude mcp add chain-mcp -- python -m chainmcp`), six example prompts, and a
  deterministic `deliverables/tool_catalog.md` emitted by the contract layer.
- **Use case:** the integration work "agentic AI" projects consist of in practice — wiring a
  language model to real, non-trivial computational engines with honest schemas, provenance
  labels and graceful failure.
- **Honesty labels (its own framing):** five tools state via a per-result `data_note` that
  they run on their repos' deterministic synthetic seeded datasets — real solver outputs on
  fabricated inputs; `forecast_demand` runs the real UCI Online Retail II pipeline (history
  `real`, forecasts `derived`), and if naive wins a demand class, naive is what gets
  reported. Limitations stated: local sibling checkouts only, stdio single-user, first
  forecast call ~10 s.
