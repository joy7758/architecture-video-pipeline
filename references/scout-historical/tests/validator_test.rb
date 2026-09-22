# frozen_string_literal: true

require "minitest/autorun"
require "json"
require "stringio"
require "tempfile"
require_relative "../src/validator/input_loader"
require_relative "../src/validator/validate"
require_relative "../src/validator/validation_aggregator"

class ValidatorPrototypeTest < Minitest::Test
  EVALUATION_TIME = Time.iso8601("2026-08-01T12:00:00Z")

  def setup
    @validator = TITMASScout::Validator::ValidationAggregator.new(
      clock: -> { EVALUATION_TIME }
    )
  end

  def test_missing_approval_fails_closed
    input = valid_chain
    input.delete("approval")

    result = @validator.validate(input)

    assert_equal "INVALID", result["validation_status"]
    assert_includes reason_codes(result), "APPROVAL_MISSING"
    assert_equal false, result["authorization_granted"]
    assert_equal false, result["external_action_allowed"]
  end

  def test_missing_discovery_evidence_is_invalid
    input = valid_chain
    input["opportunity"].delete("evidence")

    result = @validator.validate(input)

    assert_equal "INVALID", result["validation_status"]
    assert_includes reason_codes(result), "DISCOVERY_EVIDENCE_MISSING"
  end

  def test_missing_outcome_evidence_is_invalid
    input = valid_chain
    input.delete("outcome_evidence")

    result = @validator.validate(input)

    assert_equal "INVALID", result["validation_status"]
    assert_includes reason_codes(result), "OUTCOME_EVIDENCE_MISSING"
  end

  def test_invalid_opportunity_reference_is_invalid
    input = valid_chain
    input["approval"]["opportunity_reference"]["reference_id"] = "OPP-WRONG"

    result = @validator.validate(input)

    assert_equal "INVALID", result["validation_status"]
    assert_includes reason_codes(result), "OPPORTUNITY_REFERENCE_ID_MISMATCH"
  end

  def test_valid_structure_is_valid_but_never_authorized
    result = @validator.validate(valid_chain)

    assert_equal "VALID", result["validation_status"]
    assert_equal [], result["failed_rules"]
    assert_equal false, result["authorization_granted"]
    assert_equal false, result["external_action_allowed"]
    assert_equal "VALIDATION_DOES_NOT_GRANT_AUTHORIZATION", result["non_authorization_assertion"]
    assert_includes result["ruleset_version"], "PROTOTYPE-STRUCTURAL-SUBSET"
    assert_includes result["unchecked_capabilities"], "uri_resolution"
  end

  def test_agent_quorum_reviewer_shape_is_valid_but_never_authorized
    input = valid_chain
    reviewer = input.fetch("approval").fetch("reviewer")
    reviewer.delete("reviewer_type")
    reviewer.delete("identity_reference")
    reviewer["type"] = "AGENT_QUORUM"
    reviewer["reviewer_id"] = "QUORUM-TEST-001"
    reviewer["role"] = "RELEASE_DECISION_AGENT"
    reviewer["agent_reviews"] = %w[
      DISCOVERY_REVIEWER EVIDENCE_REVIEWER SCOPE_REVIEWER QUALITY_REVIEWER
      RISK_REVIEWER
    ].each_with_index.map do |role, index|
      {
        "agent_identifier" => "AGENT-#{index}",
        "model_runtime_identifier" => "RUNTIME-#{index}",
        "review_role" => role,
        "input_digest" => "sha256:#{"1" * 64}",
        "output_digest" => "sha256:#{(index + 2).to_s * 64}",
        "decision" => "PASS",
        "timestamp" => "2026-08-01T09:12:0#{index}Z",
        "ruleset_version" => "0.1"
      }
    end

    result = @validator.validate(input)

    assert_equal "VALID", result["validation_status"]
    assert_equal false, result["authorization_granted"]
    assert_equal false, result["external_action_allowed"]
  end

  def test_unresolvable_but_well_formed_uris_do_not_trigger_network_resolution
    result = @validator.validate(valid_chain)

    assert_equal "VALID", result["validation_status"]
    assert_includes result["unchecked_capabilities"], "uri_resolution"
  end

  def test_unknown_envelope_field_is_invalid
    input = valid_chain
    input["implicit_permission"] = true

    result = @validator.validate(input)

    assert_equal "INVALID", result["validation_status"]
    assert_includes reason_codes(result), "UNKNOWN_AUTHORITATIVE_FIELD"
  end

  def test_yaml_aliases_are_rejected
    yaml = <<~YAML
      opportunity: &opportunity
        id: OPP-ALIAS
      duplicate: *opportunity
    YAML

    Tempfile.create(["validator-alias", ".yaml"]) do |file|
      file.write(yaml)
      file.flush
      assert_raises(Psych::BadAlias) do
        TITMASScout::Validator::InputLoader.load_yaml(file.path)
      end
    end
  end

  def test_failed_rules_are_deduplicated_and_deterministically_ordered
    input = valid_chain
    input["approval"]["opportunity_reference"]["reference_id"] = "OPP-WRONG"

    result = @validator.validate(input)
    keys = result["failed_rules"].map do |failure|
      [failure["rule_id"], failure["reason_code"], failure["path"]]
    end

    assert_equal keys.uniq, keys
    assert_equal result, TITMASScout::Validator::Support.deep_sort(result)
  end

  def test_cli_returns_zero_only_for_valid_result
    with_json_input(valid_chain) do |path|
      stdout = StringIO.new
      stderr = StringIO.new
      code = TITMASScout::Validator::CLI.run(
        ["--timestamp", "2026-08-01T12:00:00Z", path],
        stdout: stdout,
        stderr: stderr
      )

      assert_equal 0, code
      assert_equal "VALID", JSON.parse(stdout.string)["validation_status"]
      assert_equal "", stderr.string
    end
  end

  def test_cli_returns_one_for_evaluated_invalid_result
    with_json_input({ "schema_version" => "0.1-draft" }) do |path|
      stdout = StringIO.new
      code = TITMASScout::Validator::CLI.run(
        ["--timestamp", "2026-08-01T12:00:00Z", path],
        stdout: stdout,
        stderr: StringIO.new
      )

      assert_equal 1, code
      assert_equal "INVALID", JSON.parse(stdout.string)["validation_status"]
    end
  end

  def test_cli_returns_two_and_invalid_json_for_load_error
    stdout = StringIO.new
    code = TITMASScout::Validator::CLI.run(
      ["--timestamp", "2026-08-01T12:00:00Z", "/definitely/missing/input.yaml"],
      stdout: stdout,
      stderr: StringIO.new
    )
    result = JSON.parse(stdout.string)

    assert_equal 2, code
    assert_equal "INVALID", result["validation_status"]
    assert_equal false, result["authorization_granted"]
    assert_equal false, result["external_action_allowed"]
  end

  private

  def reason_codes(result)
    result["failed_rules"].map { |failure| failure["reason_code"] }
  end

  def with_json_input(value)
    Tempfile.create(["validator-input", ".yaml"]) do |file|
      file.write(JSON.generate(value))
      file.flush
      yield file.path
    end
  end

  def bound_reference(id, type, version, digest_character)
    {
      "reference_id" => id,
      "reference_type" => type,
      "reference_uri" => "https://unresolvable.invalid/#{type.downcase}/#{id}",
      "version" => version,
      "content_digest" => "sha256:#{digest_character * 64}"
    }
  end

  def valid_chain
    opportunity_ref = bound_reference(
      "OPP-TEST-001",
      "TITMAS_SCOUT_OPPORTUNITY",
      "0.1-draft",
      "1"
    )
    assessment_ref = bound_reference(
      "ASSESS-TEST-001",
      "TITMAS_SCOUT_MATCHING_ASSESSMENT",
      "0.1-prototype",
      "2"
    ).merge(
      "model_id" => "TITMAS-SCOUT-MATCHING-SCORE",
      "model_version" => "0.1",
      "reference_status" => "APPLIED",
      "overall_status" => "COMPUTED_UNCALIBRATED",
      "opportunity_id" => "OPP-TEST-001",
      "opportunity_content_digest" => opportunity_ref["content_digest"]
    )
    approval_ref = bound_reference(
      "APPROVAL-TEST-001",
      "TITMAS_SCOUT_APPROVAL",
      "0.1-draft",
      "3"
    )
    action_ref = bound_reference(
      "ACTION-TEST-001",
      "TITMAS_SCOUT_ACTION",
      "0.1-prototype",
      "4"
    )
    action_request_ref = bound_reference(
      "REQUEST-TEST-001",
      "TITMAS_SCOUT_ACTION_REQUEST",
      "0.1",
      "5"
    )
    receipt_ref = bound_reference(
      "RECEIPT-TEST-001",
      "TITMAS_SCOUT_ACTION_RECEIPT",
      "0.1",
      "6"
    )
    source_evidence_ref = bound_reference(
      "SOURCE-EVIDENCE-TEST-001",
      "TITMAS_SCOUT_SOURCE_EVIDENCE",
      "0.1",
      "7"
    )

    {
      "prototype_profile" => "POST_ACTION_CHAIN",
      "opportunity" => {
        "schema_version" => "0.1-draft",
        "id" => "OPP-TEST-001",
        "source" => {
          "type" => "repository",
          "reference" => "https://unresolvable.invalid/source",
          "timestamp" => "2026-08-01T08:00:00Z",
          "content_digest" => "sha256:#{"8" * 64}"
        },
        "problem" => "Synthetic validator test problem; not a customer claim.",
        "domain" => "validator-test",
        "stakeholders" => [{ "role" => "synthetic_test_actor" }],
        "titmas_alignment" => {
          "status" => "ASSESSED",
          "capability_refs" => [],
          "rationale" => "Synthetic test only.",
          "evidence_refs" => []
        },
        "evidence" => [
          {
            "evidence_id" => "DISCOVERY-EVIDENCE-TEST-001",
            "evidence_type" => "synthetic",
            "reference" => "https://unresolvable.invalid/discovery-evidence",
            "observed_at" => "2026-08-01T08:00:00Z",
            "content_digest" => "sha256:#{"9" * 64}"
          }
        ],
        "scoring" => {
          "model_reference" => "docs/matching-score-v0.1.md",
          "reference_status" => "APPLIED",
          "status" => "COMPUTED_UNCALIBRATED",
          "model_version" => "0.1",
          "score_value" => 80,
          "reason_codes" => []
        },
        "recommended_action" => {
          "status" => "NOT_AUTHORIZED",
          "action_type" => "NONE",
          "authoritative" => false,
          "external_action_allowed" => false
        },
        "status" => "accepted"
      },
      "assessment" => {
        "schema_version" => "0.1-prototype",
        "object_type" => "TITMAS_SCOUT_MATCHING_ASSESSMENT",
        "assessment_id" => "ASSESS-TEST-001",
        "opportunity_reference" => Marshal.load(Marshal.dump(opportunity_ref)),
        "model_id" => "TITMAS-SCOUT-MATCHING-SCORE",
        "model_version" => "0.1",
        "reference_status" => "APPLIED",
        "overall_status" => "COMPUTED_UNCALIBRATED",
        "score_value" => 80,
        "evaluated_at" => "2026-08-01T09:00:00Z"
      },
      "approval" => {
        "schema_version" => "0.1-draft",
        "object_type" => "TITMAS_SCOUT_APPROVAL",
        "approval_id" => "APPROVAL-TEST-001",
        "opportunity_reference" => Marshal.load(Marshal.dump(opportunity_ref)),
        "assessment_reference" => assessment_ref,
        "action_request_reference" => Marshal.load(Marshal.dump(action_request_ref)),
        "policy_reference" => bound_reference("POLICY-TEST-001", "TITMAS_SCOUT_ACTION_POLICY", "0.1", "a"),
        "decision" => "APPROVED",
        "authorized_scope" => {
          "subject_ids" => ["EXECUTOR-TEST-001"],
          "target_ids" => ["TARGET-TEST-001"],
          "environment_ids" => ["ENV-TEST-001"],
          "parameter_constraints" => [],
          "max_execution_attempts" => 1,
          "max_successful_executions" => 1
        },
        "allowed_actions" => [
          {
            "action_id" => "ACTION-TEST-001",
            "action_type" => "SYNTHETIC_NO_OP",
            "request_id" => action_request_ref["reference_id"],
            "request_content_digest" => action_request_ref["content_digest"],
            "target_ids" => ["TARGET-TEST-001"],
            "parameter_content_digest" => "sha256:#{"b" * 64}"
          }
        ],
        "blocked_actions" => [],
        "constraints" => [],
        "reviewer" => {
          "reviewer_id" => "HUMAN-TEST-001",
          "reviewer_type" => "HUMAN",
          "role" => "synthetic_test_reviewer",
          "identity_reference" => bound_reference("IDENTITY-TEST-001", "TITMAS_SCOUT_REVIEWER_IDENTITY", "0.1", "c"),
          "authority_reference" => bound_reference("AUTHORITY-TEST-001", "TITMAS_SCOUT_REVIEWER_AUTHORITY", "0.1", "d"),
          "attestation_reference" => bound_reference("ATTESTATION-TEST-001", "TITMAS_SCOUT_REVIEWER_ATTESTATION", "0.1", "e")
        },
        "timestamp" => {
          "decided_at" => "2026-08-01T09:10:00Z",
          "recorded_at" => "2026-08-01T09:11:00Z",
          "valid_from" => "2026-08-01T09:15:00Z",
          "expires_at" => "2026-08-02T00:00:00Z",
          "time_source_reference" => bound_reference("TIME-TEST-001", "TITMAS_SCOUT_TIME_SOURCE", "0.1", "f")
        },
        "evidence_reference" => [Marshal.load(Marshal.dump(source_evidence_ref))],
        "decision_reason_codes" => ["SYNTHETIC_TEST_ONLY"],
        "supersedes_approval_reference" => nil
      },
      "action" => {
        "schema_version" => "0.1-prototype",
        "object_type" => "TITMAS_SCOUT_ACTION",
        "action_id" => "ACTION-TEST-001",
        "opportunity_reference" => Marshal.load(Marshal.dump(opportunity_ref)),
        "approval_reference" => approval_ref,
        "action_request_reference" => Marshal.load(Marshal.dump(action_request_ref)),
        "executor_reference" => bound_reference("EXECUTOR-TEST-001", "TITMAS_SCOUT_EXECUTOR", "0.1", "0"),
        "lifecycle_state" => "COMPLETED",
        "outcome" => "SUCCEEDED",
        "authorized_at" => "2026-08-01T09:16:00Z",
        "started_at" => "2026-08-01T09:17:00Z",
        "completed_at" => "2026-08-01T09:18:00Z",
        "completion_receipt_reference" => Marshal.load(Marshal.dump(receipt_ref)),
        "reason_codes" => ["SYNTHETIC_TEST_ONLY"]
      },
      "outcome_evidence" => {
        "schema_version" => "0.1-prototype",
        "object_type" => "TITMAS_SCOUT_OUTCOME_EVIDENCE",
        "feedback_id" => "FEEDBACK-TEST-001",
        "action_reference" => action_ref,
        "completion_receipt_reference" => Marshal.load(Marshal.dump(receipt_ref)),
        "opportunity_reference" => Marshal.load(Marshal.dump(opportunity_ref)),
        "observed_at" => "2026-08-01T09:19:00Z",
        "source_evidence_ref" => Marshal.load(Marshal.dump(source_evidence_ref)),
        "ground_truth_source" => nil,
        "subject_refs" => [bound_reference("SUBJECT-TEST-001", "TITMAS_SCOUT_SUBJECT", "0.1", "a")],
        "evidence_status" => "INSUFFICIENT_EVIDENCE",
        "reason_codes" => ["NO_GROUND_TRUTH_SOURCE"]
      }
    }
  end
end
