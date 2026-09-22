# frozen_string_literal: true

require_relative "support"

module TITMASScout
  module Validator
    class LifecycleCheck
      def initialize(evaluation_time:)
        @evaluation_time = evaluation_time.utc
      end

      def check(bundle)
        @failures = []
        opportunity = bundle["opportunity"]
        assessment = bundle["assessment"]
        approval = bundle["approval"]
        action = bundle["action"]
        outcome_evidence = bundle["outcome_evidence"]

        check_source_time(opportunity)
        check_assessment_presence_and_time(assessment)
        check_approval_presence(approval)
        return @failures unless approval.is_a?(Hash)

        check_approval_state_and_time(approval, assessment)
        check_action_presence(action)
        return @failures unless action.is_a?(Hash)

        check_action_lifecycle(action, approval)
        check_outcome_evidence_presence(outcome_evidence)
        check_outcome_evidence_lifecycle(outcome_evidence, action) if outcome_evidence.is_a?(Hash)
        @failures
      end

      private

      def check_source_time(opportunity)
        return unless opportunity.is_a?(Hash)

        check_timestamp(opportunity.dig("source", "timestamp"), "$.opportunity.source.timestamp")
        evidence = opportunity["evidence"]
        return unless evidence.is_a?(Array)

        evidence.each_with_index do |item, index|
          next unless item.is_a?(Hash)

          check_timestamp(item["observed_at"], "$.opportunity.evidence[#{index}].observed_at")
        end
      end

      def check_assessment_presence_and_time(assessment)
        unless assessment.is_a?(Hash)
          add_lifecycle_failure(
            "$.assessment",
            "MATCHING_ASSESSMENT_MISSING",
            "A post-action prototype chain requires an explicit matching assessment."
          )
          return
        end
        check_timestamp(assessment["evaluated_at"], "$.assessment.evaluated_at")
      end

      def check_approval_presence(approval)
        return if approval.is_a?(Hash)

        @failures << Support.failure(
          rule_id: "TVP-AUT-001",
          source_design_rule: "TVM-AUT-001",
          severity: "CRITICAL",
          reason_code: "APPROVAL_MISSING",
          path: "$.approval",
          message: "No Approval Object is present; the chain is invalid and no action is allowed."
        )
      end

      def check_approval_state_and_time(approval, assessment)
        unless approval["decision"] == "APPROVED"
          add_lifecycle_failure(
            "$.approval.decision",
            "APPROVAL_NOT_APPROVED",
            "A post-action chain requires the declared Approval decision APPROVED."
          )
        end
        if assessment.is_a?(Hash)
          unless assessment["reference_status"] == "APPLIED" && assessment["overall_status"] == "COMPUTED_UNCALIBRATED"
            add_lifecycle_failure(
              "$.assessment",
              "ASSESSMENT_INCOMPATIBLE_WITH_APPROVAL",
              "Only an APPLIED, COMPUTED_UNCALIBRATED assessment is structurally compatible with APPROVED."
            )
          end
          compare_time_order(
            assessment["evaluated_at"],
            approval.dig("timestamp", "decided_at"),
            "$.approval.timestamp.decided_at",
            "ASSESSMENT_AFTER_APPROVAL"
          )
        end

        timestamp = approval["timestamp"]
        return unless timestamp.is_a?(Hash)

        %w[decided_at recorded_at valid_from expires_at].each do |key|
          check_timestamp(timestamp[key], "$.approval.timestamp.#{key}")
        end
        decided_at = Support.parse_utc(timestamp["decided_at"])
        recorded_at = Support.parse_utc(timestamp["recorded_at"])
        valid_from = Support.parse_utc(timestamp["valid_from"])
        expires_at = Support.parse_utc(timestamp["expires_at"])
        return unless [decided_at, recorded_at, valid_from, expires_at].all?

        unless decided_at <= recorded_at && decided_at <= valid_from && valid_from < expires_at
          add_lifecycle_failure(
            "$.approval.timestamp",
            "APPROVAL_TIMESTAMP_ORDER_INVALID",
            "Approval timestamps must satisfy decided_at <= recorded_at, decided_at <= valid_from < expires_at."
          )
        end
        unless valid_from <= @evaluation_time && @evaluation_time < expires_at
          add_lifecycle_failure(
            "$.approval.timestamp",
            "APPROVAL_NOT_CURRENT",
            "Evaluation time is outside the half-open Approval interval."
          )
        end
      end

      def check_action_presence(action)
        return if action.is_a?(Hash)

        add_lifecycle_failure(
          "$.action",
          "ACTION_MISSING",
          "A post-action prototype chain requires an Action Record."
        )
      end

      def check_action_lifecycle(action, approval)
        unless action["lifecycle_state"] == "COMPLETED"
          add_lifecycle_failure(
            "$.action.lifecycle_state",
            "ACTION_NOT_COMPLETED",
            "Outcome-evidence validation requires Action lifecycle_state COMPLETED."
          )
        end
        unless %w[SUCCEEDED FAILED PARTIAL CANCELLED].include?(action["outcome"])
          add_lifecycle_failure(
            "$.action.outcome",
            "TERMINAL_OUTCOME_MISSING",
            "A completed Action requires one terminal outcome."
          )
        end
        unless action["completion_receipt_reference"].is_a?(Hash)
          add_lifecycle_failure(
            "$.action.completion_receipt_reference",
            "COMPLETION_RECEIPT_MISSING",
            "A completed Action requires a bound completion receipt reference."
          )
        end

        %w[authorized_at started_at completed_at].each do |key|
          check_timestamp(action[key], "$.action.#{key}")
        end
        authorized_at = Support.parse_utc(action["authorized_at"])
        started_at = Support.parse_utc(action["started_at"])
        completed_at = Support.parse_utc(action["completed_at"])
        return unless [authorized_at, started_at, completed_at].all?

        unless authorized_at <= started_at && started_at <= completed_at
          add_lifecycle_failure(
            "$.action",
            "ACTION_TIMESTAMP_ORDER_INVALID",
            "Action timestamps must satisfy authorized_at <= started_at <= completed_at."
          )
        end
        approval_window = approval["timestamp"]
        return unless approval_window.is_a?(Hash)

        valid_from = Support.parse_utc(approval_window["valid_from"])
        expires_at = Support.parse_utc(approval_window["expires_at"])
        return unless valid_from && expires_at

        unless valid_from <= authorized_at && completed_at < expires_at
          add_lifecycle_failure(
            "$.action",
            "ACTION_OUTSIDE_APPROVAL_WINDOW",
            "Action authorization and completion must be inside the Approval interval."
          )
        end
      end

      def check_outcome_evidence_presence(evidence)
        return if evidence.is_a?(Hash)

        @failures << Support.failure(
          rule_id: "TVP-EVD-005",
          source_design_rule: "TVM-EVD-005",
          severity: "HIGH",
          reason_code: "OUTCOME_EVIDENCE_MISSING",
          path: "$.outcome_evidence",
          message: "A completed Action must have an explicit Outcome Evidence record."
        )
      end

      def check_outcome_evidence_lifecycle(evidence, action)
        check_timestamp(evidence["observed_at"], "$.outcome_evidence.observed_at")
        observed_at = Support.parse_utc(evidence["observed_at"])
        completed_at = Support.parse_utc(action["completed_at"])
        return unless observed_at && completed_at
        return if completed_at <= observed_at

        @failures << Support.failure(
          rule_id: "TVP-EVD-005",
          source_design_rule: "TVM-EVD-005",
          severity: "HIGH",
          reason_code: "OUTCOME_EVIDENCE_PRECEDES_COMPLETION",
          path: "$.outcome_evidence.observed_at",
          message: "Outcome evidence cannot be observed before Action completion."
        )
      end

      def check_timestamp(value, path)
        return if Support.utc_seconds?(value)

        add_lifecycle_failure(
          path,
          "INVALID_UTC_TIMESTAMP",
          "Timestamp must be RFC 3339 UTC at whole-second precision with a Z suffix."
        )
      end

      def compare_time_order(earlier_value, later_value, path, reason_code)
        earlier = Support.parse_utc(earlier_value)
        later = Support.parse_utc(later_value)
        return unless earlier && later
        return if earlier <= later

        add_lifecycle_failure(path, reason_code, "Lifecycle timestamps are out of order.")
      end

      def add_lifecycle_failure(path, reason_code, message)
        @failures << Support.failure(
          rule_id: "TVP-LIF-003",
          source_design_rule: "TVM-LIF-003,TVM-LIF-004,TVM-LIF-007",
          severity: "HIGH",
          reason_code: reason_code,
          path: path,
          message: message
        )
      end
    end
  end
end
