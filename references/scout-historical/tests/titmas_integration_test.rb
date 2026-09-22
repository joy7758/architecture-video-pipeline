# frozen_string_literal: true

require "minitest/autorun"
require "fileutils"
require "json"
require "tmpdir"
require "yaml"
require_relative "../src/integrations/dba_handoff"
require_relative "../src/integrations/titmas_evidence_adapter"
require_relative "../src/integrations/titmas_run_orchestrator"

class TitmasIntegrationTest < Minitest::Test
  class FakeEvidenceCLI
    attr_reader :calls

    def initialize(fail_command: nil, verify_ok: true)
      @fail_command = fail_command
      @verify_ok = verify_ok
      @calls = []
    end

    def call(arguments)
      @calls << arguments
      command = arguments[1]
      return ["expected-commit\n", "", 0] if arguments.first == "git"
      return [JSON.generate("version" => "0.1.0rc3"), "", 0] if command == "capabilities"
      return ["help", "", 0] if arguments.last == "--help"
      return ["", "forced failure", 1] if command == @fail_command
      if command == "record"
        store = arguments[arguments.index("--store") + 1]
        File.write(store, "{}\n")
        return [JSON.generate("event" => { "event_id" => "event-1" }), "", 0]
      end
      if command == "verify"
        return [JSON.generate("ok" => @verify_ok, "records" => 1, "issues" => []), "", @verify_ok ? 0 : 1]
      end
      if command == "export"
        bundle = arguments[arguments.index("--output") + 1]
        manifest = arguments[arguments.index("--manifest-output") + 1]
        File.write(bundle, "{}\n")
        File.write(manifest, "{}\n")
        return [JSON.generate("record_count" => 1, "signed" => false), "", 0]
      end
      if command == "verify-export"
        return [JSON.generate(
          "ok" => true,
          "record_count" => 1,
          "latest_chain_hash" => "abc",
          "signature_present" => false,
          "signature_verified" => nil
        ), "", 0]
      end

      ["", "unexpected command", 1]
    end
  end

  def test_agent_evidence_unavailable_denies
    Dir.mktmpdir do |directory|
      config = write_config(directory, repository: File.join(directory, "missing"))
      adapter = TITMASScout::Integrations::TitmasEvidenceAdapter.new(config_path: config)

      result = adapter.preflight

      assert_equal "DENY", result["decision"]
      assert_includes result["reason_codes"], "MISSING_AGENT_EVIDENCE_CLI"
    end
  end

  def test_agent_evidence_verify_failure_denies
    with_adapter(verify_ok: false) do |adapter, directory|
      result = adapter.capture(
        run_manifest_path: write_manifest(directory),
        output_dir: File.join(directory, "evidence"),
        event_type: "titmas.scout.pre_action"
      )

      assert_equal "DENY", result["decision"]
      assert_includes result["reason_codes"], "AGENT_EVIDENCE_STORE_VERIFY_FAILED"
      assert_equal false, result["external_action_allowed"]
    end
  end

  def test_canonical_export_and_verify_passes_with_unsigned_boundary
    with_adapter do |adapter, directory|
      result = adapter.capture(
        run_manifest_path: write_manifest(directory, "api_key" => "must-not-escape"),
        output_dir: File.join(directory, "evidence"),
        event_type: "titmas.scout.pre_action"
      )

      assert_equal "PASS", result["decision"]
      assert_equal "STRUCTURE_DIGEST_CHAIN_ONLY", result["verification_scope"]
      assert_equal false, result["signature_present"]
      assert_nil result["signature_verified"]
      assert_equal false, result["authorization_granted"]
      refute_includes JSON.generate(result), "must-not-escape"
      refute_match(%r{/Users/[^/]+}, JSON.generate(result))
    end
  end

  def test_exact_authorization_binding_allows_once_current
    guard = TITMASScout::Integrations::TitmasRunOrchestrator.new(output_root: "unused")
    request, authorization, current = authorization_fixture
    result = guard.authorization_result(
      request: request,
      authorization: authorization,
      evidence_verification: { "decision" => "PASS" },
      current_context: current,
      now: Time.iso8601("2026-08-02T04:00:00Z")
    )

    assert_equal "ALLOW", result["decision"]
    assert_equal true, result["external_action_allowed"]
  end

  def test_head_or_diff_change_invalidates_old_authorization
    guard = TITMASScout::Integrations::TitmasRunOrchestrator.new(output_root: "unused")
    request, authorization, current = authorization_fixture
    current["head_sha"] = "new-head"
    current["diff_digest"] = "sha256:new-diff"
    result = guard.authorization_result(
      request: request,
      authorization: authorization,
      evidence_verification: { "decision" => "PASS" },
      current_context: current,
      now: Time.iso8601("2026-08-02T04:00:00Z")
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "STALE_AUTHORIZATION:head_sha"
    assert_includes result["reason_codes"], "STALE_AUTHORIZATION:diff_digest"
  end

  def test_issue_state_or_source_digest_change_invalidates_old_authorization
    guard = TITMASScout::Integrations::TitmasRunOrchestrator.new(output_root: "unused")
    request, authorization, current = authorization_fixture
    current["source_state"] = "CLOSED"
    current["source_digest"] = "sha256:changed-source"
    result = guard.authorization_result(
      request: request,
      authorization: authorization,
      evidence_verification: { "decision" => "PASS" },
      current_context: current,
      now: Time.iso8601("2026-08-02T04:00:00Z")
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "STALE_AUTHORIZATION:source_state"
    assert_includes result["reason_codes"], "STALE_AUTHORIZATION:source_digest"
  end

  def test_comment_body_change_invalidates_old_authorization
    guard = TITMASScout::Integrations::TitmasRunOrchestrator.new(output_root: "unused")
    request, authorization, current = authorization_fixture
    current["action_payload_digest"] = "sha256:changed-comment-body"
    result = guard.authorization_result(
      request: request,
      authorization: authorization,
      evidence_verification: { "decision" => "PASS" },
      current_context: current,
      now: Time.iso8601("2026-08-02T04:00:00Z")
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "STALE_AUTHORIZATION:action_payload_digest"
  end

  def test_action_not_in_authorized_actions_denies
    guard = TITMASScout::Integrations::TitmasRunOrchestrator.new(output_root: "unused")
    request, authorization, current = authorization_fixture
    authorization["authorized_actions"] = ["PUSH_PERSONAL_BRANCH"]
    result = guard.authorization_result(
      request: request,
      authorization: authorization,
      evidence_verification: { "decision" => "PASS" },
      current_context: current,
      now: Time.iso8601("2026-08-02T04:00:00Z")
    )

    assert_equal "DENY", result["decision"]
    assert_includes result["reason_codes"], "ACTION_NOT_AUTHORIZED"
  end

  def test_immutable_run_directory_cannot_be_overwritten
    Dir.mktmpdir do |directory|
      orchestrator = TITMASScout::Integrations::TitmasRunOrchestrator.new(output_root: directory)
      orchestrator.create_run(run_id: "run-1", manifest: { "run_id" => "run-1" })

      error = assert_raises(ArgumentError) do
        orchestrator.create_run(run_id: "run-1", manifest: { "run_id" => "run-1" })
      end
      assert_equal "IMMUTABLE_RUN_ALREADY_EXISTS", error.message
    end
  end

  def test_dba_handoff_never_claims_ingestion
    Dir.mktmpdir do |directory|
      handoff = TITMASScout::Integrations::DbaHandoff.new(output_root: directory)
      path = handoff.write("latest-run", "run_id" => "run-1")
      document = JSON.parse(File.read(path))

      assert_equal "READY_FOR_READ_ONLY_REVIEW_NOT_INTEGRATED", document["handoff_status"]
      assert_equal false, document["dba_repository_modified"]
      assert_equal false, document["dba_ingestion_observed"]
    end
  end

  private

  def with_adapter(verify_ok: true)
    Dir.mktmpdir do |directory|
      repository = File.join(directory, "agent-evidence")
      cli = File.join(repository, ".venv/bin/agent-evidence")
      FileUtils.mkdir_p(File.dirname(cli))
      File.write(cli, "fake")
      File.chmod(0o755, cli)
      config = write_config(directory, repository: repository)
      runner = FakeEvidenceCLI.new(verify_ok: verify_ok)
      adapter = TITMASScout::Integrations::TitmasEvidenceAdapter.new(
        config_path: config,
        command_runner: runner
      )
      yield adapter, directory
    end
  end

  def write_config(directory, repository:)
    path = File.join(directory, "integration.yaml")
    File.write(path, YAML.dump(
      "canonical_sources" => {
        "evidence" => {
          "local_repository_path" => repository,
          "cli_relative_path" => ".venv/bin/agent-evidence",
          "expected_commit" => "expected-commit",
          "expected_package_version" => "0.1.0rc3",
          "artifact_family" => "EVIDENCE_ENVELOPE_EXPORT",
          "verification_scope" => "STRUCTURE_DIGEST_CHAIN_ONLY"
        }
      }
    ))
    path
  end

  def write_manifest(directory, extras = {})
    path = File.join(directory, "run-manifest.json")
    File.write(path, JSON.pretty_generate({
      "run_id" => "run-1",
      "source_reference" => "agentrust-io/ca2a#76",
      "commit_sha" => "head",
      "digest_algorithm" => "sha256",
      "digest_value" => "digest",
      "ruleset_version" => "0.1",
      "action_scope" => ["POST_BOUNDED_TECHNICAL_COMMENT"],
      "actor_type" => "AGENT_QUORUM",
      "result" => "PRE_ACTION_READY",
      "uncertainty" => ["maintainer_acceptance_unknown"],
      "unsupported_claims" => ["production_safety"],
      "timestamp" => "2026-08-02T04:00:00Z"
    }.merge(extras)))
    path
  end

  def authorization_fixture
    binding = {
      "run_id" => "run-1",
      "repository" => "agentrust-io/ca2a",
      "target" => "agentrust-io/ca2a#76",
      "source_state" => "OPEN",
      "source_digest" => "sha256:source",
      "head_sha" => "head",
      "selected_slice_digest" => "sha256:selected-slice",
      "diff_digest" => "sha256:diff",
      "action_payload_digest" => "sha256:comment-body",
      "input_digest" => "sha256:input",
      "ruleset_version" => "0.1",
      "action" => "POST_BOUNDED_TECHNICAL_COMMENT",
      "expires_at" => "2026-08-02T05:00:00Z"
    }
    request = {
      "action" => "POST_BOUNDED_TECHNICAL_COMMENT",
      "authorization_binding" => Marshal.load(Marshal.dump(binding))
    }
    authorization = {
      "decision" => "ALLOW",
      "human_review_required" => false,
      "authorized_actions" => ["POST_BOUNDED_TECHNICAL_COMMENT"],
      "authorization_binding" => Marshal.load(Marshal.dump(binding))
    }
    current = binding.slice(
      "repository", "target", "source_state", "source_digest", "head_sha",
      "selected_slice_digest", "diff_digest", "action_payload_digest", "ruleset_version"
    )
    [request, authorization, current]
  end
end
