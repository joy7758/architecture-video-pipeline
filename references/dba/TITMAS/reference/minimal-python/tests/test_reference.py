import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("titmas_reference", ROOT / "titmas_reference.py")
assert SPEC and SPEC.loader
REFERENCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REFERENCE)


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((ROOT / "example-input.json").read_text(encoding="utf-8"))

    def test_example_matches_expected_output(self):
        expected = json.loads((ROOT / "expected-output.json").read_text(encoding="utf-8"))
        self.assertEqual(expected, REFERENCE.transform(self.payload))

    def test_forbidden_action_fails_closed(self):
        payload = copy.deepcopy(self.payload)
        payload["event"]["action"] = "publish"
        with self.assertRaises(REFERENCE.BoundaryRejected):
            REFERENCE.transform(payload)

    def test_unknown_action_fails_closed(self):
        payload = copy.deepcopy(self.payload)
        payload["event"]["action"] = "delete"
        with self.assertRaises(REFERENCE.BoundaryRejected):
            REFERENCE.transform(payload)

    def test_reference_does_not_claim_admission_or_authority(self):
        output = REFERENCE.transform(self.payload)
        self.assertIn("NO_DBOS_ADMISSION", output["limitations"])
        self.assertIn("NO_SAEE_EXECUTION", output["limitations"])
        self.assertNotIn("authorization_status", output["verification_result"])

    def test_missing_input_fails_closed(self):
        payload = copy.deepcopy(self.payload)
        del payload["existing_evidence_ref"]
        with self.assertRaises(ValueError):
            REFERENCE.transform(payload)


if __name__ == "__main__":
    unittest.main()
