# frozen_string_literal: true

require "minitest/autorun"
require_relative "../src/integrations/titmas_feedback_loop"

class TitmasFeedbackLoopTest < Minitest::Test
  def setup
    @feedback = TITMASScout::Integrations::TitmasFeedbackLoop.new
  end

  def test_action_required_is_external_policy_blocker
    result = @feedback.classify_workflow("conclusion" => "ACTION_REQUIRED", "name" => "CI")
    assert_equal "EXTERNAL_POLICY_BLOCKER", result
  end

  def test_test_failure_is_code_failure
    result = @feedback.classify_workflow("conclusion" => "FAILURE", "name" => "pytest")
    assert_equal "CODE_FAILURE", result
  end

  def test_merge_conflict_blocks
    assert_equal "BLOCKED_BY_CONFLICT",
                 @feedback.classify_mergeability(mergeable: false, conflict: true)
  end

  def test_unknown_mergeability_needs_refresh
    assert_equal "NEEDS_REFRESH", @feedback.classify_mergeability(mergeable: "UNKNOWN")
  end

  def test_old_review_sha_is_stale
    assert_equal "STALE_REVIEW", @feedback.classify_review(
      reviewed_sha: "old", current_head: "new", review_requested: false
    )
  end

  def test_requested_review_without_submission_is_pending
    assert_equal "PENDING_REVIEW", @feedback.classify_review(
      reviewed_sha: nil, current_head: "new", review_requested: true
    )
  end
end
