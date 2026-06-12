# PRE-HOC

Offline path for reproducible training data generation.

Initial flow:

```text
scenario YAML
-> generate_training_data.py
-> OTel SDK
-> Collector file/debug exporter
-> raw OTel JSON
-> build_dataset.py
-> features/labels dataset
-> train_models.py
-> model artifacts
```

Raw OTel JSON is the first-class artifact. Tabular datasets are derived.
