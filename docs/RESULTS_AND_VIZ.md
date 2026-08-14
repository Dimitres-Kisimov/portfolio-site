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
  ranges on synthetic data, not a forecast. A robustness gate turns the band into per-move
  decisions: it replays the **same** fixed-seed draws (test-pinned to the simulator's
  per-draw totals) and gates each of the 29 recommended price moves on carry ≥90%,
  same-move ≥80% and a positive € at the P10 when executing the published price —
  verdict **17 ACCEPT (€19,032/yr at baseline) / 12 HOLD (€16,187/yr parked)**, and the
  single biggest move (+15% on S0006, €15,836/yr, 45% of the pricing uplift) is **held**
  because the SKU survives the assortment re-optimization in only **67% of draws**. A
  screening discipline under illustrative planning ranges, not a guarantee. A **scenario
  compare** then puts two plans side by side and reconciles the difference rather than
  reporting it: both are solved through the same `scenario.solve_plan` core (no second
  model, no re-derived perturbation) and the **€ bridge attributes every euro to a named
  driver**, summed in *integer cents* so it reconciles by construction rather than to a
  tolerance. Baseline **€159,966.19** vs *Cost inflation +8%* **€139,487.29** closes with a
  **residual of exactly €0.00** — and the single −€20,479 delta hides both halves of the
  story: pricing *gains* **€7,382.88** from changed conditions at frozen prices (+€5.40 of
  actual price action, −€264.96 of assortment mix), promo response loses **€3,707.02** on
  the carried set, and the **MILP-vs-greedy assortment gap loses €23,895.20**. Honest about
  its own construction: two of the drivers are **ordered**, so splitting a shared SKU's Δ
  into "the world moved" and "we moved the price" is a sequential attribution — it closes to
  the cent, but a different order would hand the interaction term to the other driver — and
  the assortment gap moves as **one** line because a difference of two optimization
  objectives over different subsets genuinely does not decompose per SKU (shipped whole
  rather than split into invented per-SKU drivers). Illustrative planning ranges on
  synthetic data: what the model computes under each assumption, not a forecast. 91 tests.
- **Visualizations:** `docs/img/uplift_waterfall.png` (baseline→optimized waterfall);
  `deliverables/sensitivity_tornado.svg` + `.csv` (driver tornado);
  `deliverables/uplift_distribution.svg` + `uplift_simulation.csv` (Monte-Carlo band);
  `deliverables/price_move_robustness.svg` + `.csv` (per-move accept/hold gate);
  `deliverables/plan_compare_summary.csv`, `plan_compare_bridge.csv` (anchor rows included,
  so the file itself proves the identity closes), `plan_compare_lines.csv` and
  `plan_compare.svg` (the A/B € bridge), fed to the dashboard's compare panel by
  `web/compare.js`;
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
  make about one year in five. Rep performance is a **fair comparison via indirect
  standardization**: each rep's gap vs an even-share baseline (a stated choice, not a
  quota) decomposes into coverage + frequency + mix + execution, **summing to the gap
  exactly** — Berg, #2 by raw revenue and the leakage table's top offender, has an
  **execution index of 0.9999** (his +€337k gap is the Nordics book, not the selling),
  and across all 12 reps **92% of the league-table dispersion is territory, only 8%
  execution**; the chart's per-rep labels are read back off the SVG and asserted equal to
  the source to the cent. Honest that this synthetic data assigns orders at random, so
  indices *should* cluster near 1.00 — on real data a persistent gap would be the
  coaching signal. **Customer concentration & dependency risk** is measured with
  arithmetic rather than prediction, and the company-level answer is the trap: over the
  trailing 12 months the book scores **Gini 0.5476** and **HHI 68** — ~**148 effective
  accounts out of 383**, the top 10 billing just **15.4%**, and **156 accounts (41%)**
  needed to make 80% — which reads *unconcentrated* and, taken alone, would be reassuring
  and wrong. Inside a territory it is not calm: the largest account (**C0393, €395,740.85,
  3.51% of revenue**) is **35.76% of one rep's own book**, whose **HHI is 2,064** with a
  top-3 of **64.10%** and **4.8 effective accounts**. Every "what if we lost them" figure
  is **removal arithmetic on measured revenue** — no churn probability is modelled
  anywhere, the first cut of the module was fixed by *dropping* a wrong "churned /
  dormant" label off a still-ordering account rather than softening it, and a test asserts
  no churn or RFM key can reappear; the HHI bands are the DOJ–FTC merger-guideline cuts
  borrowed as a yardstick — an analogy, not a regulatory reading.
- **Visualizations:** `deliverables/forecast.png` (revenue history + 3-month forecast);
  `deliverables/pacing_bullet.svg` (pacing bullet chart, euro labels asserted equal to the
  computed figures); `deliverables/rep_performance.svg` + `.csv` (diverging stacked
  decomposition, TOTAL row ties out); `deliverables/executive_review.pdf` (8-slide EBR) and `.pptx`;
  `deliverables/kpi_workbook.xlsx`; `deliverables/reorder_list.csv`;
  `deliverables/customer_concentration.csv` + `.svg` + `.png` (the Lorenz/concentration
  view, TOTAL row tying out) and §12 of `deliverables/management_report.md`; offline
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
  with the 25%/yr carrying rate and €50 order cost stated as planning assumptions. A
  **supplier-reliability scorecard** measures the seeded PO receipt history (10 suppliers,
  2,400 receipts, **74.3% on-time** at a stated 2-day grace window) instead of trusting
  the vendor master: re-pricing safety stock on measured lead times at the same service
  targets raises it **€16,282 → €18,626 (+€2,344, +14.4%)**, split *exactly* into a delay
  effect (€576) and a variability effect (€1,768) — **variability, not lateness, is three
  quarters of the bill**, and one supplier that delivers early on average (−0.4 days)
  still costs €542. The quoted-basis column reproduces `dip.inventory`'s safety stock to
  the cent (test-asserted); the layer is labelled a working-capital consequence on
  synthetic receipts, deliberately kept out of the €136,972 uplift total. A **plan-diff
  station** answers the question that follows every re-run — *what changed since last
  time, and why?* — by diffing two full plan runs into a **€ bridge in which every euro is
  attributed to a named cause**, held up by **11 change identities**. On the shipped
  default pair the headline moves **€136,972.20 → €115,728.86**, and the single
  **−€21,243.34** delta hides the actual story: price moves **−€29,931.98** (184 of 200
  recommendations moved), SKUs dropped **−€150,919.35** (21 left the range) against
  greedy-baseline re-picks of **+€150,224.01**, routing **+€9,384.00** (32.64 km/run saved
  at €1.15/km × 250), and a publication-rounding line of **−€0.02 against a €4.03 bound
  over 806 values**. The rounding line is real, not a plug — never fitted to close the gap,
  and mis-attributing a single SKU stops the bridge closing; the inventory diff is
  deliberately kept *out* of the uplift bridge, so a pair that changes only the
  replenishment knobs correctly posts a **€0 uplift delta** (tested); and the assortment
  lever gets its own line precisely because it moves against intuition, instead of being
  netted into a small number with no explanation. **The bridge is an identity, not an
  illustration.**
- **Visualizations:** executive PDF (`deliverables/executive_review.pdf`) + Excel; a hand-built
  command-center dashboard (`templates/`, `static/`); the inventory policy served via
  `GET /api/inventory` (per-SKU rows + a nine-cell ABC-XYZ roll-up); supplier scorecards +
  the safety-stock consequence served via `GET /api/reliability`; the plan diff served via
  `GET` / `POST /api/plan-diff` and surfaced as station **ST-07 · Change** on the dashboard
  (API + UI only — this layer writes no file artifact); screenshot slots in `docs/img/`.
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
  CLV is labelled gross revenue, not profit. **Lifecycle stage segmentation** is the
  operational view: every identified customer gets one stage per calendar month
  (new / retained / resurrected / at-risk / dormant) and the month-to-month movements
  form a flow matrix whose structural zeros the test suite asserts. Measured over 24
  complete months (5,824 customers): the average month has **1,041 active buyers = 212
  new + 390 retained + 439 resurrected** — **resurrections outnumber month-over-month
  repeats (439 vs 390)**, quick ratio 1.05; **31.2%** of identified-customer revenue in
  complete months comes from resurrected buyer-months, and dormant customers still return
  at **8.9% per month** — for a wholesale-heavy base, skipping months is normal
  purchasing behaviour, and stage definitions are labelled definitional choices, a lens,
  not a behavioural truth. The honest headline stays up front:
  **seasonal-naive wins the forecasting bake-off** (mean MASE 1.094 vs 1.187 for
  Holt-Winters); **22.77% of rows have no CustomerID** and are flagged rather than
  dropped; the data-quality report card (raw C → cleaned A) is labelled a heuristic
  scorecard with stated weights, not a certification of data correctness. **Price ladders**
  take the same discipline into pricing: `Price` here is not a property of a product but of
  a *line* — **4,342 of 4,895 SKUs (88.7%) sold at more than one price** — so the ladder is
  measured before anything is said. On the cohort with ≥ 4 distinct prices and ≥ 200
  invoice lines (**1,342 SKUs carrying 79.7% of revenue, GBP 15,653,663**; median **6
  rungs**, p90/p10 spread **2.00×**), **39.5% of units sold below the posted price, 51.5%
  at it, 9.0% above**, and **price realization is 98.6% — reported as a fact, not an
  opportunity** (the GBP 216,608 gap is 1.4%). Two independent log-log slopes are kept
  apart on purpose: **within-week −1.71** (measured on variation containing *no price
  change at all* — the discount schedule alone) and **posted price week to week −1.78**,
  **market-adjusted −1.67**, with **96.0%** of market-adjusted slopes negative and **825 of
  1,113 SKUs (74.1%)** beating their own **199-draw permutation null at p ≤ 0.05** (553
  single-price SKUs excluded). What the slopes do *not* license is the headline: read
  **−1.0 as the benchmark, not zero** — a buyer who spends the same amount per line
  whatever the price produces exactly −1 with no demand response — the two measurements
  correlate at only **r = 0.20** per SKU, and prices were never randomised, with no cost,
  competitor or stock data, so **nothing here is an elasticity and nothing here is
  causal**: an assortment-level statement, not a per-SKU price recommendation. 113 tests.
- **Visualizations:** `deliverables/retail_analytics_executive.pdf`;
  `deliverables/retail_analytics.xlsx` (sheets CleaningReport → DataQuality, incl. a
  Lifecycle sheet);
  `deliverables/cohort_retention.csv`, `customer_lifetime_value.csv`,
  `returns_analysis.csv`, `lifecycle_stages.csv`, `lifecycle_flows.csv`,
  `price_ladder.csv` (the full per-SKU ladder with both slopes and the permutation
  p-value) and the workbook's `PriceLadder` sheet, `data_quality_report_card.md`;
  `figures/` chart set (`monthly_revenue.png`, `cohort_retention.svg`,
  `clv_validation.png`, `returns_analysis.png`, `lifecycle_stages.svg`,
  `price_ladder.png`, and more).
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
  and the communities mirror the three k-means segments found independently. **Rule
  redundancy pruning** (confidence improvement, Bayardo, Agrawal & Gunopulos 1999; itemsets
  classified closed/maximal per Pasquier 1999 / Bayardo 1998): **105 of the 254 rules
  (41%) are redundant and the remaining 149 carry all of the list's information** — every
  pruned rule is covered by a simpler rule at equal-or-higher confidence, and a test
  asserts the covering rule is itself in the kept set, so pruning loses nothing; the
  flagship planted bundle survives with a **+16.0 pp** improvement margin, and of the 224
  itemsets **224 are closed and 126 maximal**. Redundancy is labelled information
  content, not causality or effect size. 68 tests.
- **Visualizations:** `deliverables/cross_sell_briefing.pdf` (rules table,
  lift heatmap, redundancy page, affinity communities, segments, stability, back-test);
  `deliverables/market_basket_analysis.xlsx` (8 sheets incl. Redundancy); hand-drawn
  SVG + CSV pairs: `rule_stability`, `recommender_backtest`, `affinity_network`,
  `rule_redundancy` (every rule's verdict, with the covering rule named per row).
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
  scenarios to **44%** — the cheapest expected day in the sweep. A heterogeneous **Fleet
  Size and Mix** layer (the FSM VRP of Golden, Assad, Levy & Gheysens, 1984) hands the same
  engine a typed pool of candidate vans — per-vehicle capacities, EUR/km and a fixed cost
  per deployed van — so the objective is money, not kilometres: on n60 **consolidation wins
  outright** — 5 large vans (EUR 1,325/day) undercut the status-quo 10 mediums (EUR 1,606)
  by **17.5%** (distance −35.6%, CO2 −14.9%) at the stated service price of a **+25.2%**
  longest route; on n30 the mix is genuine — **1 medium + 2 large** (EUR 628/day) beats the
  best single-size fleet (all-large, EUR 686) by **8.5%** and the status quo by 14.7%. The
  catalogue costs are illustrative labelled estimates, not certified rates; every plan is a
  heuristic under a fixed search budget (byte-identical reruns), and the deliverable reports
  whatever the numbers say — on n60 the mixed pool simply agrees with the all-large answer
  (+0.0%). A **driver shifts & working-time** layer then models the day as three kinds of
  minute — driving (distance × 60 / speed), service at the kerb, and breaks — under a
  **600-min duty envelope**, a **540-min daily driving limit** and a mandated **45-min
  break before 270 min** of continuous driving, at 40 km/h and 5 min per stop. **The
  statutory limits are slack on this data, and the deliverable says so**: audited on the
  shift-blind savings plan the worst duty is **267 min (4h27)** across 10 vans — **333 min
  of headroom** — the worst continuous drive is **227 min** against the 270-min threshold
  (**43 min of slack**), **zero breaks** are required, and **10/10 vans** clear both
  limits. The cap sweep shows where the constraint would start to cost (uncapped reference
  1,001.6 km on 10 vans): **480 and 420 min cost nothing at all**, 360 → 1,010.3 km, 300 →
  1,014.3 km, **240 min costs +5.3% distance**, **210 min costs +17.5% and an eleventh
  van**, and at **180 min there is no plan at any fleet size** — a *proof*, not a search
  that gave up. The defaults are **informed by EU Regulation (EC) No 561/2006 as a
  modelling choice, not an implementation and not a compliance certification**: a real duty
  would be longer than every number reported, every capped plan is a heuristic under a
  fixed search budget (so the distance curve need not be monotone in the cap), and nothing
  here should be used to judge whether a real roster is legal. 74 tests.
- **Visualizations:** `deliverables/routes.png` (OR-Tools routes on the 60-customer instance);
  `deliverables/route_plan.csv`; `deliverables/summary.md`; `deliverables/robustness.svg` +
  `.csv` + `.md` (the scenario sweep); `deliverables/fleet_mix.svg` + `.csv` + `.md` (the
  mixed-vs-homogeneous fleet comparison); `deliverables/driver_shifts.svg` + `.csv` + `.md`
  (the duty audit and the cap sweep); `web/index.html` interactive Canvas map with a
  savings-heuristic overlay toggle and light/dark.
- **Use case:** the last-mile delivery plan a distributor builds every morning — now with the
  buffer question ("how much headroom is worth paying for?") answered with a measured sweep,
  and the van-catalogue question priced in money rather than kilometres.
- **Open improvements:** (1) Euclidean distance, not road-network — add an OSRM/Valhalla
  matrix; (2) single depot still — time windows are modelled (the VRPTW / service-level
  layer, on synthetic windows and a fixed per-stop service time), the fleet can be
  heterogeneous (illustrative catalogue costs, not quotes), and driver duty / working time
  is now modelled too (informed by EU 561/2006, not an implementation of it); multi-depot
  and variable service times are the next constraints, and OR-Tools supports both.

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
  worst single outage drops service to 59.6% and costs $157,016 to restore. The
  **demand-growth capacity plan** sweeps a uniform multiplier (1.00x → 2.00x in 5% steps)
  and re-solves the same facility MILP twice per level (unconstrained vs today's three
  DCs pinned open): the lean network has only **+8.8% growth headroom** (capacity wall at
  exactly 1.088x — 19,451 units of capacity vs 17,880 of demand), the first response to
  growth is a **reshuffle, not a new DC** (at 1.10x the optimizer swaps DC6 for DC0 and
  stays at three), and the **4th DC first pays at 1.30x** — exactly when any 3-DC design
  physically caps out (the three largest candidates hold 1.29x) — with the 5th at 1.65x
  and the 6th at 1.95x as an economic trigger; growth is modelled as uniform, and the
  expansion triggers are planning estimates on synthetic data, not forecasts. A **phased
  build plan** finally puts a calendar and a discount rate on that staircase: demand grows
  at an **assumed 6%/yr** and every year is priced by re-solving the **same** facility MILP,
  with policy continuity expressed through the same `force_open` / `force_closed` pins the
  resilience and growth modules already use. Over 10 years at an **assumed 10% discount
  rate**, staging the build costs **$2,750,462 NPV** — open **DC0 in year 2, DC3 in year
  6**, ending on **5 DCs** — against a **$2,598,732** free-redesign lower bound (7 site
  closures, and it closes live DCs at zero cost, which is why it is a *bound*);
  **building ahead costs $671,597 more (+24.4%)**, **never closing a site costs $151,730
  (+5.8%)**, and doing nothing **fails in year 2**, when demand reaches 1.124x and clears
  the 1.088x wall (by year 9 demand is 1.69x against a 2.74x candidate-pool and 2.10x plant
  ceiling). Test-asserted orderings: free ≤ staged ≤ build-ahead, and staged ≤ frozen. The
  growth and discount rates are **illustrative assumptions, not forecasts**; fixed cost is
  modelled as a **recurring per-period operating cost, not one-time capex**, a DC opens with
  **no construction lead time**, and costs are charged at the start of each year — so the
  build-ahead premium is the price of readiness rather than a finding that early building is
  wrong, and a model carrying capex or land escalation could reverse the sign. 71 tests.
- **Visualizations:** executive PDF (cover with disclaimer, network map of opened DCs and
  flows, cost-breakdown bar, pooling chart, cost-vs-CO2 Pareto page, resilience page,
  service-frontier page, two-panel growth page, plate 09 for the build schedule) + Excel
  workbook (Summary → Assignment, incl. Growth and BuildSchedule sheets);
  `deliverables/co2_cost_frontier.svg` + `co2_sensitivity.csv`;
  `deliverables/service_frontier.svg` + `.csv`; `deliverables/growth_expansion.svg` +
  `growth_plan.csv`; `deliverables/build_schedule.svg` + `.csv` (all SVGs hand-drawn; the
  `deliverables/` tree is generated rather than committed).
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
  an order-of-magnitude planning model, not a bill. A seeded reliability benchmark
  (`eval/reliability.py`) re-runs the flows over the same 9 fixtures while injecting
  model-level faults (wrong SKU, dropped line item, premature answer, stuck loop,
  hallucinated tool, skipped validation) on a seeded schedule — 50 trials per task across
  three tiers, **1,350 trials**, each classified into a four-way taxonomy: success /
  recovered / detected failure / silent failure. At the anchor tier (a 30% **assumed**
  fault rate): **76.8% success, 13.6% detected, 9.6% silent** — the guards catch the
  control-flow faults (a hallucinated tool call is even converted into a recovery) while
  content faults sail through looking plausible. The retry economics quantify the
  consequence: at 2 retries the anchor tier delivers **88.7% correct for ~$843/yr** in
  tokens at the business-case volume — but **~11,500 silent-wrong quotes a year**, the
  quantified argument for the "a rep still reviews every draft" model. Per-tier fault
  rates are assumed scenario parameters, not measured properties of any real model.
  A content-verification layer (`src/agentic_lab/verification.py` + `eval/verification.py`)
  is the direct countermeasure: it **independently recomputes the business outcome from the
  source input** with deterministic tools (re-parse the email, re-resolve every line against
  the catalog, re-run the enrichment pipeline) and cross-checks what the run delivered —
  trusting the tools, distrusting the model. Replaying the reliability benchmark's **exact
  fault schedule** (the "without" arm reproduces the reliability numbers verbatim, asserted
  in tests), every injected content fault becomes detectable: at the anchor tier with 2
  retries, delivered-correct **88.7% → 98.8%** and silent-wrong quotes **11,523/yr → 0**,
  at a visible price — human escalations 260 → 1,300/yr, tokens ~$843 → ~$939/yr — with
  0 false alarms on clean runs. A property of this fault schedule and this task's
  recomputable ground truth, **not a production guarantee**; the verifier checks the
  structured payload, never the prose — a blind spot that is unit-tested rather than
  hidden. **Human-in-the-loop checkpoints** are then priced *per placement* rather than
  argued: the agent stops at a gate and hands out a **resumable, digest-stamped JSON
  envelope** of its own run (transcript, tool state, counters, guard trace, pending calls),
  and `Agent.resume()` continues from it — nothing is re-sent to the model and no tool runs
  twice, so **an approved gate costs 0 extra tokens**, where restarting instead of resuming
  would multiply attempt cost **7.90×**. Five placements, same fault schedule, anchor tier,
  ~104,000 RFQs/yr, labour at €45/h: **no gate** leaves **11,523 silent-wrong quotes/yr**
  (€780 labour); **risk-gated** review — only the runs where guards and verifier disagree —
  takes that to **0** for **28,349 reviews, 1.24 FTE, €88,948/yr = €7.65 per prevented
  error**; **pre-commit** €177,205/yr (€15.31); **pre-delivery** €188,438/yr (€16.29); and
  **approving every step** €349,708/yr (€30.28) — which **buys nothing extra on this
  schedule**. Placement also decides what is caught at all: a *skipped validation* is
  missed at `pre_commit` and at `every_step`, but caught at `pre_delivery` and
  `risk_gated`. The reviewer is **modelled, and modelled generously** — an ideal one, so
  every catch rate is an **upper bound** and the 0 false alarms say nothing about people;
  review times are assumed scenario parameters except the business case's own 2-minute
  draft review; there is **no queue model**; and labour in EUR sits beside tokens in USD,
  **reported side by side, never summed**. 100 tests.
- **Visualizations:** `benchmarks/results/scorecard.png` (nine-dimension comparison);
  `benchmarks/results/scorecard.md`; `eval/cost_scorecard.md` (+ `.json`/`.csv`, byte-stable);
  `eval/reliability_scorecard.md` (+ `.json`/`.csv`, byte-stable);
  `eval/verification_scorecard.md` (+ `.json`/`.csv`, byte-stable);
  `eval/checkpoint_scorecard.md` (+ `.csv` / `checkpoint_results.json`) — the five
  placements costed per prevented error, per tier;
  `deliverables/executive_onepager.pdf`; agent trace output.
- **Use case:** deciding low-code vs full-code (vs hybrid) for an agentic automation, with the
  trade-off measured rather than asserted — and the model bill estimated before anyone runs it.
- **Open improvements:** (1) a parallel n8n run over the same emails to put measured latency +
  cost beside the Python path; (2) more than one catalog/domain before generalizing the ranking.

## 9. agent-flow-studio — Automation (Job #1)

- **What it is:** a tiny in-browser visual agent-workflow builder — drag nodes, wire ports,
  Run, and watch a mock agent walk the graph and pick tools. No backend, no build step.
- **Measured results:** covered by **78 tests** (engine logic, undo history, snapshot
  rendering, flow linter, dependency analyzer, cost estimator — pure logic; the same
  `engine.js` runs in the browser and under `node --test`); real topological sort (Kahn's
  algorithm) with cycle detection; five node types. A static data-dependency / provenance
  analyzer (`analysis.js`) computes each node's upstream/downstream closure, the
  parallelisable stages, the critical path and which Trigger's payload can reach every
  Output — honest that it describes the data flow the wiring permits, not the single path
  one input takes, and it withholds the order-dependent fields when the graph is not a DAG.
  A **dry-run cost/latency estimator** (`estimator.js`, behind the € Estimate button)
  prices a *designed* flow before it runs against a declared rate card: per-node
  tokens/€/ms, an agent call's prompt as a declared base plus a declared amount per
  toolbelt entry (fatter toolbelts visibly cost more), both latencies — the sequential sum
  this engine takes and the weighted critical path a parallel executor could reach — and,
  because a Condition takes one branch per run, enumerated branch scenarios whose executed
  sets the tests prove against real engine runs branch-for-branch. Emphatically **not a
  bill**: the rates are illustrative inputs you edit, the shipped agent is a free
  deterministic mock, nothing is measured, and a cyclic flow gets its estimate withheld,
  not invented — the committed `docs/FLOW_COST_REPORT.md` regenerates byte-for-byte and is
  stale-checked in CI. Business model estimates **~€47k/yr** of engineering time freed by
  letting business users assemble simple flows themselves.
- **Visualizations:** the live canvas itself (hand-drawn SVG wires, node highlighting, live
  wire animation, streamed trace); two example flows in `examples/` (RFQ triage, ticket router);
  `docs/FLOW_COST_REPORT.md` (the declared rate card and each flow's tokens, € per run per
  model profile, branch-scenario range and per-node table);
  `deliverables/executive_onepager.pdf`.
- **Use case:** understanding a low-code agent canvas "from the inside."
- **Open improvements:** (1) a real provider behind the agent node (keep the mock as default);
  (2) no retries/timeouts/parallel branches/sub-flows/loops yet — flows must be acyclic.

## 10. doc-extract-agent — Automation (Job #1)

- **What it is:** unstructured business document in, structured record out — a six-stage
  pipeline (detect → header → line_items → totals → confidence → validate) with a
  confidence gate and a business-rule validation layer.
- **Measured results:** takes per-document handling from **~4 minutes to under 1 second**;
  models a ~60,000-document/yr AP scenario freeing **~€110k/yr** of capacity; totals
  cross-checked against summed line items. Only documents that reconcile, clear the
  confidence gate and pass the business rules post automatically — requiring the rules as
  well as the gate lifts measured auto-post precision from **70% to 87.5%**, and the README
  says plainly that 87.5% is not 100%, naming the multicurrency case it still misses. An
  **extraction-error cost model** (`python -m eval.run_cost`) joins the measured operating
  point of every gating policy with the business case's modelled rates (€0.40 pre-filled
  review, €25 per silent error): **the confidence gate alone would lose money on this set**
  (€181,778/yr modelled vs €173,000 manual — silent errors outweigh the skipped reviews),
  **the business-rule validation layer is worth ≈€109,333/yr in this model** (the entire
  gap between gate-only and gate + validation, the euro version of the 70% → 87.5% lift),
  and **auto-posting pays only above 98.4% precision** (break-even at 1 − 0.40/25) — a
  bar no measured policy clears credibly. Measured operating points, modelled prices. Two
  parsing bugs (VAT 19.95 vs 19; Subtotal read as Total) pinned by regression tests; EU
  (`1.234,56`) and US (`1,234.56`) number parsing. **Side-by-side original ↔ extracted with
  real source spans**: hit Extract and the left column becomes the document you submitted,
  rendered as a **line-numbered sheet with every value the engine read underlined where it
  was read**. That is real provenance rather than the UI re-searching the text for
  something that looks like the answer — each extractor records the span of the match that
  produced its value (`{"start": 177, "end": 190, "line": 12, "col": 17, "text":
  "INV-2026-8842"}`), and the counter states coverage plainly: **25 of 26 extracted values
  located in this document · 1 derived (no span)**. A computed value **has no span and says
  so**; a span that does not match is reported as **not located** rather than drawn
  somewhere plausible; and a span is the **source evidence, not a copy of the value**, so a
  `1.234,56` span carries those characters while the caption reads *→ read as 1234.56*.
  Across **all 30 committed documents** (3 samples + the 27-document eval set) every span
  must satisfy `text[start:end] == span["text"]`. Honest scope: the sheet is the plain text
  you submitted — there is no PDF or scan rendering behind it, so **a span is a character
  range, never a pixel region on an image**.
- **Visualizations:** the web UI trace view (per-stage events, confidence scores) served by
  `python -m docextract.server`, now with the line-numbered source sheet and its underlined
  spans (they ride inside the existing `/extract` payload — no second route, no second
  pass); JSON/CSV exports; the per-policy cost table in
  `eval/cost_results.json`; `deliverables/executive_onepager.pdf`.
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
  conventional methods on narrow tasks. Two experiment tracks: expand-and-sparsify hashing
  (FlyHash, plus a learned BioHash variant) and a liquid CfC cell vs a GRU.
- **Measured results (public MNIST + synthetic signal, 3 seeds):** **FlyHash precision@10** at
  4/16/64/128 bits = 0.152 / 0.352 / 0.552 / **0.614** vs classical LSH 0.017 / 0.093 / 0.309 /
  0.419 — FlyHash wins at every budget. **BioHash (learned synapses, Ryali et al. 2020)**,
  trained with the local Krotov–Hopfield plasticity rule — no labels, no backprop — at a
  deliberately resource-hostile operating point: a **10× smaller circuit** (1,568 vs 15,680
  units) whose dense learned projection under-spends FlyHash's sparse random one (1,229,312
  vs 1,473,920 MACs/query). Learning wins the benchmark's mid-range at a discount
  (equal-or-better at 8–128 bits, **0.626 vs 0.614** at 128 bits) — and the negatives are
  reported with it: both tips of the grid go back to the wider random code space, the memory
  frontier is never reached, training costs a one-time ~1.62 × 10¹² MACs per seed, a learned
  hash is data-dependent, and the reference N(0,1) init is load-bearing (the paper documents
  that a unit-norm init measurably collapses training onto <8% of units). **Liquid CfC**
  cell: 3,233 params vs GRU 3,393; clean
  MSE 0.0142 vs 0.0147; MSE @ σ=0.4 noise 0.162 vs 0.168 (equal-or-lower at every noise level
  under noise-trained protocol; honest that clean-only training flips the robustness edge).
- **Visualizations:** the FlyHash precision-vs-bits plot (regenerated by
  `experiments/bench_flyhash.py`); the BioHash learned-vs-random grid
  (`experiments/results/biohash_mnist.csv` / `.svg`, by `experiments/biohash_mnist.py`);
  `liquid_robustness.png` (by `experiments/bench_liquid.py`);
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
  An **ablation study** (`mllab/ablation.py` → `docs/ABLATION.md`, machine-generated — no
  numbers typed by hand) retrains the same two numpy models with each claimed improvement
  knocked out and commits the exact deltas: **8 of 9 knockouts hurt the primary metric** —
  dropping the engineered `freq_slope` costs the churn model **−0.247 PR-AUC** (0.653 →
  0.406), dropping the demand-shock control costs the elasticity model **+1.446 RMSE**
  (0.129 → 1.575), and the everything-removed variant *is* the leaderboard's naive-OLS fair
  baseline. The honest exception: removing Platt calibration leaves PR-AUC **bit-identical**
  (a positive-slope monotone rescaling cannot change a ranking metric) while ECE collapses
  0.021 → 0.197 — exactly why the model reports both numbers; the two knockouts inside the
  bootstrap-CI noise band are reported as within evaluation noise, not counted as wins, and
  `tests/test_ablation.py` retrains every variant so the committed table cannot drift.
- **Visualizations:** per-model confusion matrix, reliability curve, PR curve, and
  elasticity/profit plots (produced by each model's training script); `docs/METHODOLOGY.md`;
  `docs/ABLATION.md` (the machine-generated knockout-delta table).
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
  At the default 5%-FPR alert threshold condition-based maintenance loses — so the loop
  is closed: an **exact sweep re-prices the CBM policy at every candidate alert
  threshold** (timeliness and false alarms re-measured per threshold, costed with the
  same Weibull MTBF), and at the policy-optimal threshold (**0.262 → 0.397**) all six
  observed failures stay alerted ≥ 3 days early while false alarms collapse **44 → 3** —
  the CBM cost rate falls **8.28 → 4.02 per machine-day, under the age-replacement
  optimum's 7.16**, and the **ranking flips to condition-based**, with a closed-form
  **break-even inspection cost of 553.3 units** (~11x the assumed 50). Honest that the
  rates are illustrative and the tuned threshold is selected on the same held-out
  machine-days it is priced on — the shape of the closed loop, not a certified operating
  point. The same fit now prices the **storeroom**, which is the bill nobody quotes: every
  policy is a renewal process consuming one part per cycle, so the Weibull (**β 4.81, η
  73.6 d, MTBF 67.4 d**, 6 failures + 14 suspensions) gives each policy's part-demand rate
  and a **Poisson base stock** says what 20 machines must hold over 365 days at **95%
  service**. Run-to-failure and condition-based draw **0.0148 parts/machine-day** (108.3
  expected, **base stock 126**, 18 safety); **age replacement at T\* = 44.4 d** shortens the
  cycle to 43.8 d and draws **0.0229** (166.8 expected, **base stock 188**, 21 safety) — the
  calendar policy cuts the cost rate 51.7% but pulls **+54% more parts**. The Poisson
  assumption is checked rather than assumed away: measured cycle CV is **0.24** and
  **0.07**, both well under the 1.00 Poisson implies, and a renewal-variance alternative
  would hold **112 / 168** instead — so the base stock is deliberately conservative. **A
  modelled provisioning exercise, not an order**: no replenishment lead time, no batching,
  no repairable-part loop, and it counts units, not money (the file header says so:
  *"SYNTHETIC data; part demand is MODELLED from a censored Weibull fit, not measured"*).
  80 tests.
- **Visualizations:** `deliverables/pdm_report.pdf` (cover with disclaimer, PR curves, health
  ranking, before/after Gantt) and `deliverables/pdm_workbook.xlsx` (Machines, Alerts,
  HealthIndex, Schedule, Comparison sheets); `docs/cbm_tuning.svg` + `.csv` (the swept
  cost curve against both benchmarks); `docs/spares_plan.svg` + `.csv` (the per-policy
  part-demand rate and Poisson base stock, regenerated by `python -m pdm --spares-out docs`).
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
  the measured verdict is **PROMOTE**. A **feedback-loop simulation** (`python -m fdo
  --feedback`) prices the **selective-labels problem** (Lakkaraju et al. 2017): analysts
  confirm labels only on the alerts they review, so four labelling-policy arms deploy
  over three rounds with a frozen threshold and retrain on their own decisions. The
  measured mechanism is not the folklore one — **ranking survives (final PR-AUC spans
  just 0.268–0.273 across arms)** because the clean initial history anchors it, but the
  **probabilities die**: retraining with 292 frauds relabelled as legitimate drags the
  poisoned arm's test **ECE to 0.0100, 3.2x the oracle arm's 0.0031**, and starves its
  alert volume 651 → 197 at the frozen threshold — while its own dashboard reads **100%
  observed recall every round, by construction** (true label coverage 23–35%): the model
  grades its own homework. A model of a process, not a measurement of one — review
  capacity and the 85% chargeback rate are labelled assumptions, and chargebacks land at
  the round boundary instead of 30–90 days late. **Reason codes** answer *why did this
  alert fire?* the way regulated lending answers it — a short list of **principal reasons**
  — and the decomposition is **exact rather than approximate**, which is the only reason it
  is worth shipping: the champion is linear in its standardized features, so fixing a
  reference profile (the mean training-window transaction, which scores **z(r) = −0.509**)
  makes the per-feature terms *the* Shapley values of the score under an interventional
  reference. The tests check that against **brute-force enumeration over all 2^m
  coalitions** (to 1e-12) instead of citing it, and the explained set is the **same 608
  alerts the shipped threshold fires**, never a re-derived one. Across those alerts
  `merchant_category` is the principal reason on **40.5%** but confirms fraud only
  **11.4%** of the time, while `transaction_amount` is principal on **19.1%** and confirms
  **20.7%** — **the most common reason is not the most predictive one** — and inside the
  100-review queue `transaction_amount` heads **59.0%** of rows at **33.0%** confirmed
  fraud. Removing just the single largest contribution drops **88.7%** of alerts back under
  the threshold (median 1, against **3.30** reasons listed per alert). Read honestly:
  contributions are **logits against a stated reference — not probabilities, not dollars,
  not causal**; change the reference and every number changes; a faithful account of the
  *score* can still be an incomplete account of the *fraud*; and the four-reason format is
  borrowed from ECOA / Regulation B adverse-action practice as a discipline — a fraud alert
  is not a credit denial, and nothing here is legal advice. 78 tests.
- **Visualizations:** executive PDF + Excel workbook via `python -m fdo --deliverables`
  (matplotlib PdfPages / openpyxl); reliability and cost-curve tables in the report;
  `figures/feedback_loop.csv` (the byte-deterministic per-round trajectory);
  `figures/reason_code_summary.csv` (the population table), `figures/reason_codes.csv` (the
  per-alert notice for the 100 queued reviews) and `figures/reason_codes.svg`.
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
  horizon. A **change-point degree-day decomposition** (the piecewise-linear model behind
  ASHRAE Guideline 14 and PRISM, with 168 hour-of-week means absorbing the two-shift
  schedule so production cannot masquerade as weather) recovers the generator's designed
  balance points exactly (**19.0 / 6.0 °C**) and the heating slope to the digit
  (3.20 kW/°C) — a recovery asserted by the test suite, the check a real meter could not
  offer without sub-metering — and finds weather-driven load is **4.5% of the year's
  energy** (68 MWh) yet **76 kW of the 412 kW July peak hour is chiller load (18%)**: in
  the worst month the battery is, to first order, shaving the weather; labelled a modelled
  attribution, not a sub-meter. **Battery sizing** then refuses to answer the procurement
  question from the bound: every candidate system is a *complete* causal backtest of the
  same deployable controller (weekly-refit forecast, month-anchored plan, meter-clamped
  execution — every rule unchanged) re-run against a different battery, power scaled at the
  default spec's 0.30 C. At an **ASSUMED linear EUR 375/kWh installed** — the midpoint of
  the EUR 120,000–180,000 range — break-even over a 15-year life is **EUR 25 per kWh-year**,
  and **only the smallest system on the grid clears it**: 100 kWh / 30 kW earns **EUR
  3,328/yr (77.0% capture), EUR 33.3 per kWh-year, an 11.3-year payback**, against 200 kWh
  EUR 5,121 (14.6 yr), the default 400 kWh EUR 8,066 (**18.6 yr**), 600 kWh EUR 9,939 (22.6
  yr) and 800 kWh EUR 12,579 (23.8 yr) — *"buying four times the battery buys 2.4x the
  saving and turns an 11-year payback into a 19-year one."* The awkward parts stay in: the
  600→800 kWh step (**EUR 13.2/kWh-yr**) is worth *more* than the 400→600 step (**EUR
  9.4**), so the curve is not concave; and it is an energy problem, not a power one —
  doubling the inverter to 240 kW buys **EUR 0/yr** while halving it to 60 kW costs **EUR
  824/yr**. Demand charge only (no arbitrage, no TOU stacking), simple undiscounted
  payback, no degradation or O&M — and the per-kWh price is **linear where real quotes are
  not**, a caveat the repo states precisely because it flatters the small systems its own
  table just recommended; five capacities and two inverter ratings, not a continuous
  optimum. 72 tests.
- **Visualizations:** `deliverables/energy_report.pdf` (6-page executive PDF with the
  per-fold table) and `deliverables/energy_workbook.xlsx` (4 sheets);
  `docs/temp_sensitivity.svg` + `.csv` (base load vs weather-driven load, monthly);
  `docs/battery_sizing.svg` + `.csv` (the capacity grid with causal capture, marginal value
  per kWh-year and payback, plus the inverter-rating probe).
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
  The alarm now ends in a **measured out-of-control action plan** (`qav/recalibration.py`):
  four responses to the camera-drift alarm — keep running, re-center the threshold on the
  unlabelled stream, re-fit on 200 recent verified-clean frames, repair the camera — each
  measured and costed at four drift levels (in control: 358 EUR per 1,000 parts).
  Re-centering is the trap the chart cannot see: it quiets the p-chart *by construction*
  while its ROC-AUC stays bit-identical to doing nothing — at +0.10 drift the "recovered"
  screen catches **1.1 of 15** defects behind an in-control-looking flag rate, a green
  chart over a blind screen — while re-fitting returns ROC-AUC to ~0.785 at every drift
  level and recovers **~99% of the drift-induced cost at +0.05 and beyond**; honest scope:
  the drift is a synthetic brightness stand-in, and the refit window is assumed
  verified-clean and free — verification labour and recalibration downtime are uncosted.
  **Severity grading** finally asks whether every escape costs the same: each defective
  part carries a **measured severity index** — the total absolute intensity its injection
  displaced (`sum |defective − clean|`, recorded at generation time, *no detector
  involved*) — cut at **8** and **15** into **minor 43 parts (29%) / major 72 (48%) /
  critical 35 (23%)** and priced at an illustrative **EUR 10 / 35 / 140**. Two findings,
  both reported: **grading changes the bill long before it changes the decision** — the
  recommended operating point does not move (**score ≥ 0.0217, 0.45% of parts pulled**)
  because the zero-false-reject cliff pins it, and a critical escape would have to be
  priced at **EUR 259 (7.4× the flat rate)** before the reject rate jumps to 1.83%; and
  **the expensive grade is the one the screen sees worst** (critical ROC-AUC **0.706** vs
  **0.819** for major and 0.746 for minor, because **22 of the 35 critical parts are
  texture-breaks**, the class nothing detects well). The bill rises **368 → 509 EUR per
  1,000 parts (+39%)**, **63%** of it from **2.3 critical escapes**; re-pricing the same
  grade *mix* to a mean of 35 EUR gives **340 EUR — 7% below** the flat model, so the rise
  is the shape of the mix, not its level. The cut points and the three prices are
  illustrative labelled constants, the grade mix is this generator's mix (a real line's
  comes from its own defect log), and the index is a synthetic-image proxy for "how much
  material the mark disturbs" — not a customer-severity model; what *is* measured is the
  index, every per-grade detection rate and every AUC.
  59 tests, two full runs bit-identical.
- **Visualizations:** `figures/gallery.png` (per-method heatmaps), `figures/roc_pr.png`,
  `figures/per_type_auc.png`; `figures/recalibration.svg` (the four responses costed per
  drift level); `figures/severity.svg` (the graded ledger under the same threshold sweep);
  `deliverables/qa_defect_report.pdf` (10-page) and
  `deliverables/qa_defect_metrics.xlsx` (incl. every raw score so the curves can be
  re-derived, plus Recalibration and Severity sheets; the `deliverables/` tree is
  generated rather than committed).
- **Use case:** a visual QA station deciding whether a deep model earns its keep over the
  boring methods before anyone ships a neural network — then watching the line for drift.
- **Open improvements (its own framing):** (1) the autoencoder is untuned — a better recipe
  might clear the 0.02 margin; (2) no lighting/perspective/focus variation, the classic real
  failure modes, by construction.

## 18. quantum-explainer — Teaching (live PWA)

- **What it is:** an installable, offline-first PWA that teaches one- and two-qubit quantum
  computing on a hand-written state-vector simulator (`sim.js`, ~550 lines, zero
  dependencies) — circuit playground, draggable Bloch sphere (reduced states in two-qubit
  mode), lessons including "What quantum computers are NOT", Deutsch's algorithm and
  superdense coding. Live at
  <https://dimitres-kisimov.github.io/quantum-explainer/>.
- **Measured results:** **201 physics/behaviour assertions** pass in plain Node (H|0⟩ gives
  50/50, H·H interference, Bell-state probabilities {00: 0.5, 11: 0.5} with a failing
  factorability check, RY(π) ≈ X up to global phase, norms stay 1 to 1e-10); the Deutsch
  lesson is checked for all four oracles — a single query yields the correct
  constant/balanced verdict with certainty, and the oracle leaves the state a product state
  (concurrence 0): phase kickback, not entanglement, even when the oracle is a CNOT.
  The superdense-coding lesson (two classical bits through one transmitted qubit, over a
  Bell pair shared in advance) is checked for all four encodings — Alice touches only her
  own qubit (I, X, Z, X-then-Z map the pair onto the four mutually orthogonal Bell states)
  and Bob's CNOT+H decode reads both bits with certainty — along with its honesty demos:
  the encoded pair is **locally invisible** (reduced Bloch length 0, and the phase-flip
  message's seeded 1000-shot counts are identical to the plain Bell pair — no-signalling
  shown on actual counts), and two qubits are used in total, one shipped ahead as
  entanglement, so Holevo's bound is respected, not beaten.
  **93 structural checks** in `tools/verify.mjs` prove the manifest, precache list and that
  the app references **no external asset of any kind**, plus a **53-check in-app self-test**;
  zero runtime network calls after first load.
- **Visualizations:** the app itself — live amplitude/probability readouts, the canvas Bloch
  sphere, the 1000-shot seeded histogram; original SVG-sourced icons.
- **Use case:** a curious person building correct quantum intuition without matrix walls or
  "tries every answer at once" hype; every claim demonstrated live or cited (Nielsen &
  Chuang, Preskill's NISQ paper, and five more references).
- **Open improvements:** (1) two qubits is the honest ceiling for full state display — a
  three-qubit mode would need a different visual language; (2) lessons could link out to
  exercises, kept offline-first.

## 19. logistics-flow-studio — Logistics & Optimization (WarehouseTwin — WMS + Plant Simulator, v3.24)

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
  by ~21%** (46.71 → 36.70 m/order) — the measurement behind the advisor's suggestion.
  Factory mode (v3.17–v3.19) grew a real line-flow engine: the deterministic line sim
  resolves declared **multi-way proportional-flow routing** (ratio splits, merges,
  assembly/dismantle) with **conservation verified at every node**; the generator itself
  emits a multi-way network — the *"Machining shop with QA split"* baseline
  (`machining-qa-split`, declared 60/40 split) is harness-pinned at the offered 120
  parts/hr: bottleneck *QA deep test* at 32 s → **112.5 parts/hr**, line efficiency
  141/160 ≈ **88.1%** — and the optimizer's **RPW line balancing** packs workstations on
  the resolved per-finished-unit effective loads (byte-identical to the legacy balancer on
  a pure chain, harness-pinned). The v3.19 **Fluids steady-state continuous-flow solver**
  gives the process-industry components deterministic flow in m³/h: volume conservation
  verified at every node, tank fill horizons computed analytically (free volume ÷ net
  inflow), and the bottleneck pipe, curtailed supply and starved mixers named in plain
  language — a steady-state analytical model, **modelled, not measured**, and explicitly
  **NOT CFD or hydraulics** (no pressure, viscosity, head loss or pump curves). **49
  headless verification harnesses** (`test/run-all.mjs`, no stubs) plus an **in-browser
  self-test (149/149)** back every documented behaviour.
- **The plant now reads like a working shift (v3.21–v3.24)** — four releases that changed
  what the canvas *shows*, not what it computes, shipped as strictly read-only drawing
  layers. **v3.21 industrial material identity** (`floor.js`): a poured-concrete slab with
  a deterministic exposed-aggregate speckle baked into an 8 m repeating tile, **saw-cut
  control joints on the real ~5 m bay**, **100 mm safety-yellow aisle lines** with
  stencilled travel arrows, **75 mm white zone borders** and a **150 mm black/yellow hazard
  hatch** on every dock apron, and **51 element types** re-toned off the blueprint ramp onto
  real materials — orange-red painted rack uprights on **galvanised steel beams whatever the
  uprights are painted**, machine gray with safety-orange guards, wooden pallets and kraft
  cartons (console ink measured at **11.3:1 / 5.3:1**, indicator LEDs at **≥ 3:1** as
  non-text UI). **v3.22 living workers** (`workers.js`): every manned element is staffed by
  an articulated **1.75 m** figure placed by two-link IK, whose pose is a *pure function of
  that element and the sim tick* — a picker walks with a real alternating gait and
  counter-swinging arms, **bends into the rack face** (deep at a floor-level face, barely a
  lean at a chest-level one), straightens **with a kraft carton in its hands** and carries it
  back; a packer sweeps a tape gun **one-handed** over the bench; a staging worker carries
  and places; a dock worker **raises a handheld and scans** — in EN ISO 20471-family hi-vis
  with a deliberately **neutral head: no skin tone, no gender, no identity is modelled**,
  legible at **7 px**, culled below the glyph tier and **capped at 64** figures. **v3.23
  physical goods** (`goods.js`): a wrapped **EUR pallet-load** off the inbound trailer
  becomes a **kraft carton** when the put-away station depalletises it, a moulded **plastic
  tote** when it is picked and a taped, labelled **parcel** when it is packed — the form
  changes exactly where the sim's own FIFO server does the work, **one MU stays one MU** so
  flowsim's spawned == in-flight + completed invariant is untouched, and units ride the
  **belt top**, the **RGV/AGV deck** and the **forklift tines** (a reach truck's forks raise
  with the load and come back down empty), follow the belt **round the bend**, and queue
  **nose-to-tail** one unit length plus a bumper gap along the sim's own route; rack stock
  moves through the **existing** deterministic fill pattern, clamped inside its own bound —
  no second inventory model, no new number. **v3.24 the working shift** (`shift.js`):
  forklifts take a load at the bay, **drive out along the aisle in the direction the sim's
  own plan routes material** (the haul lane marched against the real layout at half-cell
  steps, stopping about half a truck short of whatever blocks it — so a truck drives an
  *aisle*, never through a rack), raise the forks, place the pallet, turn and come back with
  the empty, in a closed loop **continuous in position, heading and fork height over a
  4,000-sample sweep**; congestion is an exponential smoother on normalised queue depth,
  integrated in *sim time* so it is exactly frame-rate invariant, under a **Schmitt trigger**
  and a **48-tick minimum dwell** — against a queue that crosses its threshold **on every
  tick for 900 ticks the band changes ZERO times**, while the badge keeps the sim's own raw
  count; **dock trailers** back onto working doors behind a two-second dwell (shutters up,
  levellers down, empty pallets on the apron); every stencilled floor arrow is flipped to
  agree with the direction material actually goes; and an **andon lamp** reads the run as
  **shape + colour + words**, never colour alone. All four are deterministic (no `Date`, no
  `Math.random`), LOD-gated and view-culled, and resolve to a legible static frame under
  `prefers-reduced-motion`. **Honest scope:** these are *rendering* corrections — they
  change **no number, no model and no export** (capacities, KPIs, compliance outcomes, the
  IFC path and every saved scenario stay byte-identical); the congestion bands are a
  **drawing filter over the existing synthetic queue heuristic**, the truck, trailer and
  handling-unit dimensions are **nominal drawing constants**, the one-worker-per-manned-
  element roster is a drawing heuristic, and none of it is motion capture, ergonomics, a
  labour standard, a staffing recommendation, a fleet or duty-cycle model, CAD/BIM or a
  measurement. Still to do, stated: a truck does not yet steer round a corner, and the
  docks model no turnaround time and no yard.
- **Visualizations:** the live canvas floor plan, the animated material flow and the KPI
  cockpit themselves; `docs/img/warehousetwin.png`; compliance highlights, optimizer ghost
  previews, the pick-travel heatmap and the 2D/3D equipment scene (P toggles the 3D view) —
  now over a concrete-and-paint plant floor with workers, physical handling units, hauling
  forklifts, dock trailers and an andon lamp.
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
- **Measured results (full run, all 13 artifact identities PASS, plus 4 additive):** cleaned
  revenue reproduced across two repositories **to the penny — GBP 19,643,861.62**; the
  ledger's window revenue equal to the cleaned data's to the penny (GBP 1,047,042.41); the
  cost ledger summing to the cent (253,427.16); every pick (256,787 lines), carton (70,820)
  and route drop (4,151) conserved. Three additive identities close the remaining seams:
  identity (n) — cost-driver reconstruction — rebuilds each cost line from its physical
  driver × published rate to the cent; identity (o) — forecast-error containment —
  proves the arc-elasticity of total cost to a whole-book forecast surge equals the
  holding-cost share **exactly (0.0580** on the committed full run**)**, so a doubling of
  forecast demand would raise modelled cost-to-serve by 5.80% while every delivered-cost
  line and the real revenue stay unmoved; and identity (p) — order-level allocation
  conservation — spreads the published cost ledger over every one of the **4,151 real
  orders** under labelled allocation rules (labour by the order's own DES pick minutes,
  transport by its carton share of its delivery day's CVRP km, facility split equally,
  holding honestly kept on the SKU plane) and machine-checks that the spread loses nothing
  and invents nothing: each column reassembles to its ledger line and both planes jointly
  to the ledger total **to the cent (253,427.16 == 253,427.16)**. The per-order
  distribution is the finding: median cost 20.67 GBP vs mean 57.51, the costliest 10% of
  orders (416 of 4,151) carry **59.0% of delivered cost (Gini 0.665)**, and the 191 orders
  (4.6%) whose modelled cost exceeds their own real revenue are reported as the model's
  shape under invented rates — a labelled cost model, never a profit claim. A 17th
  identity (q) — the **fleet knob** — sweeps the van capacity (a labelled
  synthetic-assigned fleet parameter, base 80 cartons) across a deterministic grid from 1
  to 320, re-solving every delivery day's CVRP + Clarke-Wright at each setting with the
  existing stage-4b engine and re-checking all 13 identities at every knob point: the
  routed drops and cartons are conserved exactly (the knob changes HOW cartons ride, never
  WHAT ships), labour, holding, facility and the real window revenue stay invariant to the
  cent, the transport line equals CVRP km × the published rate rebuilt independently, and
  the total moves by exactly the transport delta. The measured curve is diminishing
  returns — capacity buys km only while it binds: 1 → 10 cartons per van saves 206,937.7
  km, 40 → 80 saves 1,686.7, and 160 → 320 only 194.8 — and one omission is deliberate and
  declared: this ledger prices km, not vehicles, so the downhill direction of the curve is
  a model property, never fleet advice; vehicle-days are reported unpriced next to the
  pounds. Honest
  findings kept in the headline: on lumpy
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
  flag it STALE if the code drifts); `deliverables/fleet_sweep.md` + `.csv` (the van-capacity
  sweep, byte-deterministic, regenerated by `python fleet_sweep.py`).
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
- **Measured results:** **193 tests — tool calls, an input-validation matrix, a live JSON-RPC
  handshake, and contract + provenance + idempotency/cache validation**; every tool validates input and returns
  structured error results on any failure (bad input, missing source repo, engine error) —
  the server never crashes on a tool call; source repos are imported read-only with
  env-overridable paths. A machine-checked contract layer introspects the six served tools
  and asserts that the registry, the implementations and the published catalog stay in
  agreement, that every served `inputSchema` is a valid JSON Schema, and that a sample
  request/response round-trips against the real served contract. Every result — success
  *or* error — now carries a **machine-readable provenance block**, required by the
  contract layer's result envelope so no tool can omit it: server and engine commits
  (best-effort from the local checkout's `.git`, null when unresolvable, never guessed), a
  canonical data label (`synthetic` / `real+derived` / `real-local` / `caller-provided`)
  cross-checked against the tool description's honesty wording, and a determinism flag;
  error results carry identity only — a failed call computed nothing, so it makes no data
  claims. Identical requests should not recompute — the enterprise-integration pattern:
  every call to a **deterministic** tool is assigned a reproducible **SHA-256 idempotency
  key** over a documented material string covering every fact the result depends on
  (server version, tool, canonically-sorted arguments with defaults applied, and the exact
  engine checkout — repo, resolved path, commit, read at call time), and an identical
  earlier success is served from a bounded in-process LRU cache **and says so**:
  `provenance.cache` (`cacheable` / `hit` / `key`) is required by the contract layer's
  result envelope. Because the key embeds the engine commit, a cached result can never
  outlive the code that computed it — after a checkout change you get a fresh computation,
  never a stale replay; policy is derived from provenance (cacheable if and only if
  declared deterministic, so `portfolio_status` is never cached), errors are never cached,
  and the honest scope is stated: the cache lives and dies with one server process — no
  persistence, no cross-session sharing.
- **Visualizations:** none of its own — the deliverable is the protocol integration; ships
  ready-to-paste configs for Claude Desktop (`claude_desktop_config.json`) and Claude Code
  (`claude mcp add chain-mcp -- python -m chainmcp`), six example prompts, and a
  deterministic `deliverables/tool_catalog.md` emitted by the contract layer (now carrying
  a "Cacheable" column, so the docs cannot drift from the cache policy either).
- **Use case:** the integration work "agentic AI" projects consist of in practice — wiring a
  language model to real, non-trivial computational engines with honest schemas, provenance
  labels and graceful failure.
- **Honesty labels (its own framing):** five tools state via a per-result `data_note` that
  they run on their repos' deterministic synthetic seeded datasets — real solver outputs on
  fabricated inputs; `forecast_demand` runs the real UCI Online Retail II pipeline (history
  `real`, forecasts `derived`), and if naive wins a demand class, naive is what gets
  reported. Limitations stated: local sibling checkouts only, stdio single-user, first
  forecast call ~10 s.

## 23. logistics-digital-twin — Logistics & Optimization (the OR engine behind the twin)

- **What it is:** the reference operations-research engine the WarehouseTwin app is a
  front-end to — 3D carton packing (FFD with a CP-SAT optimality check), Hungarian-algorithm
  slotting, a hand-rolled discrete-event simulation, pick-path routing scored against the
  exact optimum and order batching — all sharing the same `wt-1` layout format the app uses.
  Everything is synthetic and deterministic (seed 42).
- **Measured results:** slotting via linear assignment cuts pick travel **−44.2%**
  (golden-zone A-occupancy **25% → 100%**, reshuffle break-even **~0.7 days**); container
  fill **2.0% → 30.2%** (**56 containers saved**, CP-SAT proving the heuristic optimal on
  the checked instance); the DES modern-vs-legacy run gives **cycle time −76.1%, picker
  travel −66.5%**. Pick-path routing measures four classic policies against a brute-force
  **exact optimum** (equivalently Ratliff–Rosenthal single-block): on the optimized layout
  **return is closest at 27.46 m/order, +3.03% above the 26.65 m optimum**, largest-gap
  +5.53%, s-shape +7.13%, midpoint +11.01% — and holding the policy fixed, **the
  velocity-optimized layout routes ~46% shorter than legacy (51.4 → 27.5 m/order)**. Order
  batching walks every batched tour on the *same* aisle geometry against the same exact
  optimum (extended with a Held–Karp DP): **savings batching cuts total pick travel 2,692 m
  → 774 m per shift (−71.3%)** on the optimized layout (26 tours, 6.04 faces/tour) and
  −72.3% on legacy, so **batching and slotting stack rather than cancel** — and **batching
  flips the routing recommendation**, tour density rising **2.9 → 6.0** faces and the best
  executable heuristic moving from return to **largest-gap (+1.24% above optimum)**, the
  textbook density result measured rather than quoted. **New: the result is drawn on the
  floor it happens on.** A renderer — *not a new model*: the assignment comes from the
  Hungarian optimizer, the geometry from `RoutingGeometry`, the drawn waypoints from
  `routing.heuristic_route`, and every metre from `routing.route_length` /
  `optimal_route_length` / `batching.batch_route_length`, so **no number on either plate is
  measured off the drawing** — it is printed because the engine computed it, and the test
  suite pins each one. Plate 1 (the floor plan) draws six pick aisles on the modelled
  **5.0 m** pitch between a front and back cross-aisle, a dispatch dock at the corner depot,
  and **6 × 4 bays × 3 levels** of pallet positions shaded by ABC class, with the A-movers
  filling the **12 positions nearest the dock (25% → 100%** golden-zone occupancy) and the
  seeded shift's widest order walked under the recommended `return` policy — **6 pick faces,
  69.2 m against the 64.4 m exact optimum for those same picks (+7.5%)**, the heuristic's
  real gap measured per order rather than asserted. Plate 2 (batching before/after) shows the
  batch that saves the most metres — **orders 44, 76, 87 and 96**: walked separately under
  `largest-gap` they cost **60.8 + 63.2 + 63.2 + 66.8 = 254.0 m**; on one **4-tote cart** the
  same ten pick faces cost **66.8 m — −73.7%**, both panels under the same routing policy so
  the difference is batching alone.
- **Visualizations:** `docs/img/warehouse_floorplan.svg` (Plate 1, also the repo's README
  hero) and `docs/img/batching_routes.svg` (Plate 2), regenerated by
  `python -m logitwin.floorplan`; `docs/img/warehouse_layout.svg` (the velocity-slotted
  layout, mirrored into this site's `docs/img/`) and `docs/img/slotting_before_after.svg`;
  `docs/batching_comparison.svg` / `.csv`, `docs/routing_comparison.svg`,
  `docs/labour_sensitivity.svg`, `docs/slotting_sensitivity.svg` — every SVG hand-built by
  the engine (no plotting library) and byte-identical across re-runs.
- **Use case:** the tested analytics core that keeps the operable twin honest — the layer you
  would harden and re-measure first on real slotting, packing and picking data.
- **Open improvements (its own framing):** (1) the drawing conventions are stated *on every
  plate because they are drawing and not model* — the model puts every pick face on the aisle
  centreline and carries no rack side, depth or wall, rack levels are vertical in reality and
  collapse to one floor point in the model (drawn as three chips across the rack depth), and
  only the two modelled dimensions (5.0 m aisle pitch, 1.2 m bay depth) are true to the scale
  bar; the drawn route is always the **executable heuristic**, because an exact optimum is a
  length, not a drawn route; (2) single-block layout with a corner depot and **no aisle
  congestion, one-way flow or middle cross-aisle** — a real floor has all three, so the
  optimum is exact *only for this metric model*; batching is static/offline and counts travel
  metres only (tote handling, cart weight, congestion and the time dimension are out of
  scope), and "exact" means exact per tour *given the batches* — optimal batching is NP-hard
  above 2 orders per cart (Gademann & van de Velde 2005).
