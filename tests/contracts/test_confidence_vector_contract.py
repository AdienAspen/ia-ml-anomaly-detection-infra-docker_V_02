from __future__ import annotations

import unittest

from contract_test_utils import (
    assert_contract_shape,
    assert_payload_matches_minimum_contract,
    load_contract,
)


class ConfidenceVectorContractTest(unittest.TestCase):
    def test_contract_shape_and_sample_payload(self) -> None:
        contract = load_contract("confidence_vector_v0_1.json")
        assert_contract_shape(self, contract, "confidence_vector_v0_1")
        assert_payload_matches_minimum_contract(
            self,
            contract,
            {
                "schema_version": "confidence_vector_v0_1",
                "confidence_id": "confidence-001",
                "trace_id": "trace-001",
                "agent_decision_id": "agent-decision-001",
                "scores": {
                    "data_quality": 0.9,
                    "trace_completeness": 0.8,
                    "ml_signal_strength": 0.85,
                    "context_coverage": 0.75,
                    "recommendation_confidence": 0.7,
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
