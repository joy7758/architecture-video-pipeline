# frozen_string_literal: true

require "time"

module TITMASScout
  module Validator
    module Support
      UTC_SECONDS = /\A\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\z/.freeze
      SHA256 = /\Asha256:[0-9a-f]{64}\z/.freeze

      SEVERITY_ORDER = {
        "CRITICAL" => 0,
        "HIGH" => 1,
        "MEDIUM" => 2,
        "LOW" => 3
      }.freeze

      module_function

      def failure(rule_id:, source_design_rule:, severity:, reason_code:, path:, message:)
        {
          "message" => message,
          "path" => path,
          "reason_code" => reason_code,
          "rule_id" => rule_id,
          "severity" => severity,
          "source_design_rule" => source_design_rule
        }
      end

      def non_empty_string?(value)
        value.is_a?(String) && !value.strip.empty?
      end

      def utc_seconds?(value)
        return false unless value.is_a?(String) && UTC_SECONDS.match?(value)

        Time.iso8601(value).utc.iso8601 == value
      rescue ArgumentError
        false
      end

      def parse_utc(value)
        return nil unless utc_seconds?(value)

        Time.iso8601(value).utc
      end

      def sha256?(value)
        value.is_a?(String) && SHA256.match?(value)
      end

      def deep_sort(value)
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

      def deduplicate_and_sort(failures)
        unique = failures.uniq do |failure|
          [failure["rule_id"], failure["reason_code"], failure["path"]]
        end

        unique.sort_by do |failure|
          [
            SEVERITY_ORDER.fetch(failure["severity"], 99),
            failure["rule_id"].to_s,
            failure["path"].to_s,
            failure["reason_code"].to_s
          ]
        end
      end
    end
  end
end
