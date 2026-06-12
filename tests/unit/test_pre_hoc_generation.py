from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pre_hoc.generate_training_data import generate_training_data


class PreHocGenerationTest(unittest.TestCase):
    def test_generates_raw_otel_jsonl_with_trace_hierarchy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "otel_pre_hoc_raw_traces_v0_1.jsonl"

            summary = generate_training_data(
                scenario_paths=["latency_propagation_jitter_v0_1.yaml"],
                output_path=output,
                seed=11,
                steps=4,
            )

            self.assertEqual(summary["schema_version"], "otel_pre_hoc_generation_summary_v0_1")
            self.assertTrue(output.exists())

            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            self.assertGreater(len(records), 0)

            spans = [record["span"] for record in records]
            self.assertTrue(any(span["parent_span_id"] for span in spans))
            self.assertTrue(all(span["trace_id"] for span in spans))
            self.assertTrue(any(span["attributes"].get("scenario.id") == "latency_propagation_jitter_v0_1" for span in spans))
            self.assertTrue(any(span["attributes"].get("scenario.phase") == "propagating" for span in spans))
            self.assertTrue(any("metric.latency_ms" in span["attributes"] for span in spans))


if __name__ == "__main__":
    unittest.main()
