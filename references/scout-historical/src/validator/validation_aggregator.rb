# frozen_string_literal: true

require "time"
require_relative "schema_check"
require_relative "reference_check"
require_relative "lifecycle_check"
require_relative "support"

module TITMASScout
  module Validator
    class ValidationAggregator
      RULESET_VERSION = "TITMAS-SCOUT-VALIDATOR-PROTOTYPE-STRUCTURAL-SUBSET-V0.1"
      VALIDATION_SCOPE = "PROTOTYPE_STRUCTURAL_SUBSET_POST_ACTION_CHAIN"
      NON_AUTHORIZATION_ASSERTION = "VALIDATION_DOES_NOT_GRANT_AUTHORIZATION"
      CHECKED_RULE_IDS = %w[
        TVP-SCH-002 TVP-SCH-003 TVP-SCH-004 TVP-SCH-005
        TVP-REF-001 TVP-REF-004 TVP-LIF-003 TVP-EVD-001
        TVP-EVD-005 TVP-AUT-001
      ].freeze
      UNCHECKED_CAPABILITIES = %w[
        formal_schema_validation
        full_validation_model_conformance
        nested_extension_semantics_beyond_prototype_allowlists
        ruleset_registry_and_manifest_integrity
        trusted_time_attestation
        uri_resolution
        artifact_digest_recomputation
        cryptographic_signature_verification
        evidence_provenance_freshness_and_admissibility
        reviewer_identity_authority_and_attestation_verification
        agent_reviewer_model_identity_and_runtime_independence_verification
        agent_review_output_digest_recomputation
        action_policy_evaluation
        authorized_scope_and_constraint_evaluation
        replay_and_use_limit_enforcement
        action_execution
        github_api_access
        external_action
        production_deployment
      ].freeze

      def initialize(clock: -> { Time.now.utc })
        @clock = clock
      end

      def validate(document, input_source: nil)
        timestamp = normalized_time
        bundle = normalize(document)
        failures = []
        failures.concat(SchemaCheck.new.check(bundle))
        failures.concat(ReferenceCheck.new.check(bundle))
        failures.concat(LifecycleCheck.new(evaluation_time: timestamp).check(bundle))
        build_result(
          failures: failures,
          input_source: input_source,
          timestamp: timestamp,
          input_form: envelope?(document) ? "PROTOTYPE_ENVELOPE" : "PLAIN_OPPORTUNITY_NORMALIZED_FAIL_CLOSED"
        )
      rescue StandardError => error
        self.class.execution_error(
          reason_code: "VALIDATOR_INTERNAL_ERROR",
          message: "Validator failed closed: #{error.class}: #{error.message}",
          input_source: input_source,
          timestamp: safe_time
        )
      end

      def self.execution_error(reason_code:, message:, input_source: nil, timestamp: Time.now.utc)
        instance = new(clock: -> { timestamp })
        failure = Support.failure(
          rule_id: "TVP-CTL-001",
          source_design_rule: "TVM-CTL-003,TVM-CTL-004",
          severity: "CRITICAL",
          reason_code: reason_code,
          path: "$",
          message: message
        )
        instance.send(
          :build_result,
          failures: [failure],
          input_source: input_source,
          timestamp: timestamp.utc,
          input_form: "UNAVAILABLE"
        )
      end

      private

      def normalize(document)
        if envelope?(document)
          document
        else
          {
            "prototype_profile" => "POST_ACTION_CHAIN",
            "opportunity" => document
          }
        end
      end

      def envelope?(document)
        document.is_a?(Hash) && document.key?("opportunity")
      end

      def normalized_time
        value = @clock.call
        raise ArgumentError, "clock must return Time" unless value.is_a?(Time)

        Time.iso8601(value.utc.iso8601)
      end

      def safe_time
        value = @clock.call
        value.is_a?(Time) ? value.utc : Time.now.utc
      rescue StandardError
        Time.now.utc
      end

      def build_result(failures:, input_source:, timestamp:, input_form:)
        failures = Support.deduplicate_and_sort(failures)
        status = failures.empty? ? "VALID" : "INVALID"
        Support.deep_sort(
          {
            "authorization_granted" => false,
            "checked_rule_ids" => CHECKED_RULE_IDS,
            "external_action_allowed" => false,
            "failed_rules" => failures,
            "input_form" => input_form,
            "input_source" => input_source,
            "non_authorization_assertion" => NON_AUTHORIZATION_ASSERTION,
            "prototype_classification" => "RESEARCH_PROTOTYPE_NOT_PRODUCTION",
            "ruleset_version" => RULESET_VERSION,
            "timestamp" => timestamp.utc.iso8601,
            "timestamp_trust" => "UNATTESTED_CALLER_OR_LOCAL_CLOCK",
            "unchecked_capabilities" => UNCHECKED_CAPABILITIES,
            "validation_scope" => VALIDATION_SCOPE,
            "validation_status" => status
          }
        )
      end
    end
  end
end
