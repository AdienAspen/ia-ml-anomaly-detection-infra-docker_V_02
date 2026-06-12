# Anomaly Detector

Streaming inference service for AD-HOC mode.

Responsibilities:

- consume OTel-derived features from Redis Streams
- load validated model artifacts from `artifacts/models/v_02/`
- apply iForest, HDBSCAN, and post-filter policy
- publish versioned cluster decisions for the Context Engine

Training is not performed here. Models are produced by PRE-HOC and loaded by AD-HOC.
