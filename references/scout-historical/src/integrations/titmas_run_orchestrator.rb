# frozen_string_literal: true

require "digest"
require "fileutils"
require "json"
require "time"

module TITMASScout
  module Integrations
    class TitmasRunOrchestrator
      REQUIRED_BINDING_KEYS = %w[
        run_id repository target source_state source_digest head_sha
        selected_slice_digest diff_digest action_payload_digest input_digest
        ruleset_version action expires_at
      ].freeze

      def initialize(output_root: "reports/titmas-runs")
        @output_root = output_root
      end

      def create_run(run_id:, manifest:, artifacts: {})
        run_dir = File.join(@output_root, run_id)
        raise ArgumentError, "IMMUTABLE_RUN_ALREADY_EXISTS" if File.exist?(run_dir)

        FileUtils.mkdir_p(run_dir)
        write_once(run_dir, "run-manifest.json", manifest)
        artifacts.each { |name, value| write_once(run_dir, name, value) }
        run_dir
      end

      def write_once(run_dir, name, value)
        path = File.join(run_dir, name)
        raise ArgumentError, "IMMUTABLE_ARTIFACT_ALREADY_EXISTS:#{name}" if File.exist?(path)

        FileUtils.mkdir_p(File.dirname(path))
        File.write(path, JSON.pretty_generate(deep_sort(value)) + "\n")
        path
      end

      def authorization_result(request:, authorization:, evidence_verification:, current_context:, now:)
        reasons = []
        reasons << "AGENT_EVIDENCE_NOT_VERIFIED" unless evidence_verification["decision"] == "PASS"
        reasons << "QUORUM_NOT_ALLOWED" unless authorization["decision"] == "ALLOW"
        reasons << "HUMAN_REVIEW_FLAG_INVALID" unless authorization["human_review_required"] == false
        reasons << "ACTION_NOT_AUTHORIZED" unless Array(authorization["authorized_actions"]).include?(request["action"])

        request_binding = request.fetch("authorization_binding", {})
        authorization_binding = authorization.fetch("authorization_binding", {})
        missing = REQUIRED_BINDING_KEYS.reject { |key| request_binding.key?(key) && authorization_binding.key?(key) }
        reasons << "AUTHORIZATION_BINDING_MISSING:#{missing.join(',')}" unless missing.empty?

        REQUIRED_BINDING_KEYS.each do |key|
          next unless request_binding.key?(key) && authorization_binding.key?(key)
          reasons << "AUTHORIZATION_BINDING_MISMATCH:#{key}" unless request_binding[key] == authorization_binding[key]
        end

        %w[
          repository target source_state source_digest head_sha
          selected_slice_digest diff_digest action_payload_digest ruleset_version
        ].each do |key|
          next unless request_binding.key?(key) && current_context.key?(key)
          reasons << "STALE_AUTHORIZATION:#{key}" unless request_binding[key] == current_context[key]
        end

        begin
          expires_at = Time.iso8601(request_binding.fetch("expires_at")).utc
          reasons << "AUTHORIZATION_EXPIRED" unless now.utc < expires_at
        rescue ArgumentError, KeyError
          reasons << "AUTHORIZATION_EXPIRY_INVALID"
        end

        {
          "decision" => reasons.empty? ? "ALLOW" : "DENY",
          "external_action_allowed" => reasons.empty?,
          "reason_codes" => reasons.uniq.sort,
          "authorization_binding_digest" => digest_for(request_binding)
        }
      end

      def digest_for(value)
        "sha256:#{Digest::SHA256.hexdigest(JSON.generate(deep_sort(value)))}"
      end

      private

      def deep_sort(value)
        case value
        when Hash
          value.keys.sort.each_with_object({}) { |key, sorted| sorted[key] = deep_sort(value[key]) }
        when Array
          value.map { |item| deep_sort(item) }
        else
          value
        end
      end
    end
  end
end
