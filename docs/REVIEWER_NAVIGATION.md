# Reviewer navigation and evidence refresh

The project catalogue now has a bilingual full-text finder. Terms match across
English and German descriptions, including all findings and limitations. Multiple
terms must all occur somewhere in the same project; the focus-area filter is an
additional restriction. Empty searches restore that area's complete list. Reset
clears both controls and returns focus to the input. No request leaves the device.

The finder does not rank projects, remove evidence, or collapse unfavourable
findings. Individual cards now have stable `project-<slug>` fragment targets.

The decision-chain featured copy and first metric were refreshed against its
committed README at source commit `1e8213d`: 13 artifact identities plus five
additive identities, including (r). The prominent evidence finding is GBP 0.00
real-anchored out of GBP 253,427.16 modelled cost; GBP 20,000.00 has no observed
number anywhere in its chain. Existing detailed findings remain intact.
Source: [decision-chain README](https://github.com/Dimitres-Kisimov/decision-chain/blob/1e8213d/README.md).

Document-extraction search copy now names its documented input types: invoices,
delivery notes and RFQ emails. Source: [doc-extract-agent README](https://github.com/Dimitres-Kisimov/doc-extract-agent/blob/c41d7a1/README.md).

The Approach section no longer says every result is synthetic. The catalogue
already includes public real data as well as synthetic examples. This correction
changes no measurement or claimed business outcome.

Verification: `python build.py`, `python tools/validate_site.py`, `python -m pytest -q`,
and `ruff check .`. Browser checks cover multi-term search, German terms while
English is selected, language switching with a live query, combined filters,
empty-state recovery, narrow-screen layout and preserved evidence visibility.

The printable A4 summary now places each metric below its project name, preventing
long findings from colliding with names or the footer. Currency strings render as
literal text rather than matplotlib math expressions. Rendered PDF inspected at
1400 px; all 22 rows fit without overlap. Two builds with SOURCE_DATE_EPOCH=1789819583
produce SHA256 FA13F4702ABFB29473D4AC5107AE31AE5A2F8B9B622347161C1360C2581B3FEA.
