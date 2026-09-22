# frozen_string_literal: true

require "digest"
require "fileutils"
require "json"
require "open3"
require "time"
require "yaml"

module TITMASScout
  module Integrations
    class TitmasEvidenceAdapter
      REQUIRED_MANIFEST_KEYS = %w[
        run_id source_reference commit_sha digest_algorithm digest_value
        ruleset_version action_scope actor_type result uncertainty
        unsupported_claims timestamp
      ].freeze
      COMMANDS = %w[record verify export verify-export].freeze
      SENSITIVE_KEY = /(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|private[_-]?key|client[_-]?secret)/i
      SENSITIVE_VALUE = /(?:gh[opusr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{20,})/

      def initialize(config_path:, command_runner: nil)
        @config_path = config_path
        @config = load_config(config_path)
        @command_runner = command_runner || method(:capture_command)
      end

      def preflight
        evidence = @config.dig("canonical_sources", "evidence")
        repository = evidence.fetch("local_repository_path")
        cli = File.join(repository, evidence.fetch("cli_relative_path"))
        return denied("MISSING_AGENT_EVIDENCE_CLI") unless File.executable?(cli)

        commit = execute(["git", "-C", repository, "rev-parse", "HEAD"])
        return denied("AGENT_EVIDENCE_COMMIT_PROBE_FAILED", [commit]) unless commit["success"]
        unless commit["stdout"].strip == evidence.fetch("expected_commit")
          return denied("AGENT_EVIDENCE_COMMIT_MISMATCH", [commit])
        end

        capabilities = execute([cli, "capabilities", "--json"])
        parsed = parse_json_result(capabilities)
        return denied("AGENT_EVIDENCE_CAPABILITIES_INVALID", [capabilities]) unless parsed
        unless parsed["version"] == evidence.fetch("expected_package_version")
          return denied("AGENT_EVIDENCE_VERSION_MISMATCH", [capabilities])
        end

        probes = COMMANDS.map { |command| execute([cli, command, "--help"]) }
        return denied("AGENT_EVIDENCE_COMMAND_UNAVAILABLE", probes) unless probes.all? { |item| item["success"] }

        {
          "decision" => "ALLOW",
          "artifact_family" => evidence.fetch("artifact_family"),
          "cli" => cli,
          "commit" => commit["stdout"].strip,
          "package_version" => parsed.fetch("version"),
          "verification_scope" => evidence.fetch("verification_scope"),
          "command_receipts" => [commit, capabilities] + probes
        }
      rescue KeyError, Psych::Exception, JSON::ParserError, SystemCallError => error
        denied("AGENT_EVIDENCE_PREFLIGHT_ERROR:#{error.class}")
      end

      def capture(run_manifest_path:, output_dir:, event_type:)
        FileUtils.mkdir_p(output_dir)
        verification_path = File.join(output_dir, "agent-evidence-verification.json")
        return denied_and_write("EVIDENCE_OUTPUT_ALREADY_EXISTS", verification_path) if File.exist?(verification_path)

        manifest = JSON.parse(File.read(run_manifest_path))
        missing = REQUIRED_MANIFEST_KEYS.reject { |key| manifest.key?(key) }
        return denied_and_write("RUN_MANIFEST_FIELDS_MISSING:#{missing.join(',')}", verification_path) unless missing.empty?

        safe_manifest = sanitize(manifest)
        preflight_result = preflight
        return write_result(verification_path, preflight_result) unless preflight_result["decision"] == "ALLOW"

        cli = preflight_result.fetch("cli")
        store = File.join(output_dir, "evidence-store.jsonl")
        bundle = File.join(output_dir, "evidence-bundle.json")
        export_manifest = File.join(output_dir, "evidence-export-manifest.json")
        context = {
          "source" => "tiamas-scout",
          "component" => "titmas-evidence-adapter",
          "attributes" => {
            "canonical_repository" => "agent-evidence",
            "canonical_commit" => preflight_result.fetch("commit"),
            "artifact_family" => preflight_result.fetch("artifact_family")
          }
        }
        metadata = {
          "verification_scope" => preflight_result.fetch("verification_scope"),
          "actor_authentication" => "NOT_ESTABLISHED",
          "authorization_granted" => false,
          "unsupported_claims" => safe_manifest.fetch("unsupported_claims")
        }

        receipts = []
        receipts << execute([
          cli, "record", "--store", store, "--actor", safe_manifest.fetch("actor_type"),
          "--event-type", event_type, "--input", JSON.generate(safe_manifest),
          "--output", JSON.generate("result" => safe_manifest.fetch("result")),
          "--context", JSON.generate(context), "--metadata", JSON.generate(metadata),
          "--tag", "titmas-scout", "--tag", "run:#{safe_manifest.fetch('run_id')}"
        ])
        return denied_capture("AGENT_EVIDENCE_RECORD_FAILED", verification_path, receipts) unless receipts.last["success"]

        receipts << execute([cli, "verify", "--store", store])
        store_verification = parse_json_result(receipts.last)
        unless receipts.last["success"] && store_verification&.fetch("ok", false) == true
          return denied_capture("AGENT_EVIDENCE_STORE_VERIFY_FAILED", verification_path, receipts)
        end

        receipts << execute([
          cli, "export", "--store", store, "--format", "json", "--output", bundle,
          "--manifest-output", export_manifest
        ])
        export_result = parse_json_result(receipts.last)
        unless receipts.last["success"] && export_result && File.file?(bundle) && File.file?(export_manifest)
          return denied_capture("AGENT_EVIDENCE_EXPORT_FAILED", verification_path, receipts)
        end

        receipts << execute([cli, "verify-export", "--bundle", bundle])
        export_verification = parse_json_result(receipts.last)
        unless receipts.last["success"] && export_verification&.fetch("ok", false) == true
          return denied_capture("AGENT_EVIDENCE_EXPORT_VERIFY_FAILED", verification_path, receipts)
        end

        result = {
          "artifact_type" => "TITMAS_SCOUT_AGENT_EVIDENCE_VERIFICATION",
          "schema_version" => "0.1",
          "decision" => "PASS",
          "external_action_allowed" => false,
          "authorization_granted" => false,
          "run_id" => safe_manifest.fetch("run_id"),
          "event_type" => event_type,
          "canonical_repository" => "agent-evidence",
          "canonical_commit" => preflight_result.fetch("commit"),
          "package_version" => preflight_result.fetch("package_version"),
          "artifact_family" => preflight_result.fetch("artifact_family"),
          "verification_scope" => preflight_result.fetch("verification_scope"),
          "actor_authentication" => "NOT_ESTABLISHED",
          "signature_present" => export_verification.fetch("signature_present"),
          "signature_verified" => export_verification.fetch("signature_verified"),
          "record_count" => export_verification.fetch("record_count"),
          "latest_chain_hash" => export_verification.fetch("latest_chain_hash"),
          "artifacts" => {
            "store" => artifact_reference(store, output_dir),
            "bundle" => artifact_reference(bundle, output_dir),
            "manifest" => artifact_reference(export_manifest, output_dir)
          },
          "command_receipts" => receipts,
          "unsupported_claims" => [
            "EVIDENCE_NE_TRUTH",
            "VERIFICATION_NE_AUTHORIZATION",
            "VERIFICATION_NE_CERTIFICATION",
            "ACTOR_IDENTITY_NOT_AUTHENTICATED"
          ]
        }
        write_result(verification_path, result)
      rescue JSON::ParserError, KeyError, SystemCallError => error
        denied_and_write("AGENT_EVIDENCE_CAPTURE_ERROR:#{error.class}", verification_path)
      end

      private

      def load_config(path)
        value = YAML.safe_load(
          File.read(path), permitted_classes: [], permitted_symbols: [], aliases: false,
          filename: path
        )
        raise ArgumentError, "TITMAS integration config must be a mapping" unless value.is_a?(Hash)

        value
      end

      def capture_command(arguments)
        stdout, stderr, status = Open3.capture3(*arguments)
        [stdout, stderr, status.exitstatus]
      end

      def execute(arguments)
        stdout, stderr, exit_status = @command_runner.call(arguments)
        {
          "argv" => sanitize(arguments),
          "exit_status" => Integer(exit_status),
          "success" => Integer(exit_status).zero?,
          "stdout" => sanitize(stdout.to_s),
          "stderr" => sanitize(stderr.to_s)
        }
      rescue StandardError => error
        {
          "argv" => sanitize(arguments),
          "exit_status" => -1,
          "success" => false,
          "stdout" => "",
          "stderr" => "#{error.class}: #{sanitize(error.message)}"
        }
      end

      def parse_json_result(receipt)
        return nil unless receipt["success"]

        JSON.parse(receipt["stdout"])
      rescue JSON::ParserError
        nil
      end

      def artifact_reference(path, root)
        {
          "path" => path.delete_prefix("#{root}/"),
          "digest_algorithm" => "sha256",
          "digest_value" => Digest::SHA256.file(path).hexdigest
        }
      end

      def sanitize(value)
        case value
        when Hash
          value.each_with_object({}) do |(key, nested), copy|
            copy[key] = SENSITIVE_KEY.match?(key.to_s) ? "[REDACTED]" : sanitize(nested)
          end
        when Array
          value.map { |nested| sanitize(nested) }
        when String
          value.gsub(SENSITIVE_VALUE, "[REDACTED]").gsub(%r{/Users/[^/]+}, "[LOCAL_HOME]")
        else
          value
        end
      end

      def denied(reason, receipts = [])
        {
          "artifact_type" => "TITMAS_SCOUT_AGENT_EVIDENCE_VERIFICATION",
          "schema_version" => "0.1",
          "decision" => "DENY",
          "reason_codes" => [reason],
          "external_action_allowed" => false,
          "authorization_granted" => false,
          "command_receipts" => receipts,
          "unsupported_claims" => ["VERIFICATION_NOT_COMPLETED"]
        }
      end

      def denied_capture(reason, path, receipts)
        write_result(path, denied(reason, receipts))
      end

      def denied_and_write(reason, path)
        write_result(path, denied(reason))
      end

      def write_result(path, result)
        File.write(path, JSON.pretty_generate(result) + "\n")
        result
      end
    end
  end
end
