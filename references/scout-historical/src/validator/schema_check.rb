# frozen_string_literal: true

require_relative "support"

module TITMASScout
  module Validator
    class SchemaCheck
      ROOT_KEYS = %w[
        prototype_profile opportunity assessment approval action outcome_evidence
      ].freeze

      OPPORTUNITY_KEYS = %w[
        _meta schema_version id source problem domain stakeholders
        titmas_alignment evidence scoring validation recommended_action status
        truth_boundary
      ].freeze

      ASSESSMENT_KEYS = %w[
        schema_version object_type assessment_id opportunity_reference model_id
        model_version reference_status overall_status score_value evaluated_at
      ].freeze

      APPROVAL_KEYS = %w[
        schema_version object_type approval_id opportunity_reference
        assessment_reference action_request_reference policy_reference decision
        authorized_scope allowed_actions blocked_actions constraints reviewer
        timestamp evidence_reference decision_reason_codes
        supersedes_approval_reference
      ].freeze

      ACTION_KEYS = %w[
        schema_version object_type action_id opportunity_reference
        approval_reference action_request_reference executor_reference
        lifecycle_state outcome authorized_at started_at completed_at
        completion_receipt_reference reason_codes
      ].freeze

      OUTCOME_EVIDENCE_KEYS = %w[
        schema_version object_type feedback_id action_reference
        completion_receipt_reference opportunity_reference observed_at
        source_evidence_ref ground_truth_source subject_refs evidence_status
        reason_codes
      ].freeze

      AUTHORIZED_SCOPE_KEYS = %w[
        subject_ids target_ids environment_ids parameter_constraints
        max_execution_attempts max_successful_executions
      ].freeze
      ALLOWED_ACTION_KEYS = %w[
        action_id action_type request_id request_content_digest target_ids
        parameter_content_digest
      ].freeze
      BLOCKED_ACTION_KEYS = %w[action_type target_ids reason_code].freeze
      CONSTRAINT_KEYS = %w[
        constraint_id enforcement selector operator expected evidence_references
      ].freeze
      PARAMETER_CONSTRAINT_KEYS = %w[selector operator expected].freeze
      REVIEWER_KEYS = %w[
        reviewer_id type reviewer_type role agent_reviews identity_reference
        authority_reference attestation_reference
      ].freeze
      AGENT_REVIEW_KEYS = %w[
        agent_identifier model_runtime_identifier review_role input_digest
        output_digest decision timestamp ruleset_version
      ].freeze
      REVIEWER_TYPES = %w[AGENT AGENT_QUORUM HUMAN ORGANIZATION_POLICY].freeze
      AGENT_REVIEW_ROLES = %w[
        DISCOVERY_REVIEWER EVIDENCE_REVIEWER SCOPE_REVIEWER QUALITY_REVIEWER
        RISK_REVIEWER
      ].freeze
      APPROVAL_TIMESTAMP_KEYS = %w[
        decided_at recorded_at valid_from expires_at time_source_reference
      ].freeze

      OPPORTUNITY_STATUSES = %w[discovered reviewed accepted rejected].freeze
      SOURCE_TYPES = %w[
        repository standard issue publication customer_declaration other
      ].freeze
      SCORING_STATUSES = %w[
        NOT_COMPUTABLE BLOCKED COMPUTED_UNCALIBRATED
      ].freeze
      REFERENCE_STATUSES = %w[UNVERIFIED APPLIED].freeze
      ASSESSMENT_STATUSES = SCORING_STATUSES
      APPROVAL_DECISIONS = %w[APPROVED REJECTED DEFERRED EXPIRED].freeze
      ACTION_STATES = %w[AUTHORIZED RUNNING COMPLETED].freeze
      ACTION_OUTCOMES = %w[SUCCEEDED FAILED PARTIAL CANCELLED].freeze
      EVIDENCE_STATUSES = %w[
        SUFFICIENT INSUFFICIENT_EVIDENCE REJECTED
      ].freeze

      def check(bundle)
        @failures = []
        unless bundle.is_a?(Hash)
          add_schema_failure("$", "INPUT_NOT_OBJECT", "Input must be a YAML mapping.")
          return @failures
        end

        reject_unknown_keys(bundle, ROOT_KEYS, "$")
        enum(bundle, "prototype_profile", ["POST_ACTION_CHAIN"], "$")

        opportunity = bundle["opportunity"]
        unless opportunity.is_a?(Hash)
          add_schema_failure("$.opportunity", "OPPORTUNITY_MISSING", "Opportunity must be an object.")
          return @failures
        end

        check_opportunity(opportunity)
        check_assessment(bundle["assessment"]) if bundle.key?("assessment")
        check_approval(bundle["approval"]) if bundle.key?("approval")
        check_action(bundle["action"]) if bundle.key?("action")
        check_outcome_evidence(bundle["outcome_evidence"]) if bundle.key?("outcome_evidence")
        @failures
      end

      private

      def check_opportunity(object)
        reject_unknown_keys(object, OPPORTUNITY_KEYS, "$.opportunity")
        required_string(object, "schema_version", "$.opportunity")
        unless object["schema_version"] == "0.1-draft"
          add_enum_failure("$.opportunity.schema_version", "UNSUPPORTED_SCHEMA_VERSION")
        end
        required_string(object, "id", "$.opportunity")
        required_string(object, "problem", "$.opportunity")
        required_string(object, "domain", "$.opportunity")
        enum(object, "status", OPPORTUNITY_STATUSES, "$.opportunity")

        source = required_hash(object, "source", "$.opportunity")
        if source
          required_string(source, "reference", "$.opportunity.source")
          required_string(source, "timestamp", "$.opportunity.source")
          required_string(source, "content_digest", "$.opportunity.source")
          enum(source, "type", SOURCE_TYPES, "$.opportunity.source")
          check_digest(source["content_digest"], "$.opportunity.source.content_digest")
        end

        stakeholders = required_array(object, "stakeholders", "$.opportunity", allow_empty: false)
        stakeholders&.each_with_index do |stakeholder, index|
          unless stakeholder.is_a?(Hash) && Support.non_empty_string?(stakeholder["role"])
            add_schema_failure(
              "$.opportunity.stakeholders[#{index}]",
              "STAKEHOLDER_ROLE_MISSING",
              "Each stakeholder must be an object with a non-empty role."
            )
          end
        end

        required_hash(object, "titmas_alignment", "$.opportunity")
        check_discovery_evidence(object)
        check_scoring(object)
        check_recommended_action(object)
      end

      def check_discovery_evidence(object)
        evidence = object["evidence"]
        unless evidence.is_a?(Array) && !evidence.empty?
          @failures << Support.failure(
            rule_id: "TVP-EVD-001",
            source_design_rule: "TVM-EVD-004",
            severity: "HIGH",
            reason_code: "DISCOVERY_EVIDENCE_MISSING",
            path: "$.opportunity.evidence",
            message: "Opportunity discovery evidence must contain at least one item."
          )
          return
        end

        evidence.each_with_index do |item, index|
          path = "$.opportunity.evidence[#{index}]"
          unless item.is_a?(Hash)
            add_schema_failure(path, "DISCOVERY_EVIDENCE_NOT_OBJECT", "Evidence item must be an object.")
            next
          end
          %w[evidence_id reference observed_at content_digest].each do |key|
            required_string(item, key, path)
          end
          check_digest(item["content_digest"], "#{path}.content_digest")
        end
      end

      def check_scoring(object)
        scoring = required_hash(object, "scoring", "$.opportunity")
        return unless scoring

        enum(scoring, "status", SCORING_STATUSES, "$.opportunity.scoring")
        if scoring.key?("reference_status")
          enum(scoring, "reference_status", REFERENCE_STATUSES, "$.opportunity.scoring")
        end
        if scoring["status"] == "NOT_COMPUTABLE" && !scoring["score_value"].nil?
          add_cross_field_failure(
            "$.opportunity.scoring.score_value",
            "NOT_COMPUTABLE_HAS_SCORE",
            "NOT_COMPUTABLE requires score_value to be null."
          )
        elsif scoring["status"] == "COMPUTED_UNCALIBRATED" && !scoring["score_value"].is_a?(Numeric)
          add_cross_field_failure(
            "$.opportunity.scoring.score_value",
            "COMPUTED_SCORE_MISSING",
            "COMPUTED_UNCALIBRATED requires a numeric score_value."
          )
        end
      end

      def check_recommended_action(object)
        action = required_hash(object, "recommended_action", "$.opportunity")
        return unless action

        unless action["external_action_allowed"] == false
          add_cross_field_failure(
            "$.opportunity.recommended_action.external_action_allowed",
            "OPPORTUNITY_ACTION_FLAG_NOT_FALSE",
            "Opportunity recommended_action must keep external_action_allowed false."
          )
        end
        unless action["status"] == "NOT_AUTHORIZED"
          add_cross_field_failure(
            "$.opportunity.recommended_action.status",
            "RECOMMENDED_ACTION_STATUS_NOT_SAFE",
            "Opportunity recommended_action status must be NOT_AUTHORIZED."
          )
        end
        if action.key?("authoritative") && action["authoritative"] != false
          add_cross_field_failure(
            "$.opportunity.recommended_action.authoritative",
            "RECOMMENDATION_MARKED_AUTHORITATIVE",
            "Opportunity recommended_action must be explicitly non-authoritative."
          )
        end
      end

      def check_assessment(object)
        unless object.is_a?(Hash)
          add_schema_failure("$.assessment", "ASSESSMENT_NOT_OBJECT", "Assessment must be an object.")
          return
        end
        reject_unknown_keys(object, ASSESSMENT_KEYS, "$.assessment")
        %w[schema_version object_type assessment_id model_id model_version evaluated_at].each do |key|
          required_string(object, key, "$.assessment")
        end
        required_hash(object, "opportunity_reference", "$.assessment")
        enum(object, "reference_status", REFERENCE_STATUSES, "$.assessment")
        enum(object, "overall_status", ASSESSMENT_STATUSES, "$.assessment")
        unless object["object_type"] == "TITMAS_SCOUT_MATCHING_ASSESSMENT"
          add_enum_failure("$.assessment.object_type", "UNKNOWN_OBJECT_TYPE")
        end
        unless object["schema_version"] == "0.1-prototype"
          add_enum_failure("$.assessment.schema_version", "UNSUPPORTED_PROTOTYPE_SCHEMA_VERSION")
        end
        if object["overall_status"] == "COMPUTED_UNCALIBRATED" && !object["score_value"].is_a?(Numeric)
          add_cross_field_failure("$.assessment.score_value", "ASSESSMENT_SCORE_MISSING", "Computed assessment requires a numeric score.")
        elsif %w[NOT_COMPUTABLE BLOCKED].include?(object["overall_status"]) && !object["score_value"].nil?
          add_cross_field_failure("$.assessment.score_value", "ASSESSMENT_SCORE_MUST_BE_NULL", "Non-computed assessment requires a null score.")
        end
      end

      def check_approval(object)
        unless object.is_a?(Hash)
          add_schema_failure("$.approval", "APPROVAL_NOT_OBJECT", "Approval must be an object.")
          return
        end
        reject_unknown_keys(object, APPROVAL_KEYS, "$.approval")
        %w[schema_version object_type approval_id].each do |key|
          required_string(object, key, "$.approval")
        end
        unless object["schema_version"] == "0.1-draft"
          add_enum_failure("$.approval.schema_version", "UNSUPPORTED_SCHEMA_VERSION")
        end
        unless object["object_type"] == "TITMAS_SCOUT_APPROVAL"
          add_enum_failure("$.approval.object_type", "UNKNOWN_OBJECT_TYPE")
        end
        approval_objects = %w[
          opportunity_reference assessment_reference action_request_reference
          policy_reference authorized_scope reviewer timestamp
        ]
        approval_objects.each { |key| required_hash(object, key, "$.approval") }
        approval_arrays = %w[
          allowed_actions blocked_actions constraints evidence_reference
          decision_reason_codes
        ]
        approval_arrays.each { |key| required_array(object, key, "$.approval") }
        enum(object, "decision", APPROVAL_DECISIONS, "$.approval")
        unless object.key?("supersedes_approval_reference")
          add_schema_failure("$.approval.supersedes_approval_reference", "REQUIRED_NULLABLE_FIELD_MISSING", "Required nullable field is missing.")
        end
        check_authorized_scope(object["authorized_scope"])
        check_allowed_actions(object["allowed_actions"], object["decision"])
        check_blocked_actions(object["blocked_actions"])
        check_constraints_shape(object["constraints"])
        check_reviewer(object["reviewer"])
        check_approval_timestamp(object["timestamp"])
        if object["decision"] == "APPROVED"
          required_array(object, "evidence_reference", "$.approval", allow_empty: false)
          required_array(object, "decision_reason_codes", "$.approval", allow_empty: false)
        end
      end

      def check_action(object)
        unless object.is_a?(Hash)
          add_schema_failure("$.action", "ACTION_NOT_OBJECT", "Action must be an object.")
          return
        end
        reject_unknown_keys(object, ACTION_KEYS, "$.action")
        %w[schema_version object_type action_id authorized_at].each do |key|
          required_string(object, key, "$.action")
        end
        unless object["object_type"] == "TITMAS_SCOUT_ACTION"
          add_enum_failure("$.action.object_type", "UNKNOWN_OBJECT_TYPE")
        end
        unless object["schema_version"] == "0.1-prototype"
          add_enum_failure("$.action.schema_version", "UNSUPPORTED_PROTOTYPE_SCHEMA_VERSION")
        end
        %w[
          opportunity_reference approval_reference action_request_reference
          executor_reference
        ].each { |key| required_hash(object, key, "$.action") }
        required_array(object, "reason_codes", "$.action")
        enum(object, "lifecycle_state", ACTION_STATES, "$.action")
        if object["outcome"] && !ACTION_OUTCOMES.include?(object["outcome"])
          add_enum_failure("$.action.outcome", "UNKNOWN_ACTION_OUTCOME")
        end
      end

      def check_outcome_evidence(object)
        unless object.is_a?(Hash)
          add_schema_failure("$.outcome_evidence", "OUTCOME_EVIDENCE_NOT_OBJECT", "Outcome evidence must be an object.")
          return
        end
        reject_unknown_keys(object, OUTCOME_EVIDENCE_KEYS, "$.outcome_evidence")
        %w[schema_version object_type feedback_id observed_at].each do |key|
          required_string(object, key, "$.outcome_evidence")
        end
        unless object["object_type"] == "TITMAS_SCOUT_OUTCOME_EVIDENCE"
          add_enum_failure("$.outcome_evidence.object_type", "UNKNOWN_OBJECT_TYPE")
        end
        unless object["schema_version"] == "0.1-prototype"
          add_enum_failure("$.outcome_evidence.schema_version", "UNSUPPORTED_PROTOTYPE_SCHEMA_VERSION")
        end
        %w[
          action_reference completion_receipt_reference opportunity_reference
          source_evidence_ref
        ].each { |key| required_hash(object, key, "$.outcome_evidence") }
        required_array(object, "subject_refs", "$.outcome_evidence", allow_empty: false)
        required_array(object, "reason_codes", "$.outcome_evidence")
        enum(object, "evidence_status", EVIDENCE_STATUSES, "$.outcome_evidence")
        unless object.key?("ground_truth_source")
          add_schema_failure("$.outcome_evidence.ground_truth_source", "REQUIRED_NULLABLE_FIELD_MISSING", "Required nullable field is missing.")
        end
      end

      def check_authorized_scope(scope)
        return unless scope.is_a?(Hash)

        reject_unknown_keys(scope, AUTHORIZED_SCOPE_KEYS, "$.approval.authorized_scope")
        %w[subject_ids target_ids environment_ids].each do |key|
          required_array(scope, key, "$.approval.authorized_scope", allow_empty: false)
        end
        constraints = required_array(scope, "parameter_constraints", "$.approval.authorized_scope")
        constraints&.each_with_index do |constraint, index|
          check_parameter_constraint(constraint, "$.approval.authorized_scope.parameter_constraints[#{index}]")
        end
        attempts = required_nonnegative_integer(scope, "max_execution_attempts", "$.approval.authorized_scope")
        successes = required_nonnegative_integer(scope, "max_successful_executions", "$.approval.authorized_scope")
        if attempts && successes && successes > attempts
          add_cross_field_failure(
            "$.approval.authorized_scope",
            "SUCCESS_LIMIT_EXCEEDS_ATTEMPT_LIMIT",
            "max_successful_executions cannot exceed max_execution_attempts."
          )
        end
      end

      def check_allowed_actions(actions, decision)
        return unless actions.is_a?(Array)

        if decision == "APPROVED" && actions.empty?
          add_schema_failure("$.approval.allowed_actions", "APPROVED_WITHOUT_ALLOWED_ACTION", "APPROVED requires at least one explicitly allowed action.")
        end
        actions.each_with_index do |action, index|
          path = "$.approval.allowed_actions[#{index}]"
          unless action.is_a?(Hash)
            add_schema_failure(path, "ALLOWED_ACTION_NOT_OBJECT", "Allowed action must be an object.")
            next
          end
          reject_unknown_keys(action, ALLOWED_ACTION_KEYS, path)
          %w[action_id action_type request_id request_content_digest parameter_content_digest].each do |key|
            required_string(action, key, path)
          end
          required_array(action, "target_ids", path, allow_empty: false)
          check_digest(action["request_content_digest"], "#{path}.request_content_digest")
          check_digest(action["parameter_content_digest"], "#{path}.parameter_content_digest")
        end
      end

      def check_blocked_actions(actions)
        return unless actions.is_a?(Array)

        actions.each_with_index do |action, index|
          path = "$.approval.blocked_actions[#{index}]"
          unless action.is_a?(Hash)
            add_schema_failure(path, "BLOCKED_ACTION_NOT_OBJECT", "Blocked action must be an object.")
            next
          end
          reject_unknown_keys(action, BLOCKED_ACTION_KEYS, path)
          %w[action_type reason_code].each { |key| required_string(action, key, path) }
          required_array(action, "target_ids", path, allow_empty: false)
        end
      end

      def check_constraints_shape(constraints)
        return unless constraints.is_a?(Array)

        constraints.each_with_index do |constraint, index|
          path = "$.approval.constraints[#{index}]"
          unless constraint.is_a?(Hash)
            add_schema_failure(path, "CONSTRAINT_NOT_OBJECT", "Constraint must be an object.")
            next
          end
          reject_unknown_keys(constraint, CONSTRAINT_KEYS, path)
          %w[constraint_id enforcement selector operator].each do |key|
            required_string(constraint, key, path)
          end
          unless constraint["enforcement"] == "HARD"
            add_enum_failure("#{path}.enforcement", "UNKNOWN_CONSTRAINT_ENFORCEMENT")
          end
          enum(constraint, "operator", %w[EQUALS IN LTE GTE DIGEST_EQUALS], path)
          required_array(constraint, "evidence_references", path, allow_empty: false)
          unless constraint.key?("expected")
            add_schema_failure("#{path}.expected", "CONSTRAINT_EXPECTED_MISSING", "Constraint expected value is required.")
          end
        end
      end

      def check_parameter_constraint(constraint, path)
        unless constraint.is_a?(Hash)
          add_schema_failure(path, "PARAMETER_CONSTRAINT_NOT_OBJECT", "Parameter constraint must be an object.")
          return
        end
        reject_unknown_keys(constraint, PARAMETER_CONSTRAINT_KEYS, path)
        required_string(constraint, "selector", path)
        enum(constraint, "operator", %w[EQUALS IN LTE GTE DIGEST_EQUALS], path)
        unless constraint.key?("expected")
          add_schema_failure("#{path}.expected", "PARAMETER_EXPECTED_MISSING", "Parameter expected value is required.")
        end
      end

      def check_reviewer(reviewer)
        return unless reviewer.is_a?(Hash)

        reject_unknown_keys(reviewer, REVIEWER_KEYS, "$.approval.reviewer")
        %w[reviewer_id role].each do |key|
          required_string(reviewer, key, "$.approval.reviewer")
        end
        %w[authority_reference attestation_reference].each do |key|
          required_hash(reviewer, key, "$.approval.reviewer")
        end

        type = reviewer["type"] || reviewer["reviewer_type"]
        if reviewer.key?("type") && reviewer.key?("reviewer_type")
          add_enum_failure("$.approval.reviewer", "CONFLICTING_REVIEWER_TYPE_FIELDS")
        end
        unless REVIEWER_TYPES.include?(type)
          add_enum_failure("$.approval.reviewer.type", "REVIEWER_TYPE_UNKNOWN")
          return
        end

        if %w[AGENT AGENT_QUORUM].include?(type)
          check_agent_reviews(reviewer["agent_reviews"], type)
        else
          required_hash(reviewer, "identity_reference", "$.approval.reviewer")
          if reviewer.key?("agent_reviews") && !Array(reviewer["agent_reviews"]).empty?
            add_schema_failure(
              "$.approval.reviewer.agent_reviews",
              "AGENT_REVIEWS_NOT_ALLOWED_FOR_REVIEWER_TYPE",
              "Human and organization-policy reviewer records cannot embed agent quorum results."
            )
          end
        end
      end

      def check_agent_reviews(reviews, reviewer_type)
        path = "$.approval.reviewer.agent_reviews"
        unless reviews.is_a?(Array) && !reviews.empty?
          add_schema_failure(path, "AGENT_REVIEWS_MISSING", "Agent reviewer results are required.")
          return
        end
        if reviewer_type == "AGENT" && reviews.length != 1
          add_schema_failure(path, "SINGLE_AGENT_REVIEW_CARDINALITY", "AGENT requires exactly one review result.")
        end

        reviews.each_with_index do |review, index|
          item_path = "#{path}[#{index}]"
          unless review.is_a?(Hash)
            add_schema_failure(item_path, "AGENT_REVIEW_NOT_OBJECT", "Agent review must be an object.")
            next
          end
          reject_unknown_keys(review, AGENT_REVIEW_KEYS, item_path)
          AGENT_REVIEW_KEYS.each { |key| required_string(review, key, item_path) }
          enum(review, "review_role", AGENT_REVIEW_ROLES, item_path)
          enum(review, "decision", %w[PASS BLOCKING_FAIL], item_path)
          unless Support.sha256?(review["input_digest"])
            add_enum_failure("#{item_path}.input_digest", "AGENT_REVIEW_INPUT_DIGEST_INVALID")
          end
          unless Support.sha256?(review["output_digest"])
            add_enum_failure("#{item_path}.output_digest", "AGENT_REVIEW_OUTPUT_DIGEST_INVALID")
          end
          unless Support.utc_seconds?(review["timestamp"])
            add_enum_failure("#{item_path}.timestamp", "AGENT_REVIEW_TIMESTAMP_INVALID")
          end
        end

        return unless reviewer_type == "AGENT_QUORUM"

        roles = reviews.map { |review| review["review_role"] if review.is_a?(Hash) }.compact
        agents = reviews.map { |review| review["agent_identifier"] if review.is_a?(Hash) }.compact
        digests = reviews.map { |review| review["input_digest"] if review.is_a?(Hash) }.compact
        unless roles.sort == AGENT_REVIEW_ROLES.sort
          add_schema_failure(path, "AGENT_QUORUM_ROLE_SET_INVALID", "Agent quorum requires each v0.1 role exactly once.")
        end
        unless agents.uniq.length == agents.length
          add_schema_failure(path, "AGENT_QUORUM_REVIEWER_REUSED", "Agent quorum requires distinct agent identifiers.")
        end
        unless digests.uniq.length == 1
          add_schema_failure(path, "AGENT_QUORUM_INPUT_CONFLICT", "Agent quorum reviews must bind one input digest.")
        end
      end

      def check_approval_timestamp(timestamp)
        return unless timestamp.is_a?(Hash)

        reject_unknown_keys(timestamp, APPROVAL_TIMESTAMP_KEYS, "$.approval.timestamp")
        %w[decided_at recorded_at valid_from expires_at].each do |key|
          required_string(timestamp, key, "$.approval.timestamp")
        end
        required_hash(timestamp, "time_source_reference", "$.approval.timestamp")
      end

      def reject_unknown_keys(object, allowed, path)
        return unless object.is_a?(Hash)

        (object.keys - allowed).sort.each do |key|
          @failures << Support.failure(
            rule_id: "TVP-SCH-005",
            source_design_rule: "TVM-SCH-005",
            severity: "MEDIUM",
            reason_code: "UNKNOWN_AUTHORITATIVE_FIELD",
            path: "#{path}.#{key}",
            message: "Field is not in the prototype allowlist; unknown authority defaults to INVALID."
          )
        end
      end

      def required_string(object, key, path)
        return object[key] if Support.non_empty_string?(object[key])

        add_schema_failure("#{path}.#{key}", "REQUIRED_STRING_MISSING", "Required non-empty string is missing.")
        nil
      end

      def required_hash(object, key, path)
        return object[key] if object[key].is_a?(Hash)

        add_schema_failure("#{path}.#{key}", "REQUIRED_OBJECT_MISSING", "Required object is missing.")
        nil
      end

      def required_array(object, key, path, allow_empty: true)
        value = object[key]
        return value if value.is_a?(Array) && (allow_empty || !value.empty?)

        reason = allow_empty ? "REQUIRED_ARRAY_MISSING" : "REQUIRED_NONEMPTY_ARRAY_MISSING"
        add_schema_failure("#{path}.#{key}", reason, "Required array is missing or has invalid cardinality.")
        nil
      end

      def required_nonnegative_integer(object, key, path)
        value = object[key]
        return value if value.is_a?(Integer) && value >= 0

        add_schema_failure("#{path}.#{key}", "NONNEGATIVE_INTEGER_REQUIRED", "Required value must be a non-negative integer.")
        nil
      end

      def check_digest(value, path)
        return if Support.sha256?(value)

        add_schema_failure(path, "INVALID_SHA256_DIGEST", "Digest must be sha256 plus 64 lowercase hex characters.")
      end

      def enum(object, key, allowed, path)
        return if allowed.include?(object[key])

        add_enum_failure("#{path}.#{key}", "UNKNOWN_ENUM_VALUE")
      end

      def add_schema_failure(path, reason_code, message)
        @failures << Support.failure(
          rule_id: "TVP-SCH-002",
          source_design_rule: "TVM-SCH-002",
          severity: "HIGH",
          reason_code: reason_code,
          path: path,
          message: message
        )
      end

      def add_enum_failure(path, reason_code)
        @failures << Support.failure(
          rule_id: "TVP-SCH-003",
          source_design_rule: "TVM-SCH-003",
          severity: "HIGH",
          reason_code: reason_code,
          path: path,
          message: "Value is missing or outside the prototype's closed vocabulary."
        )
      end

      def add_cross_field_failure(path, reason_code, message)
        @failures << Support.failure(
          rule_id: "TVP-SCH-004",
          source_design_rule: "TVM-SCH-004",
          severity: "HIGH",
          reason_code: reason_code,
          path: path,
          message: message
        )
      end
    end
  end
end
