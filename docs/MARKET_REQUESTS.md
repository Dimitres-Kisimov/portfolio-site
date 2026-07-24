# Market requests → portfolio map

A researched list of the most-requested capabilities in three areas — (a) BI/analytics,
(b) automation / low-code + agentic AI, (c) logistics / warehouse optimization — each mapped
to the portfolio project that addresses it, or flagged as a backlog gap.

**How to read this.** Every item separates what is **verified from public sources** (a named,
checkable report, product doc, or standard, with a URL) from **my inference** (the mapping and
my judgement of coverage). I do not restate a statistic unless it is attributed to its source;
where I have no citation for a number I describe the demand qualitatively.

Coverage note: I could not independently re-audit paywalled analyst reports; where I cite one
(e.g. Gartner Magic Quadrants), I cite it by its published name so it can be looked up, and I
only quote figures a public press release or vendor page stated.

---

## (a) BI / analytics platforms

**Verified from public sources**

- The Dresner *Wisdom of Crowds* Business Intelligence Market Study (17th edition, 2025)
  reports the most strategic BI topics as **data security, data quality, data integration,
  reporting, and dashboards**. Source: Dresner Advisory Services press release, PR Newswire —
  https://www.prnewswire.com/news-releases/dresner-advisory-publishes-17th-edition-flagship-business-intelligence-market-study-302784060.html
  and study landing page https://dresneradvisory.com/ .
- Gartner's *Magic Quadrant for Analytics and Business Intelligence Platforms* (published
  annually) is the standard analyst framing for this category and emphasizes governed
  self-service, augmented analytics, and natural-language querying. Look up by name at
  https://www.gartner.com/ .
- Natural-language "ask a question of your data" is a first-class, documented feature in the
  major tools: Power BI **Q&A** (https://learn.microsoft.com/power-bi/) and Tableau **Ask
  Data**/**Pulse**. Semantic modelling with a **star schema + DAX** measures is Microsoft's
  documented recommended pattern — https://learn.microsoft.com/power-bi/guidance/star-schema .
- Forecasting / predictive analytics inside BI is a shipped capability (e.g. Power BI's
  built-in forecasting on line charts) — https://learn.microsoft.com/power-bi/ .

**Most-requested capabilities → mapping** *(mapping is my inference)*

| Requested capability | Portfolio coverage |
|---|---|
| Governed KPI dashboards & reporting | `sales-kpi-analytics`, `distributor-intelligence-platform`, `revops-optimizer` (all ship KPI dashboards + exec reviews) |
| Semantic model: star schema + DAX measures | `revops-optimizer` (Power BI star schema with KPIs written as real DAX) |
| Forecasting with honest, out-of-sample evaluation | `sales-kpi-analytics` & `distributor-intelligence-platform` (rolling-origin CV, MASE); `ml-models-lab` (DeepAR-lite) |
| Margin / price-volume-mix bridge, ABC-XYZ, RFM | `sales-kpi-analytics`, `distributor-intelligence-platform` |
| Data quality / reconciliation trust | `sales-kpi-analytics` (SQL-vs-Python rollup asserted to the cent) |
| Prescriptive "what should we do" (not just describe) | `revops-optimizer`, `distributor-intelligence-platform` (optimizers → one € plan + action cards) |
| **Backlog gap:** natural-language query (NLQ) over the model | *not built* — my dashboards are curated, not conversational. A genuine gap versus Power BI Q&A / Tableau Ask Data. |
| **Backlog gap:** cloud multi-tenant governance, row-level security, scheduled refresh | *not built* — artifacts are offline single-file; enterprise governance is out of scope by design. |

---

## (b) Automation / low-code + agentic AI

**Verified from public sources**

- Anthropic's *Building Effective Agents* (engineering guide) defines the now-common building
  blocks and orchestration patterns: an LLM augmented with **tool use**, retrieval and memory;
  workflows vs agents; and the **orchestrator-workers** pattern. It also introduces the
  **Model Context Protocol (MCP)** for connecting tools. Source:
  https://www.anthropic.com/engineering/building-effective-agents and https://modelcontextprotocol.io .
- Low-code automation platforms document the widely-requested primitives directly: **n8n**
  (AI-agent nodes, HTTP/tool calls, error workflows) — https://docs.n8n.io/ ; **Microsoft
  Power Automate** (connectors, approvals/human-in-the-loop) —
  https://learn.microsoft.com/power-automate/ .
- The low-code application platform (LCAP) market is tracked by Gartner's *Magic Quadrant for
  Enterprise Low-Code Application Platforms* and Forrester's *Wave* for low-code — both
  emphasize connectors, governance, and pro-code extensibility. Look up by name at
  https://www.gartner.com/ and https://www.forrester.com/ .

**Most-requested capabilities → mapping** *(mapping is my inference)*

| Requested capability | Portfolio coverage |
|---|---|
| Agentic tool-use loop (LLM selects tools, variable steps) | `agentic-automation-lab` (from-scratch, provider-agnostic loop); `agent-flow-studio` (mock observe→decide→act on a canvas) |
| Visual low-code canvas: nodes, ports, DAG execution | `agent-flow-studio` (Kahn topo-sort executor, hand-drawn SVG wires) |
| Same logic runnable low-code **and** full-code (hybrid) | `agentic-automation-lab` (n8n and Python drive identical tool functions) |
| Document understanding / IDP with validation + confidence gate | `doc-extract-agent` (5-stage pipeline, totals cross-check, human routing) |
| Human-in-the-loop / approval before an action posts | `doc-extract-agent` (confidence gate → human); `agentic-automation-lab` ("a rep reviews every draft" model) |
| Build-vs-buy / ROI to prioritize the automation backlog | `automation-roi-explorer` (hours, €, payback, 3y ROI, ranked) |
| Decision framework: when low-code vs full-code | `agentic-automation-lab` (nine-dimension scorecard with cited ratings) |
| **Backlog gap:** MCP / real connector ecosystem, retries, timeouts, parallel branches | *partly gap* — my agents run a mock/single provider offline; production connectors, retries and parallelism are named as next steps, not built. |
| **Backlog gap:** live latency/cost telemetry per orchestrator | *gap* — only runtime is measured; a parallel live n8n run is the stated next step. |

---

## (c) Logistics / warehouse optimization

**Verified from public sources**

- The MHI *Annual Industry Report* (2025 edition, survey of 700+ supply-chain leaders) reports
  that **83% of respondents are adopting or planning to adopt robotics and automation**, with
  **budget and cost/ROI the top barriers** and **labor shortages the leading catalyst**.
  Source, as summarized in trade coverage and MHI's report — https://www.mhi.org/publications/report
  (see also the 2024 edition PDF hosted publicly:
  https://locusrobotics.com/wp-content/uploads/2024/05/MHI-Industry-Report-2024.pdf ).
- Vehicle routing with real constraints (capacity, **time windows**, multiple depots,
  pickup-and-delivery) is documented directly by Google **OR-Tools** —
  https://developers.google.com/optimization/routing — which is the exact engine and
  constraint set the routing work builds on.
- Warehouse Management System capability sets (slotting, wave/zone picking, labor management,
  3D bin-packing, a digital-twin/simulation layer) are the axes of Gartner's *Magic Quadrant
  for Warehouse Management Systems*. Look up by name at https://www.gartner.com/ .

**Most-requested capabilities → mapping** *(mapping is my inference)*

| Requested capability | Portfolio coverage |
|---|---|
| Capacitated vehicle routing (CVRP) with a measured optimizer-vs-heuristic gap | `route-optimizer` (Clarke-Wright vs OR-Tools GLS, −4.6%/−31%); `distributor-intelligence-platform` (CVRP, 25% km saved) |
| Clear baseline so the routing saving is quantified, not asserted | `route-optimizer` (nearest-neighbour + savings baselines shipped alongside) |
| 3D bin-packing / cube utilization | `logistics-digital-twin` *(in progress — packing module started)* |
| Slotting optimization (fast movers to golden zones) | `logistics-digital-twin` *(in progress — planned)* |
| Discrete-event simulation / digital twin of the operation | `logistics-digital-twin` *(in progress — the DES layer is the next milestone)* |
| ROI / business case for warehouse automation (the MHI budget barrier) | `automation-roi-explorer` (generic back-office ROI; applicable to warehouse processes) |
| **Backlog gap:** road-network distance/time matrix (OSRM/Valhalla) | *gap* — routing currently uses Euclidean/Manhattan distance, not roads. |
| **Backlog gap:** time windows, heterogeneous fleet, driver shifts | *gap* — single depot, homogeneous fleet, no time windows yet (OR-Tools supports all; named as next constraints). |
| **Backlog gap:** live warehouse metrics (throughput, labor) end to end | *gap* — `logistics-digital-twin` is under construction; no measured legacy-vs-modern gap published yet. |

---

## Summary of honest gaps

Across the three areas the recurring, genuinely-unbuilt gaps are: **natural-language querying**
over a BI model; a **real connector/MCP ecosystem with retries and parallelism** for the agents;
**road-network routing** and **time-window/heterogeneous-fleet** constraints; and the
**warehouse digital-twin metrics** (`logistics-digital-twin` is still under construction). These
are named as next steps in the respective repos rather than papered over.

*Author: Dimitres Kisimov, 2026. Sources are cited inline; the capability-to-project mappings
and the coverage judgements are my own inference and are labelled as such.*
