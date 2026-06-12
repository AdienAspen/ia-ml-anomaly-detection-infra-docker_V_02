from __future__ import annotations

import unittest

from contract_test_utils import (
    assert_contract_shape,
    assert_payload_matches_minimum_contract,
    load_contract,
)


class MLFeatureVectorContractTest(unittest.TestCase):
    def test_contract_shape_and_sample_payload(self) -> None:
        contract = load_contract("ml_feature_vector_v0_1.json")
        assert_contract_shape(self, contract, "ml_feature_vector_v0_1")
        assert_payload_matches_minimum_contract(
            self,
            contract,
            {
                "schema_version": "ml_feature_vector_v0_1",
                "trace_id": "trace-001",
                "service_name": "payments-api",
                "window_start": "2026-06-10T12:00:00Z",
                "window_end": "2026-06-10T12:01:00Z",
                "features": {"duration_p95_ms": 42.0, "error_rate": 0.0},
            },
        )


if __name__ == "__main__":
    unittest.main()
