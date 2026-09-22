#!/usr/bin/env python3

import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PILOT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PILOT_ROOT))

import validate_agent_audit


class AgentAuditValidationTests(unittest.TestCase):
    def test_complete_result_preserves_recorded_limitations(self):
        result = validate_agent_audit.validate()
        self.assertEqual(
            "PASS_COMPLETE_WITH_RECORDED_LIMITATIONS", result["status"]
        )
        self.assertTrue(result["stage5_private_preview_operational"])
        self.assertEqual(0, result["automatic_retry_count"])
        self.assertEqual(3, result["authorized_review_attempts"])
        self.assertTrue(result["review_checkpoint_durable"])

    def test_operational_state_requires_durable_review(self):
        original = validate_agent_audit.load

        def altered(name):
            value = original(name)
            if name == "sanitized-standard-review.json":
                value = copy.deepcopy(value)
                value["checkpoint_state"] = "PERSISTING"
            return value

        with patch.object(validate_agent_audit, "load", side_effect=altered):
            with self.assertRaises(ValueError):
                validate_agent_audit.validate()

    def test_retry_count_cannot_be_elevated(self):
        original = validate_agent_audit.load

        def altered(name):
            value = original(name)
            if name == "sanitized-agent-pilot-audit.json":
                value = copy.deepcopy(value)
                value["automatic_retry_count"] = 1
            return value

        with patch.object(validate_agent_audit, "load", side_effect=altered):
            with self.assertRaises(ValueError):
                validate_agent_audit.validate()

    def test_sanitized_review_payload_tamper_is_rejected(self):
        original = validate_agent_audit.load

        def altered(name):
            value = original(name)
            if name == "sanitized-standard-review.json":
                value = copy.deepcopy(value)
                value["structured_result"]["checks"]["negative_cases"] = True
            return value

        with patch.object(validate_agent_audit, "load", side_effect=altered):
            with self.assertRaisesRegex(
                ValueError, "sanitized payload hash drift"
            ):
                validate_agent_audit.validate()


if __name__ == "__main__":
    unittest.main()
