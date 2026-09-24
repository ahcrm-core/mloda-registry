# Issue #717 — DuckDB NaN First Red

Status: FIRST RED PRESERVED / NO PRODUCT REPAIR YET

Upstream issue: mloda-ai/mloda-registry#717

Baseline:
- upstream mloda-registry main: 85bd72347f89949a65f6c60340eb877d4a52eea1
- branch: fix/717-duckdb-nan-mask-first-red
- test commit: b25cf66399840bc34a7e96d3f3ecea8b2fc08a55
- workflow commit: 97d23e0536ed19249230877a8ee7858da056631a
- workflow run: https://github.com/ahcrm-core/mloda-registry/actions/runs/36013189310

Observed failure:
- focused test executed; no skip
- result: 1 failed
- actual DuckDB result: [(None,), (20,), (30,)]
- expected result: [(None,), (None,), (30,)]
- the NaN row incorrectly passed the greater_equal mask and retained value 20

No production repair had been applied when this result was recorded.
