from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACTS_ROOT = PROJECT_ROOT / "contracts"


def load_contract(name: str) -> dict[str, Any]:
    path = CONTRACTS_ROOT / name
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def assert_contract_shape(testcase, contract: dict[str, Any], expected_schema_version: str) -> None:
    testcase.assertEqual(contract["type"], "object")
    testcase.assertIn("required", contract)
    testcase.assertIn("properties", contract)
    testcase.assertIn("schema_version", contract["required"])
    testcase.assertEqual(contract["properties"]["schema_version"]["const"], expected_schema_version)
    for required_key in contract["required"]:
        testcase.assertIn(required_key, contract["properties"])


def assert_payload_matches_minimum_contract(testcase, contract: dict[str, Any], payload: dict[str, Any]) -> None:
    required = contract["required"]
    properties = contract["properties"]

    for key in required:
        testcase.assertIn(key, payload)

    if not contract.get("additionalProperties", True):
        testcase.assertEqual(set(payload).difference(properties), set())

    for key, rules in properties.items():
        if key not in payload:
            continue
        value = payload[key]
        if "const" in rules:
            testcase.assertEqual(value, rules["const"])
        if "enum" in rules:
            testcase.assertIn(value, rules["enum"])
        if rules.get("type") == "array":
            testcase.assertIsInstance(value, list)
        if rules.get("type") == "object":
            testcase.assertIsInstance(value, dict)
