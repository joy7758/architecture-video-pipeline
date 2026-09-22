# frozen_string_literal: true

require_relative "support"

module TITMASScout
  module Validator
    class ReferenceCheck
      BOUND_KEYS = %w[
        reference_id reference_type reference_uri version content_digest
      ].freeze

      REGISTERED_REFERENCE_TYPES = %w[
        TITMAS_SCOUT_OPPORTUNITY
        TITMAS_SCOUT_MATCHING_ASSESSMENT
        TITMAS_SCOUT_APPROVAL
        TITMAS_SCOUT_ACTION
        TITMAS_SCOUT_OUTCOME_EVIDENCE
        TITMAS_SCOUT_ACTION_REQUEST
        TITMAS_SCOUT_ACTION_POLICY
        TITMAS_SCOUT_EXECUTOR
        TITMAS_SCOUT_ACTION_RECEIPT
        TITMAS_SCOUT_SOURCE_EVIDENCE
        TITMAS_SCOUT_SUBJECT
        TITMAS_SCOUT_REVIEWER_IDENTITY
        TITMAS_SCOUT_REVIEWER_AUTHORITY
        TITMAS_SCOUT_REVIEWER_ATTESTATION
        TITMAS_SCOUT_TIME_SOURCE
      ].freeze

      ASSESSMENT_REFERENCE_EXTRA_KEYS = %w[
        model_id model_version reference_status overall_status opportunity_id
        opportunity_content_digest
      ].freeze

      def check(bundle)
        @failures = []
        opportunity = bundle["opportunity"]
        assessment = bundle["assessment"]
        approval = bundle["approval"]
        action = bundle["action"]
        outcome_evidence = bundle["outcome_evidence"]

        check_assessment(assessment, opportunity) if assessment.is_a?(Hash)
        check_approval(approval, opportunity, assessment) if approval.is_a?(Hash)
        check_action(action, opportunity, approval) if action.is_a?(Hash)
        check_outcome_evidence(outcome_evidence, opportunity, approval, action) if outcome_evidence.is_a?(Hash)
        @failures
      end

      private

      def check_assessment(assessment, opportunity)
        reference = assessment["opportunity_reference"]
        check_bound_reference(reference, "$.assessment.opportunity_reference", "TITMAS_SCOUT_OPPORTUNITY")
        return unless reference.is_a?(Hash) && opportunity.is_a?(Hash)

        compare_value(
          reference["reference_id"],
          opportunity["id"],
          "$.assessment.opportunity_reference.reference_id",
          "OPPORTUNITY_REFERENCE_ID_MISMATCH"
        )
        compare_value(
          reference["version"],
          opportunity["schema_version"],
          "$.assessment.opportunity_reference.version",
          "OPPORTUNITY_REFERENCE_VERSION_MISMATCH"
        )
      end

      def check_approval(approval, opportunity, assessment)
        opportunity_ref = approval["opportunity_reference"]
        assessment_ref = approval["assessment_reference"]
        check_bound_reference(opportunity_ref, "$.approval.opportunity_reference", "TITMAS_SCOUT_OPPORTUNITY")
        check_bound_reference(
          assessment_ref,
          "$.approval.assessment_reference",
          "TITMAS_SCOUT_MATCHING_ASSESSMENT",
          ASSESSMENT_REFERENCE_EXTRA_KEYS
        )
        check_bound_reference(approval["action_request_reference"], "$.approval.action_request_reference", "TITMAS_SCOUT_ACTION_REQUEST")
        check_bound_reference(approval["policy_reference"], "$.approval.policy_reference", "TITMAS_SCOUT_ACTION_POLICY")

        if opportunity_ref.is_a?(Hash) && opportunity.is_a?(Hash)
          compare_value(
            opportunity_ref["reference_id"],
            opportunity["id"],
            "$.approval.opportunity_reference.reference_id",
            "OPPORTUNITY_REFERENCE_ID_MISMATCH"
          )
          compare_value(
            opportunity_ref["version"],
            opportunity["schema_version"],
            "$.approval.opportunity_reference.version",
            "OPPORTUNITY_REFERENCE_VERSION_MISMATCH"
          )
        end

        if assessment_ref.is_a?(Hash) && assessment.is_a?(Hash)
          compare_value(assessment_ref["reference_id"], assessment["assessment_id"], "$.approval.assessment_reference.reference_id", "ASSESSMENT_REFERENCE_ID_MISMATCH")
          compare_value(assessment_ref["version"], assessment["schema_version"], "$.approval.assessment_reference.version", "ASSESSMENT_REFERENCE_VERSION_MISMATCH")
          compare_value(assessment_ref["model_id"], assessment["model_id"], "$.approval.assessment_reference.model_id", "ASSESSMENT_MODEL_ID_MISMATCH")
          compare_value(assessment_ref["model_version"], assessment["model_version"], "$.approval.assessment_reference.model_version", "ASSESSMENT_MODEL_VERSION_MISMATCH")
          compare_value(assessment_ref["reference_status"], assessment["reference_status"], "$.approval.assessment_reference.reference_status", "ASSESSMENT_REFERENCE_STATUS_MISMATCH")
          compare_value(assessment_ref["overall_status"], assessment["overall_status"], "$.approval.assessment_reference.overall_status", "ASSESSMENT_STATUS_MISMATCH")
        end

        if opportunity_ref.is_a?(Hash) && assessment_ref.is_a?(Hash)
          compare_value(assessment_ref["opportunity_id"], opportunity_ref["reference_id"], "$.approval.assessment_reference.opportunity_id", "ASSESSMENT_OPPORTUNITY_ID_MISMATCH")
          compare_value(assessment_ref["opportunity_content_digest"], opportunity_ref["content_digest"], "$.approval.assessment_reference.opportunity_content_digest", "ASSESSMENT_OPPORTUNITY_DIGEST_MISMATCH")
        end
        if assessment.is_a?(Hash)
          compare_reference(
            assessment["opportunity_reference"],
            opportunity_ref,
            "$.approval.opportunity_reference",
            "ASSESSMENT_APPROVAL_OPPORTUNITY_LINEAGE_MISMATCH"
          )
        end

        check_reviewer_references(approval["reviewer"])
        check_bound_reference(approval.dig("timestamp", "time_source_reference"), "$.approval.timestamp.time_source_reference", "TITMAS_SCOUT_TIME_SOURCE")
        check_reference_array(approval["evidence_reference"], "$.approval.evidence_reference")
        check_constraints(approval["constraints"])
        if approval["supersedes_approval_reference"]
          check_bound_reference(approval["supersedes_approval_reference"], "$.approval.supersedes_approval_reference", "TITMAS_SCOUT_APPROVAL")
        end
      end

      def check_action(action, opportunity, approval)
        opportunity_ref = action["opportunity_reference"]
        approval_ref = action["approval_reference"]
        request_ref = action["action_request_reference"]
        check_bound_reference(opportunity_ref, "$.action.opportunity_reference", "TITMAS_SCOUT_OPPORTUNITY")
        check_bound_reference(approval_ref, "$.action.approval_reference", "TITMAS_SCOUT_APPROVAL")
        check_bound_reference(request_ref, "$.action.action_request_reference", "TITMAS_SCOUT_ACTION_REQUEST")
        check_bound_reference(action["executor_reference"], "$.action.executor_reference", "TITMAS_SCOUT_EXECUTOR")
        if action["completion_receipt_reference"]
          check_bound_reference(action["completion_receipt_reference"], "$.action.completion_receipt_reference", "TITMAS_SCOUT_ACTION_RECEIPT")
        end

        if opportunity_ref.is_a?(Hash) && opportunity.is_a?(Hash)
          compare_value(opportunity_ref["reference_id"], opportunity["id"], "$.action.opportunity_reference.reference_id", "ACTION_OPPORTUNITY_ID_MISMATCH")
          compare_value(opportunity_ref["version"], opportunity["schema_version"], "$.action.opportunity_reference.version", "ACTION_OPPORTUNITY_VERSION_MISMATCH")
        end
        return unless approval.is_a?(Hash)

        compare_value(approval_ref["reference_id"], approval["approval_id"], "$.action.approval_reference.reference_id", "ACTION_APPROVAL_ID_MISMATCH") if approval_ref.is_a?(Hash)
        compare_value(approval_ref["version"], approval["schema_version"], "$.action.approval_reference.version", "ACTION_APPROVAL_VERSION_MISMATCH") if approval_ref.is_a?(Hash)
        compare_reference(opportunity_ref, approval["opportunity_reference"], "$.action.opportunity_reference", "ACTION_OPPORTUNITY_LINEAGE_MISMATCH")
        compare_reference(request_ref, approval["action_request_reference"], "$.action.action_request_reference", "ACTION_REQUEST_REFERENCE_MISMATCH")
        check_allowed_action_binding(action, approval)
      end

      def check_outcome_evidence(evidence, opportunity, approval, action)
        action_ref = evidence["action_reference"]
        receipt_ref = evidence["completion_receipt_reference"]
        opportunity_ref = evidence["opportunity_reference"]
        source_ref = evidence["source_evidence_ref"]
        check_bound_reference(action_ref, "$.outcome_evidence.action_reference", "TITMAS_SCOUT_ACTION")
        check_bound_reference(receipt_ref, "$.outcome_evidence.completion_receipt_reference", "TITMAS_SCOUT_ACTION_RECEIPT")
        check_bound_reference(opportunity_ref, "$.outcome_evidence.opportunity_reference", "TITMAS_SCOUT_OPPORTUNITY")
        check_bound_reference(source_ref, "$.outcome_evidence.source_evidence_ref", "TITMAS_SCOUT_SOURCE_EVIDENCE")
        check_bound_reference(evidence["ground_truth_source"], "$.outcome_evidence.ground_truth_source") if evidence["ground_truth_source"]
        check_reference_array(evidence["subject_refs"], "$.outcome_evidence.subject_refs", "TITMAS_SCOUT_SUBJECT")

        if action.is_a?(Hash)
          compare_value(action_ref["reference_id"], action["action_id"], "$.outcome_evidence.action_reference.reference_id", "EVIDENCE_ACTION_ID_MISMATCH") if action_ref.is_a?(Hash)
          compare_value(action_ref["version"], action["schema_version"], "$.outcome_evidence.action_reference.version", "EVIDENCE_ACTION_VERSION_MISMATCH") if action_ref.is_a?(Hash)
          compare_reference(receipt_ref, action["completion_receipt_reference"], "$.outcome_evidence.completion_receipt_reference", "EVIDENCE_RECEIPT_REFERENCE_MISMATCH")
          compare_reference(opportunity_ref, action["opportunity_reference"], "$.outcome_evidence.opportunity_reference", "EVIDENCE_OPPORTUNITY_LINEAGE_MISMATCH")
        end
        if opportunity_ref.is_a?(Hash) && opportunity.is_a?(Hash)
          compare_value(opportunity_ref["reference_id"], opportunity["id"], "$.outcome_evidence.opportunity_reference.reference_id", "EVIDENCE_OPPORTUNITY_ID_MISMATCH")
        end
        if approval.is_a?(Hash) && source_ref.is_a?(Hash) && approval["evidence_reference"].is_a?(Array)
          unless approval["evidence_reference"].any? { |item| same_reference?(item, source_ref) }
            add_lineage_failure(
              "$.outcome_evidence.source_evidence_ref",
              "OUTCOME_SOURCE_NOT_IN_APPROVAL_EVIDENCE",
              "Outcome source evidence is not one of the Approval evidence references."
            )
          end
        end
      end

      def check_bound_reference(reference, path, expected_type = nil, extra_keys = [])
        return unless reference.is_a?(Hash)

        unknown = reference.keys - (BOUND_KEYS + extra_keys)
        unknown.sort.each do |key|
          add_reference_failure("#{path}.#{key}", "UNKNOWN_REFERENCE_FIELD", "Unknown bound-reference field.")
        end
        %w[reference_id reference_type reference_uri version content_digest].each do |key|
          unless Support.non_empty_string?(reference[key])
            add_reference_failure("#{path}.#{key}", "REFERENCE_COMPONENT_MISSING", "Bound reference component is missing.")
          end
        end
        unless REGISTERED_REFERENCE_TYPES.include?(reference["reference_type"])
          add_reference_failure("#{path}.reference_type", "UNREGISTERED_REFERENCE_TYPE", "Reference type is not in the prototype registry.")
        end
        if expected_type && reference["reference_type"] != expected_type
          add_reference_failure("#{path}.reference_type", "REFERENCE_TYPE_MISMATCH", "Reference type does not match the required object type.")
        end
        unless immutable_version?(reference["version"])
          add_reference_failure("#{path}.version", "MUTABLE_OR_AMBIGUOUS_VERSION", "Reference version must be exact and immutable-looking.")
        end
        unless Support.sha256?(reference["content_digest"])
          add_reference_failure("#{path}.content_digest", "INVALID_SHA256_DIGEST", "Reference digest must be sha256 plus 64 lowercase hex characters.")
        end
      end

      def check_reference_array(array, path, expected_type = nil)
        return unless array.is_a?(Array)

        array.each_with_index do |reference, index|
          check_bound_reference(reference, "#{path}[#{index}]", expected_type)
        end
      end

      def check_reviewer_references(reviewer)
        return unless reviewer.is_a?(Hash)

        if reviewer["identity_reference"].is_a?(Hash)
          check_bound_reference(reviewer["identity_reference"], "$.approval.reviewer.identity_reference", "TITMAS_SCOUT_REVIEWER_IDENTITY")
        end
        check_bound_reference(reviewer["authority_reference"], "$.approval.reviewer.authority_reference", "TITMAS_SCOUT_REVIEWER_AUTHORITY")
        check_bound_reference(reviewer["attestation_reference"], "$.approval.reviewer.attestation_reference", "TITMAS_SCOUT_REVIEWER_ATTESTATION")
      end

      def check_constraints(constraints)
        return unless constraints.is_a?(Array)

        constraints.each_with_index do |constraint, index|
          next unless constraint.is_a?(Hash)

          check_reference_array(constraint["evidence_references"], "$.approval.constraints[#{index}].evidence_references")
        end
      end

      def check_allowed_action_binding(action, approval)
        allowed_actions = approval["allowed_actions"]
        return unless allowed_actions.is_a?(Array)

        matching = allowed_actions.select { |item| item.is_a?(Hash) && item["action_id"] == action["action_id"] }
        if matching.length != 1
          add_lineage_failure("$.approval.allowed_actions", "ACTION_NOT_EXACTLY_ONCE_ALLOWLISTED", "Action ID must occur exactly once in allowed_actions.")
          return
        end
        item = matching.first
        request = approval["action_request_reference"]
        return unless request.is_a?(Hash)

        compare_value(item["request_id"], request["reference_id"], "$.approval.allowed_actions", "ALLOWED_ACTION_REQUEST_ID_MISMATCH")
        compare_value(item["request_content_digest"], request["content_digest"], "$.approval.allowed_actions", "ALLOWED_ACTION_REQUEST_DIGEST_MISMATCH")
      end

      def immutable_version?(value)
        Support.non_empty_string?(value) && value !~ /(?:latest|[\*\^~<>])/i
      end

      def compare_reference(actual, expected, path, reason_code)
        return unless actual.is_a?(Hash) && expected.is_a?(Hash)
        return if same_reference?(actual, expected)

        add_lineage_failure(path, reason_code, "Bound references do not identify the same immutable snapshot.")
      end

      def same_reference?(left, right)
        left.is_a?(Hash) && right.is_a?(Hash) && BOUND_KEYS.all? { |key| left[key] == right[key] }
      end

      def compare_value(actual, expected, path, reason_code)
        return if actual == expected && !actual.nil?

        add_lineage_failure(path, reason_code, "Reference value does not match the linked object or lineage.")
      end

      def add_reference_failure(path, reason_code, message)
        @failures << Support.failure(
          rule_id: "TVP-REF-001",
          source_design_rule: "TVM-REF-001",
          severity: "HIGH",
          reason_code: reason_code,
          path: path,
          message: message
        )
      end

      def add_lineage_failure(path, reason_code, message)
        @failures << Support.failure(
          rule_id: "TVP-REF-004",
          source_design_rule: "TVM-REF-004",
          severity: "HIGH",
          reason_code: reason_code,
          path: path,
          message: message
        )
      end
    end
  end
end
