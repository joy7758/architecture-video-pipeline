# frozen_string_literal: true

require "digest"
require "json"
require "time"
require_relative "review_result"

module TITMASScout
  module Review
    class ReviewInput
      REQUIRED_KEYS = %w[
        artifact_type
        ruleset_version
        review_run_id
        observed_at
        requested_action
        target
        source_issue
        duplicate_check
        pull_request
        diff
        local_validation
        github_checks
        automation
        risk_evidence
        history_references
        known_limits
      ].freeze
      TARGET_KEYS = %w[type reference url].freeze
      REQUIRED_EVIDENCE_OBJECTS = %w[
        source_issue
        duplicate_check
        pull_request
        diff
        local_validation
        automation
        risk_evidence
      ].freeze
      REQUIRED_EVIDENCE_ARRAYS = %w[
        github_checks
        history_references
        known_limits
      ].freeze
      HISTORY_REFERENCE_KEYS = %w[path content_digest].freeze

      attr_reader :document, :digest, :source

      def self.load(path)
        bytes = File.binread(path)
        document = JSON.parse(
          bytes,
          object_class: DuplicateKeyRejectingHash
        )
        new(
          document,
          digest: "sha256:#{Digest::SHA256.hexdigest(bytes)}",
          source: path
        )
      end

      def initialize(document, digest:, source: nil)
        @document = ReviewResult.deep_copy(document)
        ReviewResult.deep_freeze(@document)
        @digest = digest.dup.freeze
        @source = source&.dup&.freeze
      end

      def requested_action
        document["requested_action"] if document.is_a?(Hash)
      end

      def errors(policy_version:)
        return ["REVIEW_INPUT_NOT_OBJECT"] unless document.is_a?(Hash)

        errors = []
        errors << "REVIEW_INPUT_KEYS_INVALID" unless document.keys.map(&:to_s).sort == REQUIRED_KEYS.sort
        unless document["artifact_type"] == "TITMAS_SCOUT_AGENT_REVIEW_INPUT"
          errors << "REVIEW_INPUT_ARTIFACT_TYPE_INVALID"
        end
        errors << "REVIEW_INPUT_RULESET_MISMATCH" unless document["ruleset_version"] == policy_version
        errors << "REVIEW_RUN_ID_INVALID" unless non_empty_string?(document["review_run_id"])
        errors << "REVIEW_INPUT_TIMESTAMP_INVALID" unless utc_seconds?(document["observed_at"])
        errors << "REQUESTED_ACTION_INVALID" unless non_empty_string?(requested_action)
        errors << "REVIEW_INPUT_DIGEST_INVALID" unless ReviewResult::SHA256.match?(digest.to_s)

        target = document["target"]
        if !target.is_a?(Hash) || target.keys.map(&:to_s).sort != TARGET_KEYS.sort
          errors << "REVIEW_TARGET_INVALID"
        elsif TARGET_KEYS.any? { |key| !non_empty_string?(target[key]) }
          errors << "REVIEW_TARGET_INVALID"
        end

        REQUIRED_EVIDENCE_OBJECTS.each do |key|
          value = document[key]
          unless value.is_a?(Hash) && !value.empty?
            errors << "REVIEW_EVIDENCE_OBJECT_INVALID:#{key}"
          end
        end
        REQUIRED_EVIDENCE_ARRAYS.each do |key|
          errors << "REVIEW_EVIDENCE_ARRAY_INVALID:#{key}" unless document[key].is_a?(Array)
        end
        errors.concat(content_reference_errors)

        errors.uniq.sort
      end

      private

      def non_empty_string?(value)
        value.is_a?(String) && !value.strip.empty?
      end

      def utc_seconds?(value)
        return false unless value.is_a?(String) && ReviewResult::UTC_SECONDS.match?(value)

        Time.iso8601(value).utc.iso8601 == value
      rescue ArgumentError
        false
      end

      def content_reference_errors
        errors = []
        diff = document["diff"]
        if diff.is_a?(Hash) && !digest?(diff["content_digest"])
          errors << "DIFF_CONTENT_DIGEST_INVALID"
        end

        validation = document["local_validation"]
        if validation.is_a?(Hash)
          errors << "VALIDATION_RECORD_REFERENCE_INVALID" unless non_empty_string?(validation["record_reference"])
          errors << "VALIDATION_RECORD_DIGEST_INVALID" unless digest?(validation["record_digest"])
        end

        checks = document["github_checks"]
        if checks.is_a?(Array) && !checks.all? { |item| item.is_a?(Hash) && !item.empty? }
          errors << "GITHUB_CHECK_EVIDENCE_INVALID"
        end

        references = document["history_references"]
        if references.is_a?(Array)
          valid = references.all? do |item|
            item.is_a?(Hash) &&
              item.keys.map(&:to_s).sort == HISTORY_REFERENCE_KEYS.sort &&
              non_empty_string?(item["path"]) &&
              digest?(item["content_digest"])
          end
          errors << "HISTORY_REFERENCE_INVALID" unless valid
        end

        limits = document["known_limits"]
        if limits.is_a?(Array) && !limits.all? { |item| non_empty_string?(item) }
          errors << "KNOWN_LIMITS_INVALID"
        end
        errors
      end

      def digest?(value)
        value.is_a?(String) && ReviewResult::SHA256.match?(value)
      end

      private_class_method :new
    end
  end
end
