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


class AuditEventContractTest(unittest.TestCase):
    def test_contract_shape_and_sample_payload(self) -> None:
        contract = load_contract("audit_event_v0_1.json")
        assert_contract_shape(self, contract, "audit_event_v0_1")
        assert_payload_matches_minimum_contract(
            self,
            contract,
            {
                "schema_version": "audit_event_v0_1",
                "event_id": "audit-001",
                "trace_id": "trace-001",
                "component": "agentic_reasoning_core",
                "action": "emit_agent_decision",
                "timestamp": "2026-06-10T12:00:00Z",
                "outcome": "success",
                "provenance": {"source": "contract_test_sample"},
            },
        )


if __name__ == "__main__":
    unittest.main()
