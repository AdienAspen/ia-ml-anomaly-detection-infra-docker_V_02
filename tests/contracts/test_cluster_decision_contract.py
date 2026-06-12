from __future__ import annotations

import unittest

from contract_test_utils import (
    assert_contract_shape,
    assert_payload_matches_minimum_contract,
    load_contract,
)


class ClusterDecisionContractTest(unittest.TestCase):
    def test_contract_shape_and_sample_payload(self) -> None:
        contract = load_contract("cluster_decision_v0_1.json")
        assert_contract_shape(self, contract, "cluster_decision_v0_1")
        assert_payload_matches_minimum_contract(
            self,
            contract,
            {
                "schema_version": "cluster_decision_v0_1",
                "decision_id": "cluster-decision-001",
                "trace_id": "trace-001",
                "model_name": "iforest_otel_v0_1",
                "cluster_id": "cluster-a",
                "anomaly_score": 0.91,
                "is_anomaly": True,
                "reason_codes": ["high_latency"],
            },
        )


if __name__ == "__main__":
    unittest.main()
