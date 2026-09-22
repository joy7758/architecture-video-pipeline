# frozen_string_literal: true

require_relative "review_result"
require_relative "review_input"

module TITMASScout
  module Review
    class QuorumAggregator
      DECISIONS = %w[
        ALLOW
        DENY
        BLOCKED_BY_MISSING_EVIDENCE
        BLOCKED_BY_CONFLICT
      ].freeze

      def initialize(policy)
        @policy = policy
      end

      def aggregate(review_documents, review_input:, requested_action:)
        actions = [requested_action.to_s].reject(&:empty?)
        input_errors = if review_input.is_a?(ReviewInput)
                         review_input.errors(policy_version: policy.policy_version)
                       else
                         ["REVIEW_INPUT_MISSING_OR_INVALID"]
                       end
        unless input_errors.empty?
          return decision("DENY", actions, [], input_errors)
        end
        unless requested_action == review_input.requested_action
          return decision("DENY", actions, [], ["REQUESTED_ACTION_INPUT_MISMATCH"])
        end

        results = Array(review_documents).map do |item|
          item.is_a?(ReviewResult) ? item : ReviewResult.new(item)
        end
        valid_results, invalid_results = results.partition do |result|
          result.errors(policy_version: policy.policy_version).empty?
        end
        summaries = ordered_summaries(valid_results)

        return decision("DENY", actions, summaries, ["ACTION_REQUEST_MISSING"]) if actions.empty?

        agent_actions = PolicyLoader::AGENT_ACTIONS
        human_exception_actions = PolicyLoader::HUMAN_ACTIONS
        required_reviewers = ReviewResult::ROLES
        unknown_actions = actions - agent_actions - human_exception_actions
        if unknown_actions.any?
          return decision(
            "DENY", actions, summaries,
            unknown_actions.map { |action| "UNKNOWN_ACTION:#{action}" }
          )
        end

        human_actions = actions & human_exception_actions
        if human_actions.any?
          return decision(
            "DENY", actions, summaries,
            human_actions.map { |action| "HUMAN_EXCEPTION_ACTION:#{action}" },
            human_review_required: true
          )
        end

        if invalid_results.any?
          reasons = invalid_results.flat_map do |result|
            result.errors(policy_version: policy.policy_version)
          end
          return decision("DENY", actions, summaries, reasons)
        end

        mismatched_inputs = valid_results.reject do |result|
          result.document["input_digest"] == review_input.digest
        end
        if mismatched_inputs.any?
          reasons = mismatched_inputs.map do |result|
            "REVIEW_INPUT_DIGEST_MISMATCH:#{result.document['review_role']}"
          end
          return decision("DENY", actions, summaries, reasons)
        end

        blocking = valid_results.select { |result| result.document["decision"] == "BLOCKING_FAIL" }
        if blocking.any?
          reasons = blocking.flat_map do |result|
            result.document["blocking_reasons"].map do |reason|
              "#{result.document['review_role']}:#{reason}"
            end
          end
          human_required = blocking.any? do |result|
            result.document["blocking_reasons"].any? do |reason|
              reason.start_with?("HUMAN_REVIEW_REQUIRED:")
            end
          end
          return decision(
            "DENY", actions, summaries, reasons,
            human_review_required: human_required
          )
        end

        grouped = valid_results.group_by { |result| result.document["review_role"] }
        duplicate_roles = grouped.select { |_role, items| items.length != 1 }.keys
        duplicate_agents = duplicate_values(valid_results, "agent_identifier")
        duplicate_review_ids = duplicate_values(valid_results, "review_id")
        input_digests = valid_results.map { |result| result.document["input_digest"] }.uniq
        if duplicate_roles.any? || duplicate_agents.any? || duplicate_review_ids.any? || input_digests.length > 1
          reasons = duplicate_roles.map { |role| "CONFLICTING_ROLE_RESULTS:#{role}" }
          reasons.concat(duplicate_agents.map { |agent| "REVIEWER_NOT_INDEPENDENT:#{agent}" })
          reasons.concat(duplicate_review_ids.map { |id| "DUPLICATE_REVIEW_ID:#{id}" })
          reasons << "CONFLICTING_INPUT_DIGESTS" if input_digests.length > 1
          return decision(
            "BLOCKED_BY_CONFLICT", actions, summaries, reasons,
            human_review_required: true
          )
        end

        missing = required_reviewers - grouped.keys
        if missing.any?
          return decision(
            "BLOCKED_BY_MISSING_EVIDENCE", actions, summaries,
            missing.map { |role| "MISSING_REVIEWER:#{role}" }
          )
        end

        decision("ALLOW", actions, summaries, ["ALL_REQUIRED_REVIEWERS_PASS"])
      end

      def self.fail_closed_result(actions:, reason:, ruleset_version: "UNKNOWN")
        deep_sort(
          {
            "authorized_actions" => [],
            "blocked_actions" => Array(actions).map(&:to_s).uniq.sort,
            "decision" => "DENY",
            "human_review_required" => true,
            "reason_codes" => [reason.to_s],
            "reviewers" => [],
            "ruleset_version" => ruleset_version
          }
        )
      end

      def self.deep_sort(value)
        ReviewResult.deep_sort(value)
      end

      private

      attr_reader :policy

      def decision(value, actions, reviewers, reasons, human_review_required: false)
        raise ArgumentError, "unknown aggregate decision" unless DECISIONS.include?(value)

        allowed = value == "ALLOW" ? actions : []
        blocked = value == "ALLOW" ? [] : actions
        self.class.deep_sort(
          {
            "authorized_actions" => allowed,
            "blocked_actions" => blocked,
            "decision" => value,
            "human_review_required" => human_review_required,
            "reason_codes" => reasons.uniq.sort,
            "reviewers" => reviewers,
            "ruleset_version" => policy.policy_version
          }
        )
      end

      def ordered_summaries(results)
        order = ReviewResult::ROLES.each_with_index.to_h
        results.map(&:summary).sort_by do |summary|
          [
            order.fetch(summary["review_role"], 99),
            summary["agent_identifier"].to_s,
            summary["output_digest"].to_s
          ]
        end
      end

      def duplicate_values(results, key)
        results.map { |result| result.document[key] }
               .group_by(&:itself)
               .select { |_value, items| items.length > 1 }
               .keys
               .sort
      end
    end
  end
end
