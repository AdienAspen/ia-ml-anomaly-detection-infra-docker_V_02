from __future__ import annotations

import unittest

try:
    from .contract_test_utils import (
        assert_contract_shape,
        assert_payload_matches_minimum_contract,
        load_contract,
    )
except ImportError:
    from contract_test_utils import (
        assert_contract_shape,
        assert_payload_matches_minimum_contract,
        load_contract,
    )


class ContextSliceContractTest(unittest.TestCase):
    def test_contract_shape_and_sample_payload(self) -> None:
        contract = load_contract("context_slice_v0_1.json")
        assert_contract_shape(self, contract, "context_slice_v0_1")
        assert_payload_matches_minimum_contract(
            self,
            contract,
            {
                "schema_version": "context_slice_v0_1",
                "context_id": "context-001",
                "trace_id": "trace-001",
                "service_name": "payments-api",
                "cluster_decision_id": "cluster-decision-001",
                "evidence": [{"kind": "span", "summary": "p95 latency increased"}],
                "timeline": [{"timestamp": "2026-06-10T12:00:00Z", "event": "span_started"}],
            },
        )


if __name__ == "__main__":
    unittest.main()
