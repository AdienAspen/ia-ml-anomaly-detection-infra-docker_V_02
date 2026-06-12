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


class OTelTraceEventContractTest(unittest.TestCase):
    def test_contract_shape_and_sample_payload(self) -> None:
        contract = load_contract("otel_trace_event_v0_1.json")
        assert_contract_shape(self, contract, "otel_trace_event_v0_1")
        assert_payload_matches_minimum_contract(
            self,
            contract,
            {
                "schema_version": "otel_trace_event_v0_1",
                "trace_id": "trace-001",
                "span_id": "span-001",
                "parent_span_id": None,
                "service_name": "payments-api",
                "operation_name": "process_payment",
                "timestamp": "2026-06-10T12:00:00Z",
                "duration_ms": 42.0,
                "status_code": "OK",
                "error_type": None,
                "attributes": {"http.method": "POST"},
            },
        )


if __name__ == "__main__":
    unittest.main()
