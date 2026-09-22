# frozen_string_literal: true

module TITMASScout
  module Integrations
    class TitmasFeedbackLoop
      def classify_workflow(check)
        conclusion = check["conclusion"].to_s.upcase
        name = [check["name"], check["workflow_name"]].join(" ").downcase
        message = check["message"].to_s.downcase

        return "EXTERNAL_POLICY_BLOCKER" if conclusion == "ACTION_REQUIRED"
        if conclusion == "FAILURE" && (name.include?("maintainer") || message.include?("maintainer approval"))
          return "EXTERNAL_POLICY_BLOCKER"
        end
        return "CODE_FAILURE" if conclusion == "FAILURE"
        return "PASS" if conclusion == "SUCCESS"
        return "PENDING" if %w[QUEUED IN_PROGRESS PENDING].include?(conclusion)

        "UNKNOWN"
      end

      def classify_mergeability(mergeable:, conflict: false)
        return "BLOCKED_BY_CONFLICT" if conflict || mergeable.to_s.upcase == "CONFLICTING"
        return "NEEDS_REFRESH" if mergeable.nil? || mergeable.to_s.upcase == "UNKNOWN"
        return "MERGEABLE" if [true, "MERGEABLE"].include?(mergeable)
        return "NOT_MERGEABLE" if [false, "UNMERGEABLE"].include?(mergeable)

        "NEEDS_REFRESH"
      end

      def classify_review(reviewed_sha:, current_head:, review_requested:)
        return "STALE_REVIEW" if reviewed_sha && reviewed_sha != current_head
        return "LATEST_REVIEW_PRESENT" if reviewed_sha == current_head
        return "PENDING_REVIEW" if review_requested

        "REVIEW_NOT_REQUESTED"
      end

      def analyze(observation)
        {
          "workflow_classifications" => Array(observation["checks"]).map do |check|
            { "name" => check["name"], "classification" => classify_workflow(check) }
          end,
          "mergeability_classification" => classify_mergeability(
            mergeable: observation["mergeable"], conflict: observation["merge_conflict"] == true
          ),
          "review_classification" => classify_review(
            reviewed_sha: observation["reviewed_sha"],
            current_head: observation["current_head"],
            review_requested: observation["review_requested"] == true
          )
        }
      end
    end
  end
end
