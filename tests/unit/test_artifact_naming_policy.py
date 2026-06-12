from __future__ import annotations

import re
import unittest


ARTIFACT_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*_v[0-9]+_[0-9]+\.[a-z0-9]+$")


class ArtifactNamingPolicyTest(unittest.TestCase):
    def test_versioned_artifact_names(self) -> None:
        names = [
            "otel_pre_hoc_raw_traces_v0_1.jsonl",
            "otel_pre_hoc_feature_dataset_v0_1.parquet",
            "iforest_otel_model_v0_1.joblib",
            "hdbscan_otel_model_v0_1.joblib",
            "post_filter_policy_v0_1.json",
        ]

        for name in names:
            with self.subTest(name=name):
                self.assertRegex(name, ARTIFACT_NAME_PATTERN)


if __name__ == "__main__":
    unittest.main()
