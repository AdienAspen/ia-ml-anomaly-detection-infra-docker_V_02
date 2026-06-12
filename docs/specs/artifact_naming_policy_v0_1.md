# Artifact Naming Policy V0.1

All generated PRE-HOC, ML, and runtime artifacts use semantic, versioned names.

Pattern:

```text
<domain>_<artifact_kind>_v<major>_<minor>.<extension>
```

Examples:

```text
otel_pre_hoc_raw_traces_v0_1.jsonl
otel_pre_hoc_trace_bundle_v0_1.json
otel_pre_hoc_feature_dataset_v0_1.parquet
otel_pre_hoc_labels_v0_1.parquet
iforest_otel_model_v0_1.joblib
hdbscan_otel_model_v0_1.joblib
post_filter_policy_v0_1.json
cluster_validation_report_v0_1.md
model_registry_manifest_v0_1.json
```

Raw OTel JSON is the primary artifact. Feature datasets, labels, models, and validation reports are derived artifacts.
