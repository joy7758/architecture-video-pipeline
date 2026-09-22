# frozen_string_literal: true

require "digest"
require "json"
require "time"

module TITMASScout
  module Review
    class DuplicateJSONKeyError < StandardError; end

    class DuplicateKeyRejectingHash < Hash
      def []=(key, value)
        raise DuplicateJSONKeyError, "duplicate JSON key: #{key}" if key?(key)

        super
      end
    end

    class ReviewResult
      ROLES = %w[
        DISCOVERY_REVIEWER
        EVIDENCE_REVIEWER
        SCOPE_REVIEWER
        QUALITY_REVIEWER
        RISK_REVIEWER
      ].freeze
      DECISIONS = %w[PASS BLOCKING_FAIL].freeze
      REQUIRED_KEYS = %w[
        schema_version
        review_id
        agent_identifier
        model_runtime_identifier
        review_role
        input_digest
        output_digest
        decision
        timestamp
        ruleset_version
        reason_codes
        findings
        blocking_reasons
        evidence_references
      ].freeze
      SHA256 = /\Asha256:[0-9a-f]{64}\z/.freeze
      UTC_SECONDS = /\A\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\z/.freeze

      attr_reader :document, :source

      def self.load(path)
        document = JSON.parse(
          File.read(path),
          object_class: DuplicateKeyRejectingHash
        )
        new(document, source: path)
      end

      def self.digest_for(document)
        payload = deep_sort(document.reject { |key, _value| key == "output_digest" })
        "sha256:#{Digest::SHA256.hexdigest(JSON.generate(payload))}"
      end

      def self.deep_sort(value)
        case value
        when Hash
          value.keys.sort.each_with_object({}) do |key, sorted|
            sorted[key] = deep_sort(value[key])
          end
        when Array
          value.map { |item| deep_sort(item) }
        else
          value
        end
      end

      def self.deep_copy(value)
        case value
        when Hash
          value.each_with_object({}) do |(key, nested), copy|
            copy[deep_copy(key)] = deep_copy(nested)
          end
        when Array
          value.map { |nested| deep_copy(nested) }
        else
          value.dup
        end
      rescue TypeError
        value
      end

      def self.deep_freeze(value)
        case value
        when Hash
          value.each do |key, nested|
            deep_freeze(key)
            deep_freeze(nested)
          end
        when Array
          value.each { |nested| deep_freeze(nested) }
        end
        value.freeze
      end

      def initialize(document, source: nil)
        @document = self.class.deep_copy(document)
        self.class.deep_freeze(@document)
        @source = source&.dup&.freeze
      end

      def errors(policy_version:)
        return ["REVIEW_RESULT_NOT_OBJECT"] unless document.is_a?(Hash)

        errors = []
        keys = document.keys.map(&:to_s)
        errors << "REVIEW_RESULT_KEYS_INVALID" unless keys.sort == REQUIRED_KEYS.sort
        errors << "SCHEMA_VERSION_INVALID" unless document["schema_version"] == "0.1"
        errors << "REVIEW_ID_INVALID" unless non_empty_string?(document["review_id"])
        errors << "AGENT_IDENTIFIER_INVALID" unless non_empty_string?(document["agent_identifier"])
        unless non_empty_string?(document["model_runtime_identifier"])
          errors << "MODEL_RUNTIME_IDENTIFIER_INVALID"
        end
        errors << "REVIEW_ROLE_UNKNOWN" unless ROLES.include?(document["review_role"])
        errors << "INPUT_DIGEST_INVALID" unless digest?(document["input_digest"])
        errors << "OUTPUT_DIGEST_INVALID" unless digest?(document["output_digest"])
        errors << "REVIEW_DECISION_UNKNOWN" unless DECISIONS.include?(document["decision"])
        errors << "TIMESTAMP_INVALID" unless utc_seconds?(document["timestamp"])
        errors << "RULESET_VERSION_MISMATCH" unless document["ruleset_version"] == policy_version
        errors << "REASON_CODES_INVALID" unless string_array?(document["reason_codes"], allow_empty: false)
        errors << "FINDINGS_INVALID" unless string_array?(document["findings"], allow_empty: false)
        unless string_array?(document["blocking_reasons"], allow_empty: true)
          errors << "BLOCKING_REASONS_INVALID"
        end
        unless string_array?(document["evidence_references"], allow_empty: false)
          errors << "EVIDENCE_REFERENCES_INVALID"
        end
        if document["decision"] == "PASS" && Array(document["blocking_reasons"]).any?
          errors << "PASS_WITH_BLOCKING_REASON"
        end
        if document["decision"] == "BLOCKING_FAIL" && Array(document["blocking_reasons"]).empty?
          errors << "BLOCKING_FAIL_WITHOUT_REASON"
        end
        if digest?(document["output_digest"]) && document["output_digest"] != self.class.digest_for(document)
          errors << "OUTPUT_DIGEST_MISMATCH"
        end
        errors.uniq.sort
      end

      def summary
        {
          "agent_identifier" => document["agent_identifier"],
          "decision" => document["decision"],
          "input_digest" => document["input_digest"],
          "model_runtime_identifier" => document["model_runtime_identifier"],
          "output_digest" => document["output_digest"],
          "review_id" => document["review_id"],
          "review_role" => document["review_role"],
          "timestamp" => document["timestamp"]
        }
      end

      private

      def digest?(value)
        value.is_a?(String) && SHA256.match?(value)
      end

      def non_empty_string?(value)
        value.is_a?(String) && !value.strip.empty?
      end

      def string_array?(value, allow_empty:)
        return false unless value.is_a?(Array)
        return false if !allow_empty && value.empty?

        value.all? { |item| non_empty_string?(item) }
      end

      def utc_seconds?(value)
        return false unless value.is_a?(String) && UTC_SECONDS.match?(value)

        Time.iso8601(value).utc.iso8601 == value
      rescue ArgumentError
        false
      end
    end
  end
end
