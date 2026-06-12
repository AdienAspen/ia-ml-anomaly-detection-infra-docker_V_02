from __future__ import annotations

import unittest

from contract_test_utils import (
    assert_contract_shape,
    assert_payload_matches_minimum_contract,
    load_contract,
)


class AgentDecisionContractTest(unittest.TestCase):
    def test_contract_shape_and_sample_payload(self) -> None:
        contract = load_contract("agent_decision_v0_1.json")
        assert_contract_shape(self, contract, "agent_decision_v0_1")
        assert_payload_matches_minimum_contract(
            self,
            contract,
            {
                "schema_version": "agent_decision_v0_1",
                "agent_decision_id": "agent-decision-001",
                "trace_id": "trace-001",
                "context_id": "context-001",
                "triage": "investigate",
                "diagnosis": "payments-api latency propagation suspected",
                "recommendation": "review payments-api dependency latency before remediation",
                "confidence_id": "confidence-001",
                "policy_outcome": "requires_approval",
                "requires_human_approval": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
