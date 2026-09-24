# Issue #715 — Compatibility First Red

Status: FIRST RED PRESERVED / NO PRODUCT REPAIR YET

Upstream issue: mloda-ai/mloda-registry#715

Compatibility environment:
- mloda: 0.14.0
- polars: 1.43.2
- mloda source commit: 754e6f0305d25fbbe69b30fa9ce71b1a80c4442d
- workflow run: https://github.com/ahcrm-core/mloda-registry/actions/runs/36010480364
- branch head at run: 0488670fdd23c970a921a68dc7333f43acbc659a

Observed failure:
- focused test executed; no skip
- result: 1 failed
- PolarsExprMaskEngine.is_in runtime source calls data.collect_schema()
- exception: AttributeError: 'NoneType' object has no attribute 'collect_schema'

Root-cause diagnosis before repair:
- build_polars_mask_expr currently accepts only mask_spec.
- It dispatches PolarsExprMaskEngine operations with data=None.
- apply_polars_mask owns the actual Polars LazyFrame but calls build_polars_mask_expr(mask_spec) without passing it.
- Therefore schema-dependent upstream mask operations cannot inspect the LazyFrame.

Smallest defensible repair candidate:
- pass the existing LazyFrame from apply_polars_mask into build_polars_mask_expr;
- have build_polars_mask_expr pass that same data object to _engine_op / PolarsExprMaskEngine;
- do not alter upstream mloda, operator semantics, or unrelated framework paths.

This record preserves the failure before any production repair.
