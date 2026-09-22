# frozen_string_literal: true

require "minitest/autorun"
require "json"
require "stringio"
require "tempfile"
require_relative "../src/review/cli"
require_relative "../src/review/policy_loader"
require_relative "../src/review/quorum_aggregator"
require_relative "../src/review/review_result"
require_relative "../src/review/review_input"

class AgentReviewAggregatorTest < Minitest::Test
  RUN_ROOT = "reports/review-runs/2026-08-02-ca2a-pr-76-ready"

  def setup
    @policy = TITMASScout::Review::PolicyLoader.load(
      "config/agent-review-policy.yaml"
    )
    @aggregator = TITMASScout::Review::QuorumAggregator.new(@policy)
    @review_input = TITMASScout::Review::ReviewInput.load(
      File.join(RUN_ROOT, "input.json")
    )
  end

  def test_all_pass_allows_agent_action_without_human_review
    result = @aggregator.aggregate(
      valid_reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "ALLOW", result["decision"]
    assert_equal false, result["human_review_required"]
    assert_equal ["MARK_PR_READY_FOR_REVIEW"], result["authorized_actions"]
    assert_empty result["blocked_actions"]
    assert_equal 5, result["reviewers"].length
  end

  def test_missing_reviewer_blocks_by_missing_evidence
    reviews = valid_reviews.reject do |review|
      review["review_role"] == "RISK_REVIEWER"
    end
    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "BLOCKED_BY_MISSING_EVIDENCE", result["decision"]
    assert_includes result["reason_codes"], "MISSING_REVIEWER:RISK_REVIEWER"
    assert_empty result["authorized_actions"]
  end

  def test_conflicting_role_results_block_by_conflict
    duplicate = deep_copy(valid_reviews.first)
    duplicate["review_id"] = "review-duplicate"
    duplicate["agent_identifier"] = "agent-duplicate"
    sign!(duplicate)
    result = @aggregator.aggregate(
      valid_reviews + [duplicate],
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "BLOCKED_BY_CONFLICT", result["decision"]
    assert_includes result["reason_codes"],
                    "CONFLICTING_ROLE_RESULTS:DISCOVERY_REVIEWER"
    assert_equal true, result["human_review_required"]
  end

  def test_unknown_reviewer_decision_denies
    reviews = valid_reviews
    reviews.first["decision"] = "MAYBE"
    sign!(reviews.first)
    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "REVIEW_DECISION_UNKNOWN"
  end

  def test_missing_required_field_denies
    reviews = valid_reviews
    reviews.first.delete("agent_identifier")
    sign!(reviews.first)
    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "AGENT_IDENTIFIER_INVALID"
  end

  def test_blocking_fail_denies
    reviews = valid_reviews
    reviews.last["decision"] = "BLOCKING_FAIL"
    reviews.last["blocking_reasons"] = ["SECRET_DETECTED"]
    sign!(reviews.last)
    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "RISK_REVIEWER:SECRET_DETECTED"
  end

  def test_repository_human_authorship_blocker_requires_human_action
    reviews = valid_reviews
    reviews.last["decision"] = "BLOCKING_FAIL"
    reviews.last["blocking_reasons"] = [
      "HUMAN_REVIEW_REQUIRED:REPOSITORY_PERSON_TO_PERSON_AUTHORSHIP"
    ]
    sign!(reviews.last)
    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_equal true, result["human_review_required"]
    assert_includes result["reason_codes"],
                    "RISK_REVIEWER:HUMAN_REVIEW_REQUIRED:REPOSITORY_PERSON_TO_PERSON_AUTHORSHIP"
  end

  def test_unknown_action_denies
    input = review_input_for("UNKNOWN_WRITE")
    result = @aggregator.aggregate(
      valid_reviews(input_digest: input.digest),
      review_input: input,
      requested_action: "UNKNOWN_WRITE"
    )

    assert_equal "DENY", result["decision"]
    assert_empty result["authorized_actions"]
    assert_equal ["UNKNOWN_WRITE"], result["blocked_actions"]
  end

  def test_human_exception_action_denies_and_requires_human
    input = review_input_for("SIGN_LEGAL_AGREEMENT")
    result = @aggregator.aggregate(
      valid_reviews(input_digest: input.digest),
      review_input: input,
      requested_action: "SIGN_LEGAL_AGREEMENT"
    )

    assert_equal "DENY", result["decision"]
    assert_equal true, result["human_review_required"]
    assert_equal ["SIGN_LEGAL_AGREEMENT"], result["blocked_actions"]
  end

  def test_loaded_policy_is_deeply_immutable
    assert_raises(FrozenError) { @policy.required_reviewers.clear }
    assert_raises(FrozenError) do
      @policy.agent_authorizable_actions << "UNREGISTERED_WRITE"
    end
    assert_equal TITMASScout::Review::ReviewResult::ROLES,
                 @policy.required_reviewers
    assert_equal TITMASScout::Review::PolicyLoader::AGENT_ACTIONS,
                 @policy.agent_authorizable_actions
  end

  def test_empty_quorum_never_allows_after_policy_mutation_attempt
    assert_raises(FrozenError) { @policy.required_reviewers.clear }

    result = @aggregator.aggregate(
      [],
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "BLOCKED_BY_MISSING_EVIDENCE", result["decision"]
    assert_empty result["authorized_actions"]
    assert_equal 5, result["reason_codes"].length
  end

  def test_tampered_output_digest_denies
    reviews = valid_reviews
    reviews.first["output_digest"] = "sha256:#{"0" * 64}"
    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "OUTPUT_DIGEST_MISMATCH"
  end

  def test_different_input_digest_denies_against_loaded_input
    reviews = valid_reviews
    reviews.last["input_digest"] = "sha256:#{"b" * 64}"
    sign!(reviews.last)
    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"],
                    "REVIEW_INPUT_DIGEST_MISMATCH:RISK_REVIEWER"
  end

  def test_reused_agent_identifier_blocks_by_conflict
    reviews = valid_reviews
    reviews.last["agent_identifier"] = reviews.first["agent_identifier"]
    sign!(reviews.last)
    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "BLOCKED_BY_CONFLICT", result["decision"]
    assert result["reason_codes"].any? { |reason| reason.start_with?("REVIEWER_NOT_INDEPENDENT:") }
  end

  def test_replay_is_deterministic_for_review_order
    forward = @aggregator.aggregate(
      valid_reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )
    reverse = @aggregator.aggregate(
      valid_reviews.reverse,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal forward, reverse
    assert_equal JSON.generate(forward), JSON.generate(reverse)
  end

  def test_ca2a_review_run_replays_to_recorded_allow
    root = RUN_ROOT
    input_digest = "sha256:#{Digest::SHA256.file(File.join(root, "input.json")).hexdigest}"
    reviews = Dir[File.join(root, "reviews", "*.json")].sort.map do |path|
      TITMASScout::Review::ReviewResult.load(path)
    end
    assert(reviews.all? do |review|
      review.document["input_digest"] == input_digest &&
        review.errors(policy_version: @policy.policy_version).empty?
    end)

    forward = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )
    reverse = @aggregator.aggregate(
      reviews.reverse,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )
    recorded = JSON.parse(File.read(File.join(root, "decision.json")))

    assert_equal "ALLOW", forward["decision"]
    assert_equal false, forward["human_review_required"]
    assert_equal ["MARK_PR_READY_FOR_REVIEW"], forward["authorized_actions"]
    assert_equal forward, reverse
    assert_equal recorded, forward
  end

  def test_duplicate_json_keys_are_rejected
    Tempfile.create(["duplicate-review", ".json"]) do |file|
      file.write('{"review_id":"one","review_id":"two"}')
      file.flush

      assert_raises(TITMASScout::Review::DuplicateJSONKeyError) do
        TITMASScout::Review::ReviewResult.load(file.path)
      end
    end
  end

  def test_duplicate_review_input_keys_are_rejected
    source = File.read(File.join(RUN_ROOT, "input.json"))
    duplicate = source.sub(
      '"requested_action": "MARK_PR_READY_FOR_REVIEW",',
      '"requested_action": "MARK_PR_READY_FOR_REVIEW",' \
      "\n  \"requested_action\": \"MARK_PR_READY_FOR_REVIEW\","
    )
    Tempfile.create(["duplicate-review-input", ".json"]) do |file|
      file.write(duplicate)
      file.flush

      assert_raises(TITMASScout::Review::DuplicateJSONKeyError) do
        TITMASScout::Review::ReviewInput.load(file.path)
      end
    end
  end

  def test_loaded_review_input_is_deeply_immutable
    assert_raises(FrozenError) do
      @review_input.document["requested_action"] = "POST_BOUNDED_TECHNICAL_COMMENT"
    end
    assert_equal "MARK_PR_READY_FOR_REVIEW", @review_input.requested_action
  end

  def test_loaded_review_result_is_deeply_immutable
    path = Dir[File.join(RUN_ROOT, "reviews", "*.json")].sort.first
    result = TITMASScout::Review::ReviewResult.load(path)

    assert_raises(FrozenError) { result.document["decision"] = "BLOCKING_FAIL" }
    assert_equal "PASS", result.document["decision"]
  end

  def test_missing_evidence_envelope_denies_even_if_all_reviewers_pass
    input = review_input_for("MARK_PR_READY_FOR_REVIEW") do |document|
      %w[
        source_issue duplicate_check pull_request diff local_validation
        github_checks automation risk_evidence history_references known_limits
      ].each { |key| document[key] = nil }
    end
    result = @aggregator.aggregate(
      valid_reviews(input_digest: input.digest),
      review_input: input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"],
                    "REVIEW_EVIDENCE_OBJECT_INVALID:source_issue"
    assert_includes result["reason_codes"],
                    "REVIEW_EVIDENCE_ARRAY_INVALID:github_checks"
    assert_empty result["authorized_actions"]
  end

  def test_content_addressed_evidence_requires_sha256_shape
    input = review_input_for("MARK_PR_READY_FOR_REVIEW") do |document|
      document["diff"]["content_digest"] = "not-a-digest"
      document["local_validation"]["record_digest"] = "not-a-digest"
      document["history_references"].first["content_digest"] = "not-a-digest"
    end
    result = @aggregator.aggregate(
      valid_reviews(input_digest: input.digest),
      review_input: input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "DIFF_CONTENT_DIGEST_INVALID"
    assert_includes result["reason_codes"], "VALIDATION_RECORD_DIGEST_INVALID"
    assert_includes result["reason_codes"], "HISTORY_REFERENCE_INVALID"
  end

  def test_review_results_cannot_be_replayed_for_a_different_allowed_action
    result = @aggregator.aggregate(
      valid_reviews,
      review_input: @review_input,
      requested_action: "POST_BOUNDED_TECHNICAL_COMMENT"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "REQUESTED_ACTION_INPUT_MISMATCH"
  end

  def test_review_digest_must_match_loaded_input_bytes
    other_input = review_input_for("MARK_PR_READY_FOR_REVIEW", run_id: "other-run")
    result = @aggregator.aggregate(
      valid_reviews,
      review_input: other_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert result["reason_codes"].all? do |reason|
      reason.start_with?("REVIEW_INPUT_DIGEST_MISMATCH:")
    end
  end

  def test_missing_review_input_denies
    result = @aggregator.aggregate(
      valid_reviews,
      review_input: nil,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "REVIEW_INPUT_MISSING_OR_INVALID"
  end

  def test_blocking_fail_takes_precedence_over_missing_reviewer
    reviews = valid_reviews.reject do |review|
      review["review_role"] == "RISK_REVIEWER"
    end
    reviews.first["decision"] = "BLOCKING_FAIL"
    reviews.first["blocking_reasons"] = ["OPPORTUNITY_CLOSED"]
    sign!(reviews.first)

    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"],
                    "DISCOVERY_REVIEWER:OPPORTUNITY_CLOSED"
  end

  def test_duplicate_review_id_blocks_by_conflict
    reviews = valid_reviews
    reviews.last["review_id"] = reviews.first["review_id"]
    sign!(reviews.last)

    result = @aggregator.aggregate(
      reviews,
      review_input: @review_input,
      requested_action: "MARK_PR_READY_FOR_REVIEW"
    )

    assert_equal "BLOCKED_BY_CONFLICT", result["decision"]
    assert_includes result["reason_codes"],
                    "DUPLICATE_REVIEW_ID:#{reviews.first['review_id']}"
  end

  def test_duplicate_yaml_keys_are_rejected
    source = File.read("config/agent-review-policy.yaml")
    duplicate = source.sub(
      "default_mode: AGENT_QUORUM",
      "default_mode: AGENT_QUORUM\ndefault_mode: AGENT_QUORUM"
    )
    Tempfile.create(["duplicate-policy", ".yaml"]) do |file|
      file.write(duplicate)
      file.flush

      error = assert_raises(TITMASScout::Review::PolicyError) do
        TITMASScout::Review::PolicyLoader.load(file.path)
      end
      assert_includes error.message, "DUPLICATE_POLICY_KEY:default_mode"
    end
  end

  def test_cli_missing_input_fails_closed
    stdout = StringIO.new
    stderr = StringIO.new
    code = TITMASScout::Review::CLI.run(
      ["--action", "MARK_PR_READY_FOR_REVIEW"],
      stdout: stdout,
      stderr: stderr
    )
    result = JSON.parse(stdout.string)

    assert_equal 2, code
    assert_equal "DENY", result["decision"]
    assert_equal true, result["human_review_required"]
    assert_includes stderr.string, "--input is required"
  end

  def test_cli_rejects_duplicate_action_options
    stdout = StringIO.new
    stderr = StringIO.new
    code = TITMASScout::Review::CLI.run(
      [
        "--action", "MARK_PR_READY_FOR_REVIEW",
        "--action", "POST_BOUNDED_TECHNICAL_COMMENT"
      ],
      stdout: stdout,
      stderr: stderr
    )
    result = JSON.parse(stdout.string)

    assert_equal 2, code
    assert_equal "DENY", result["decision"]
    assert_includes stderr.string, "--action provided more than once"
  end

  private

  def valid_reviews(input_digest: @review_input.digest)
    TITMASScout::Review::ReviewResult::ROLES.each_with_index.map do |role, index|
      document = {
        "schema_version" => "0.1",
        "review_id" => "review-#{index}",
        "agent_identifier" => "agent-#{index}",
        "model_runtime_identifier" => "runtime-#{index}",
        "review_role" => role,
        "input_digest" => input_digest,
        "output_digest" => nil,
        "decision" => "PASS",
        "timestamp" => "2026-08-01T12:00:0#{index}Z",
        "ruleset_version" => "0.1",
        "reason_codes" => ["ROLE_CHECKS_PASS"],
        "findings" => ["Required evidence was checked."],
        "blocking_reasons" => [],
        "evidence_references" => ["review-input.json##{input_digest}"]
      }
      sign!(document)
    end
  end

  def sign!(document)
    document["output_digest"] = TITMASScout::Review::ReviewResult.digest_for(document)
    document
  end

  def deep_copy(value)
    Marshal.load(Marshal.dump(value))
  end

  def review_input_for(action, run_id: "test-run")
    document = JSON.parse(File.read(File.join(RUN_ROOT, "input.json")))
    document["requested_action"] = action
    document["review_run_id"] = run_id
    yield document if block_given?
    bytes = JSON.generate(document)
    Tempfile.create(["review-input", ".json"]) do |file|
      file.binmode
      file.write(bytes)
      file.flush
      return TITMASScout::Review::ReviewInput.load(file.path)
    end
  end
end
