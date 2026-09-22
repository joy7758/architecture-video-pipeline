# frozen_string_literal: true

require "minitest/autorun"
require "date"
require "json"
require "open3"
require "rbconfig"
require "stringio"
require "tmpdir"
require "yaml"
require_relative "../src/discovery/action_pack_generator"
require_relative "../src/discovery/actionability_classifier"
require_relative "../src/discovery/cli"
require_relative "../src/discovery/daily_report"
require_relative "../src/discovery/deduplicator"
require_relative "../src/discovery/opportunity_ranker"
require_relative "../src/discovery/opportunity_selector"
require_relative "../src/discovery/signal_extractor"
require_relative "../src/discovery/source_collector"
require_relative "../src/discovery/status_index"

class DiscoveryPrototypeTest < Minitest::Test
  RUN_DATE = Date.iso8601("2026-08-01")
  RETRIEVED_AT = Time.iso8601("2026-08-01T10:00:00Z")

  def test_action_pack_generator_loads_its_actionability_dependency
    generator_path = File.expand_path("../src/discovery/action_pack_generator", __dir__)
    script = <<~RUBY
      require #{generator_path.inspect}
      puts TITMASScout::Discovery::ActionPackGenerator.name
      puts TITMASScout::Discovery::ActionabilityClassifier::CLASSIFICATIONS.length
    RUBY
    stdout, stderr, status = Open3.capture3(RbConfig.ruby, "-e", script)

    assert status.success?, stderr
    assert_equal "TITMASScout::Discovery::ActionPackGenerator\n4\n", stdout
  end

  class FakeCommandRunner
    attr_reader :calls

    def initialize(authenticated: false, search_items: [])
      @authenticated = authenticated
      @calls = []
      @search_items = search_items
    end

    def call(arguments)
      @calls << arguments
      if arguments.first(2) == %w[gh version]
        result(true, "gh version 2.92.0\n", "", 0)
      elsif arguments.first(3) == %w[gh auth status]
        if @authenticated
          result(true, "github.com authenticated\n", "", 0)
        else
          result(false, "", "token invalid\n", 1)
        end
      elsif arguments.first(3) == %w[gh search issues]
        result(true, "#{JSON.generate(@search_items)}\n", "", 0)
      else
        result(false, "", "unexpected command\n", 1)
      end
    end

    private

    def result(success, stdout, stderr, exit_status)
      {
        "exit_status" => exit_status,
        "stderr" => stderr,
        "stdout" => stdout,
        "success" => success
      }
    end
  end

  def test_authenticated_gh_search_uses_flags_without_embedded_qualifiers
    runner = FakeCommandRunner.new(authenticated: true)
    config = Marshal.load(Marshal.dump(@config))
    config["collection_policy"]["maximum_queries_per_run"] = 1
    collector = TITMASScout::Discovery::SourceCollector.new(
      config: config,
      run_date: RUN_DATE,
      retrieved_at: RETRIEVED_AT,
      http_transport: FakeGetTransport.new([]),
      command_runner: runner
    )

    result = collector.collect
    arguments = runner.calls.find do |item|
      item.first(3) == %w[gh search issues]
    end

    assert_equal "GH_CLI_AUTHENTICATED", result["backend"]
    assert_equal @config.dig("queries", 0, "query"), arguments[3]
    refute_match(/\bis:|archived:|updated:/, arguments[3])
    assert_includes arguments, "--archived=false"
    assert_equal "open", arguments[arguments.index("--state") + 1]
    assert_equal ">=2026-05-03", arguments[arguments.index("--updated") + 1]
    assert_equal "public", arguments[arguments.index("--visibility") + 1]
  end

  def test_authenticated_gh_search_preserves_nonempty_assignees
    item = gh_issue.merge(
      "assignees" => [{ "login" => "issue-owner" }]
    )
    runner = FakeCommandRunner.new(
      authenticated: true,
      search_items: [item]
    )
    config = Marshal.load(Marshal.dump(@config))
    config["collection_policy"]["maximum_queries_per_run"] = 1
    result = TITMASScout::Discovery::SourceCollector.new(
      config: config,
      run_date: RUN_DATE,
      retrieved_at: RETRIEVED_AT,
      http_transport: FakeGetTransport.new([]),
      command_runner: runner
    ).collect

    assert_equal ["issue-owner"], result.dig("items", 0, "assignees")
  end

  def test_authenticated_gh_search_preserves_malformed_assignee_as_unknown
    item = gh_issue.merge("assignees" => [{}])
    runner = FakeCommandRunner.new(
      authenticated: true,
      search_items: [item]
    )
    config = Marshal.load(Marshal.dump(@config))
    config["collection_policy"]["maximum_queries_per_run"] = 1
    result = TITMASScout::Discovery::SourceCollector.new(
      config: config,
      run_date: RUN_DATE,
      retrieved_at: RETRIEVED_AT,
      http_transport: FakeGetTransport.new([]),
      command_runner: runner
    ).collect

    assert_nil result.dig("items", 0, "assignees")
    classification = TITMASScout::Discovery::ActionabilityClassifier.new.classify(
      result.fetch("items").first
    )
    assert_equal "EXCLUDE", classification.fetch("classification")
    assert_equal "ASSIGNEE_EVIDENCE_UNKNOWN", classification.fetch("reason_code")
    assert_nil classification.dig("evidence", "assignees")
  end

  class FakeGetTransport
    attr_reader :events

    def initialize(items)
      @items = items
      @events = []
    end

    def get(uri, _headers)
      @events << {
        "host" => uri.host,
        "method" => "GET",
        "path" => uri.path,
        "status" => 200
      }
      body = JSON.generate("total_count" => @items.length, "items" => @items)
      TITMASScout::Discovery::SourceCollector::HttpResponse.new(
        200,
        body,
        {
          "x-ratelimit-limit" => "10",
          "x-ratelimit-remaining" => "9",
          "x-ratelimit-resource" => "search"
        }
      )
    end
  end

  class FlakyGetTransport < FakeGetTransport
    attr_reader :attempts

    def initialize(items, failures:)
      super(items)
      @failures = failures
      @attempts = 0
    end

    def get(uri, headers)
      @attempts += 1
      raise Net::OpenTimeout, "simulated transient failure" if @attempts <= @failures

      super
    end
  end

  class FixedCollector
    def initialize(collection)
      @collection = collection
    end

    def collect
      Marshal.load(Marshal.dump(@collection))
    end
  end

  def setup
    @config = YAML.safe_load(
      File.read("config/discovery-sources.yaml"),
      permitted_classes: [],
      permitted_symbols: [],
      aliases: false
    )
  end

  def test_invalid_gh_auth_transparently_falls_back_to_get_only_rest
    transport = FakeGetTransport.new([rest_issue])
    collector = TITMASScout::Discovery::SourceCollector.new(
      config: @config,
      run_date: RUN_DATE,
      retrieved_at: RETRIEVED_AT,
      http_transport: transport,
      command_runner: FakeCommandRunner.new(authenticated: false)
    )

    result = collector.collect

    assert_equal "GITHUB_PUBLIC_REST_GET_ONLY", result["backend"]
    assert_equal "INVALID", result.dig("gh_cli", "auth_status")
    assert_equal "BLOCKED", result.dig("discussion_coverage", "status")
    assert_equal 0, result["external_write_operations_observed"]
    assert_equal ["GET"], transport.events.map { |event| event["method"] }.uniq
    assert_equal @config["queries"].length, transport.events.length
  end

  def test_github_write_commands_are_rejected_by_the_allowlist
    collector = TITMASScout::Discovery::SourceCollector.new(
      config: @config,
      run_date: RUN_DATE,
      retrieved_at: RETRIEVED_AT,
      http_transport: FakeGetTransport.new([]),
      command_runner: FakeCommandRunner.new
    )

    assert_raises(ArgumentError) do
      collector.send(
        :run_command,
        ["gh", "issue", "comment", "1", "--body", "forbidden"],
        "WRITE_ATTEMPT"
      )
    end
  end

  def test_graphql_mutation_is_rejected_by_the_read_only_allowlist
    collector = TITMASScout::Discovery::SourceCollector.new(
      config: @config,
      run_date: RUN_DATE,
      retrieved_at: RETRIEVED_AT,
      http_transport: FakeGetTransport.new([]),
      command_runner: FakeCommandRunner.new
    )

    assert_raises(ArgumentError) do
      collector.send(
        :run_command,
        ["gh", "api", "graphql", "-f", "query=mutation { deleteProjectV2(input: {}) { clientMutationId } }"],
        "GRAPHQL_MUTATION_ATTEMPT"
      )
    end
  end

  def test_public_rest_retries_bounded_transient_failures
    transport = FlakyGetTransport.new([rest_issue], failures: 2)
    config = Marshal.load(Marshal.dump(@config))
    config["collection_policy"]["maximum_queries_per_run"] = 1
    collector = TITMASScout::Discovery::SourceCollector.new(
      config: config,
      run_date: RUN_DATE,
      retrieved_at: RETRIEVED_AT,
      http_transport: transport,
      command_runner: FakeCommandRunner.new(authenticated: false)
    )

    result = collector.collect

    assert_equal 3, transport.attempts
    assert_equal "SUCCESS", result.dig("queries", 0, "status")
    assert_equal 2, result.dig("queries", 0, "transport_retry_count")
    assert_equal ["issue-owner"], result.dig("items", 0, "assignees")
  end

  def test_public_rest_preserves_malformed_assignee_as_unknown
    transport = FakeGetTransport.new([rest_issue.merge("assignees" => [nil])])
    config = Marshal.load(Marshal.dump(@config))
    config["collection_policy"]["maximum_queries_per_run"] = 1
    result = TITMASScout::Discovery::SourceCollector.new(
      config: config,
      run_date: RUN_DATE,
      retrieved_at: RETRIEVED_AT,
      http_transport: transport,
      command_runner: FakeCommandRunner.new(authenticated: false)
    ).collect

    assert_nil result.dig("items", 0, "assignees")
    classification = TITMASScout::Discovery::ActionabilityClassifier.new.classify(
      result.fetch("items").first
    )
    assert_equal "EXCLUDE", classification.fetch("classification")
    assert_equal "ASSIGNEE_EVIDENCE_UNKNOWN", classification.fetch("reason_code")
  end

  def test_deduplication_preserves_query_lineage
    first = normalized_item.merge("query_ids" => ["Q-1"])
    second = normalized_item.merge("query_ids" => ["Q-2"])
    result = TITMASScout::Discovery::Deduplicator.new.deduplicate([first, second])

    assert_equal 2, result["input_count"]
    assert_equal 1, result["unique_count"]
    assert_equal 1, result["duplicate_count"]
    assert_equal %w[Q-1 Q-2], result.dig("items", 0, "query_ids")
  end

  def test_existing_publication_and_review_are_not_rediscovered
    Dir.mktmpdir do |directory|
      review_root = File.join(directory, "review-runs", "run-1")
      FileUtils.mkdir_p(review_root)
      File.write(
        File.join(review_root, "input.json"),
        JSON.generate(
          "source_issue" => {
            "url" => "https://github.com/agentrust-io/ca2a/issues/36"
          },
          "target" => "https://github.com/agentrust-io/ca2a/pull/76",
          "ambiguous_reference" => "agentrust-io/ca2a#76"
        )
      )
      index = TITMASScout::Discovery::StatusIndex.new(reports_root: directory)
      status = index.status_for(
        "repository" => "agentrust-io/ca2a", "number" => 36
      )

      assert_equal "READY_FOR_REVIEW", status["status"]
      assert_equal "github:agentrust-io/ca2a:issue:36", status["root_problem_id"]
      assert_equal "agentrust-io/ca2a", status["repository"]
      assert_equal 36, status["number"]
      assert_equal "https://github.com/agentrust-io/ca2a/issues/36", status["source"]
      assert_includes status["related_entries"], "github:agentrust-io/ca2a:pull:76"
      assert_nil index.status_for(
        "repository" => "agentrust-io/ca2a", "number" => 76
      )
      refute index.entries.key?("agentrust-io/ca2a#76")

      signal = TITMASScout::Discovery::SignalExtractor.new(config: @config).extract(
        normalized_item.merge(
          "repository" => "agentrust-io/ca2a",
          "number" => 36,
          "url" => "https://github.com/agentrust-io/ca2a/issues/36"
        )
      )
      signal["history_status"] = status
      ranker = TITMASScout::Discovery::OpportunityRanker.new(
        config: @config, run_date: RUN_DATE
      )
      result = ranker.filter([signal])

      assert_empty result["retained"]
      assert_includes result.dig("excluded", 0, "reasons"),
                      "ALREADY_TRACKED:READY_FOR_REVIEW"
    end
  end

  def test_cli_carries_active_conversion_when_not_returned_by_current_queries
    collection = fixed_collection([normalized_item])

    Dir.mktmpdir("titmas-discovery-history-test") do |directory|
      review_root = File.join(directory, "review-runs", "run-1")
      FileUtils.mkdir_p(review_root)
      File.write(
        File.join(review_root, "input.json"),
        JSON.generate(
          "source_issue" => "https://github.com/agentrust-io/ca2a/issues/36",
          "target" => "https://github.com/agentrust-io/ca2a/pull/76"
        )
      )

      code = TITMASScout::Discovery::CLI.run(
        [
          "--date", RUN_DATE.iso8601,
          "--retrieved-at", RETRIEVED_AT.iso8601,
          "--output-root", directory
        ],
        stdout: StringIO.new,
        stderr: StringIO.new,
        dependencies: { collector: FixedCollector.new(collection) }
      )

      assert_equal 0, code
      report = JSON.parse(File.read(File.join(directory, "latest-opportunities.json")))
      tracked = report.fetch("tracked_opportunities").find do |item|
        item["root_problem_id"] == "github:agentrust-io/ca2a:issue:36"
      end
      refute_nil tracked
      assert_equal "READY_FOR_REVIEW", tracked["tracked_status"]
      assert_equal false, tracked["source_observed_in_current_run"]
      assert_includes tracked["related_entries"], "github:agentrust-io/ca2a:pull:76"
    end
  end

  def test_filter_and_ranking_are_explainable_and_not_calibrated
    extractor = TITMASScout::Discovery::SignalExtractor.new(config: @config)
    signal = extractor.extract(normalized_item)
    ranker = TITMASScout::Discovery::OpportunityRanker.new(
      config: @config,
      run_date: RUN_DATE
    )
    filtering = ranker.filter([signal])
    candidate = ranker.rank(filtering["retained"]).first

    assert_empty filtering["excluded"]
    assert_equal true, candidate["heuristic_unvalidated"]
    assert_equal "NEEDS_REVIEW", candidate["ranking_status"]
    assert_equal "NEEDS_REVIEW", candidate.dig("ranking_factors", "potential_value", "band")
    assert_nil candidate["success_probability"]
    refute recursive_key?(candidate, "score")
  end

  def test_actionable_now_precedes_observe_in_conversion_selection
    candidates = classified_candidate_pool
    ranked = rank_candidates(candidates.reverse)
    result = TITMASScout::Discovery::OpportunitySelector.new.select(
      ranked,
      maximum: 5
    )

    assert_equal "https://github.com/praxis-proxy/ai/issues/194",
                 result.dig("next_conversion_target", "url")
    assert_equal [194, 482, 461],
                 result.fetch("conversion_queue").map { |item| item["number"] }
    assert result.fetch("conversion_queue").all? do |candidate|
      %w[ACTIONABLE_NOW ACTIONABLE_AFTER_CONTACT].include?(
        candidate.dig("actionability_classification", "classification")
      )
    end
    refute_includes result.fetch("conversion_queue").map { |item| item["url"] },
                    "https://github.com/syswonder/robonix/issues/189"
  end

  def test_assigned_to_author_without_invitation_is_observe
    candidate = rank_candidates([robonix_candidate]).first

    assert_equal "OBSERVE",
                 candidate.dig("actionability_classification", "classification")
    assert_equal "ASSIGNED_WITHOUT_EXTERNAL_CONTRIBUTION_INVITATION",
                 candidate.dig("actionability_classification", "reason_code")
    assert_equal "OBSERVE",
                 TITMASScout::Discovery::ActionPackGenerator.new.generate(candidate)
                                                            .fetch("suggested_action_type")
    assert_equal "conversion_readiness",
                 candidate.fetch("ordering_basis").first.fetch("factor")
    assert_equal "OBSERVE",
                 candidate.fetch("ordering_basis").first.fetch("band")
  end

  def test_assignment_without_invitation_precedes_contact_instruction
    candidate = rank_candidates([
      gents_candidate.merge("assignees" => ["jackzampolin"])
    ]).first

    assert_equal "OBSERVE",
                 candidate.dig("actionability_classification", "classification")
    assert_equal "ASSIGNED_WITHOUT_EXTERNAL_CONTRIBUTION_INVITATION",
                 candidate.dig("actionability_classification", "reason_code")
  end

  def test_automated_author_without_contribution_invitation_is_observe
    candidate = rank_candidates([
      praxis_candidate.merge(
        "author" => "sadasant-ghost[bot]",
        "number" => 37,
        "repository" => "idolum-ai/kenogram",
        "url" => "https://github.com/idolum-ai/kenogram/issues/37"
      )
    ]).first

    assert_equal "OBSERVE",
                 candidate.dig("actionability_classification", "classification")
    assert_equal "AUTOMATED_AUTHOR_WITHOUT_EXTERNAL_CONTRIBUTION_INVITATION",
                 candidate.dig("actionability_classification", "reason_code")
  end

  def test_unknown_lock_or_assignee_evidence_fails_closed
    candidates = rank_candidates([
      praxis_candidate.merge("is_locked" => nil),
      praxis_candidate.merge("assignees" => nil, "number" => 195,
                              "url" => "https://github.com/praxis-proxy/ai/issues/195")
    ])

    assert_equal %w[ASSIGNEE_EVIDENCE_UNKNOWN LOCK_STATE_UNKNOWN],
                 candidates.map { |item| item.dig("actionability_classification", "reason_code") }.sort
    assert candidates.all? do |candidate|
      candidate.dig("actionability_classification", "classification") == "EXCLUDE"
    end
  end

  def test_unknown_selector_classification_is_explicitly_excluded
    candidate = ranked_candidate
    candidate.delete("actionability_classification")
    result = TITMASScout::Discovery::OpportunitySelector.new.select(
      [candidate],
      maximum: 5
    )

    assert_nil result["next_conversion_target"]
    assert_empty result["conversion_queue"]
    assert_equal "ACTIONABILITY_CLASSIFICATION_UNKNOWN",
                 result.dig("excluded_by_actionability", 0,
                            "actionability_classification", "reason_code")
  end

  def test_action_pack_rejects_missing_or_unknown_actionability
    generator = TITMASScout::Discovery::ActionPackGenerator.new
    candidate = ranked_candidate
    candidate.delete("actionability_classification")

    assert_raises(ArgumentError) { generator.generate(candidate) }
    candidate["actionability_classification"] = {
      "classification" => "UNKNOWN"
    }
    assert_raises(ArgumentError) { generator.generate(candidate) }
  end

  def test_excluded_candidate_can_only_generate_observe_pack
    candidate = ranked_candidate
    candidate["actionability_classification"] = {
      "classification" => "EXCLUDE"
    }
    pack = TITMASScout::Discovery::ActionPackGenerator.new.generate(candidate)

    assert_equal "OBSERVE", pack["suggested_action_type"]
    assert_equal false, pack["external_action_authorized"]
  end

  def test_talk_to_maintainer_first_is_actionable_after_contact
    candidate = rank_candidates([gents_candidate]).first

    assert_equal "ACTIONABLE_AFTER_CONTACT",
                 candidate.dig("actionability_classification", "classification")
    assert_equal "CONTACT_FIRST_INSTRUCTION",
                 candidate.dig("actionability_classification", "reason_code")
  end

  def test_automated_research_summary_cannot_be_next_conversion_target
    ranked = rank_candidates([nightly_research_candidate, praxis_candidate])
    result = TITMASScout::Discovery::OpportunitySelector.new.select(
      ranked,
      maximum: 5
    )

    assert_equal "OBSERVE",
                 ranked.find { |item| item["number"] == 27 }
                       .dig("actionability_classification", "classification")
    assert_equal 194, result.dig("next_conversion_target", "number")
    refute_includes result.fetch("conversion_queue").map { |item| item["number"] }, 27
  end

  def test_historical_issue_636_is_excluded_without_a_new_entry
    extractor = TITMASScout::Discovery::SignalExtractor.new(config: @config)
    item = normalized_item.merge(
      "number" => 636,
      "repository" => "openai/openai-agents-python",
      "url" => "https://github.com/openai/openai-agents-python/issues/636"
    )
    ranker = TITMASScout::Discovery::OpportunityRanker.new(
      config: @config,
      run_date: RUN_DATE
    )
    result = ranker.filter([extractor.extract(item)])

    assert_empty result["retained"]
    assert_includes result.dig("excluded", 0, "reasons"),
                    "EXCLUDED_HISTORICAL_SIGNAL_636_NO_NEW_ENTRY"
  end

  def test_explicitly_assigned_internal_worker_item_is_excluded
    extractor = TITMASScout::Discovery::SignalExtractor.new(config: @config)
    item = normalized_item.merge(
      "title" => "Worker 3 - agent audit and provenance task",
      "body" => "This assignment is assigned to Worker 3 for an audit trail implementation."
    )
    ranker = TITMASScout::Discovery::OpportunityRanker.new(
      config: @config,
      run_date: RUN_DATE
    )
    result = ranker.filter([extractor.extract(item)])

    assert_empty result["retained"]
    assert_includes result.dig("excluded", 0, "reasons"),
                    "ASSIGNED_INTERNAL_WORK_ITEM"
  end

  def test_action_pack_is_non_executable_and_non_authorizing
    candidate = ranked_candidate
    generator = TITMASScout::Discovery::ActionPackGenerator.new
    pack = generator.generate(candidate)

    assert_equal false, pack["external_action_authorized"]
    assert_empty pack["human_exception_decisions_required"]
    assert_includes %w[COMMENT DISCUSSION PR APPLICATION BID CONTACT OBSERVE],
                    pack["suggested_action_type"]
    assert generator.validate!(pack)
    refute_match(/```|api\.github\.com|\bgh\s+api\b/i, JSON.generate(pack))
  end

  def test_evidence_excerpt_omits_embedded_links_and_email_addresses
    extractor = TITMASScout::Discovery::SignalExtractor.new(config: @config)
    signal = extractor.extract(
      normalized_item.merge(
        "body" => "#{"prefixword " * 12}Agent audit trace gap. " \
                  "See [proposal](https://example.test/x) " \
                  "or contact maintainer@example.test."
      )
    )
    excerpt = signal.fetch("source_evidence_excerpt")

    refute_match(%r{https?://}, excerpt)
    refute_match(/maintainer@example\.test/, excerpt)
    assert_match(/\Aprefixword\b/, excerpt)
  end

  def test_ranking_is_deterministic_for_reversed_input_order
    extractor = TITMASScout::Discovery::SignalExtractor.new(config: @config)
    signals = 3.times.map do |index|
      extractor.extract(
        normalized_item.merge(
          "id" => "NODE-#{index}",
          "number" => index + 50,
          "url" => "https://github.com/example/project/issues/#{index + 50}"
        )
      )
    end
    ranker = TITMASScout::Discovery::OpportunityRanker.new(
      config: @config,
      run_date: RUN_DATE
    )

    forward = ranker.rank(signals).map { |item| item["url"] }
    reverse = ranker.rank(signals.reverse).map { |item| item["url"] }

    assert_equal forward, reverse
  end

  def test_cli_writes_maximum_five_deterministic_review_candidates
    items = 6.times.map do |index|
      normalized_item.merge(
        "id" => "NODE-#{index}",
        "number" => index + 10,
        "title" => "Agent audit trace gap #{index}",
        "url" => "https://github.com/example/project/issues/#{index + 10}"
      )
    end
    collection = fixed_collection(items)

    Dir.mktmpdir("titmas-discovery-test") do |directory|
      stdout = StringIO.new
      stderr = StringIO.new
      code = TITMASScout::Discovery::CLI.run(
        [
          "--date", RUN_DATE.iso8601,
          "--retrieved-at", RETRIEVED_AT.iso8601,
          "--output-root", directory
        ],
        stdout: stdout,
        stderr: stderr,
        dependencies: { collector: FixedCollector.new(collection) }
      )

      assert_equal 0, code
      assert_equal "", stderr.string
      daily_path = File.join(
        directory,
        "daily",
        "2026-08-01-opportunity-report.json"
      )
      latest_path = File.join(directory, "latest-opportunities.json")
      report = JSON.parse(File.read(daily_path))
      latest = JSON.parse(File.read(latest_path))
      assert_equal 5, report.dig("candidate_counts", "selected_count")
      assert_equal 6, report.dig("candidate_counts", "eligible_count")
      assert_equal 1, report.fetch("unselected_candidates").length
      refute report.fetch("opportunities").first.key?("body")
      assert_equal false, latest["external_action_authorized"]
      assert_equal "CONDITIONAL",
                   latest["human_exception_review_required"]
      assert_equal false,
                   latest.dig("architecture_handoff", "dba_repository_modified")
      next_target = latest.dig("opportunity_selection", "next_conversion_target")
      refute_nil next_target
      assert_equal "ACTIONABLE_NOW",
                   next_target.dig("actionability_classification", "classification")
      assert_equal "OPEN_PUBLIC_COMMENT_ENTRY",
                   next_target.dig("actionability_classification", "reason_code")
      queue = latest.dig("opportunity_selection", "conversion_queue")
      assert_equal 5, queue.length
      assert queue.all? do |candidate|
        %w[ACTIONABLE_NOW ACTIONABLE_AFTER_CONTACT].include?(
          candidate.dig("actionability_classification", "classification")
        )
      end
      markdown = File.read(File.join(directory, "daily", "2026-08-01-opportunity-report.md"))
      assert_includes markdown, "## Conversion Selection"
      assert_includes markdown, "Classification: `ACTIONABLE_NOW`"
    end
  end

  private

  def rest_issue
    {
      "assignees" => [{ "login" => "issue-owner" }],
      "author_association" => "MEMBER",
      "body" => issue_body,
      "comments" => 4,
      "created_at" => "2026-07-15T12:00:00Z",
      "html_url" => "https://github.com/example/project/issues/42",
      "id" => 42,
      "labels" => [{ "name" => "help wanted" }],
      "locked" => false,
      "node_id" => "NODE-42",
      "number" => 42,
      "repository_url" => "https://api.github.com/repos/example/project",
      "state" => "open",
      "title" => "Need auditable agent execution trace and replay",
      "updated_at" => "2026-07-31T12:00:00Z",
      "user" => { "login" => "maintainer" }
    }
  end

  def normalized_item
    {
      "assignees" => [],
      "author" => "maintainer",
      "author_association" => "MEMBER",
      "body" => issue_body,
      "comments_count" => 4,
      "created_at" => "2026-07-15T12:00:00Z",
      "id" => "NODE-42",
      "is_locked" => false,
      "is_pull_request" => false,
      "labels" => ["help wanted"],
      "number" => 42,
      "query_ids" => ["Q-AI-AGENT-AUDIT"],
      "repository" => "example/project",
      "source_type" => "GITHUB_ISSUE",
      "state" => "OPEN",
      "title" => "Need auditable agent execution trace and replay",
      "updated_at" => "2026-07-31T12:00:00Z",
      "url" => "https://github.com/example/project/issues/42"
    }
  end

  def issue_body
    "We need an audit trail for agent execution evidence, provenance, replay, " \
      "authorization policy, and tamper-evident receipts. The current trace " \
      "cannot be independently verified. A small reproducible test and review " \
      "of the permission boundary would help maintainers evaluate a fix."
  end

  def ranked_candidate
    extractor = TITMASScout::Discovery::SignalExtractor.new(config: @config)
    signal = extractor.extract(normalized_item)
    ranker = TITMASScout::Discovery::OpportunityRanker.new(
      config: @config,
      run_date: RUN_DATE
    )
    ranker.rank([signal]).first
  end

  def classified_candidate_pool
    [praxis_candidate, robonix_candidate, gents_candidate, nightly_research_candidate, scion_candidate]
  end

  def praxis_candidate
    normalized_item.merge(
      "assignees" => [],
      "body" => "Log every policy decision as an audit event and propagate OpenTelemetry trace context.",
      "comments_count" => 0,
      "labels" => ["enhancement"],
      "number" => 194,
      "repository" => "praxis-proxy/ai",
      "title" => "Agent audit trail and observability",
      "url" => "https://github.com/praxis-proxy/ai/issues/194"
    )
  end

  def robonix_candidate
    normalized_item.merge(
      "assignees" => ["enkerewpo"],
      "author" => "enkerewpo",
      "body" => "The planner can claim completion without execution evidence. The architecture has open questions.",
      "comments_count" => 0,
      "labels" => ["bug"],
      "number" => 189,
      "repository" => "syswonder/robonix",
      "title" => "Pilot can falsely complete tasks without execution evidence",
      "url" => "https://github.com/syswonder/robonix/issues/189"
    )
  end

  def gents_candidate
    normalized_item.merge(
      "assignees" => [],
      "body" => "Anyone interested in working on it should talk to Jack first so the authorization design stays aligned.",
      "labels" => ["design"],
      "number" => 461,
      "repository" => "source-inc/gents",
      "title" => "DefraDB ACP integration for agent authorization",
      "url" => "https://github.com/source-inc/gents/issues/461"
    )
  end

  def nightly_research_candidate
    normalized_item.merge(
      "assignees" => [],
      "body" => "Paper summary and imagined implementation. Filed via the nightly research→issues pipeline.",
      "labels" => [],
      "number" => 27,
      "repository" => "mnemonik-dev/nightly-research",
      "title" => "[arXiv] ZK-proved agent authorization gate",
      "url" => "https://github.com/mnemonik-dev/nightly-research/issues/27"
    )
  end

  def scion_candidate
    normalized_item.merge(
      "assignees" => [],
      "body" => "Define tiered agent authorization roles and prevent sub-agent scope escalation.",
      "labels" => ["enhancement"],
      "number" => 482,
      "repository" => "ptone/scion",
      "title" => "Tiered agent authorization roles and sub-agent scope inheritance",
      "url" => "https://github.com/ptone/scion/issues/482"
    )
  end

  def gh_issue
    {
      "assignees" => [],
      "author" => { "login" => "maintainer" },
      "authorAssociation" => "MEMBER",
      "body" => issue_body,
      "commentsCount" => 0,
      "createdAt" => "2026-07-15T12:00:00Z",
      "id" => "NODE-42",
      "isLocked" => false,
      "isPullRequest" => false,
      "labels" => [{ "name" => "help wanted" }],
      "number" => 42,
      "repository" => { "nameWithOwner" => "example/project" },
      "state" => "OPEN",
      "title" => "Need auditable agent execution trace and replay",
      "updatedAt" => "2026-07-31T12:00:00Z",
      "url" => "https://github.com/example/project/issues/42"
    }
  end

  def rank_candidates(items)
    extractor = TITMASScout::Discovery::SignalExtractor.new(config: @config)
    signals = items.map { |item| extractor.extract(item) }
    TITMASScout::Discovery::OpportunityRanker.new(
      config: @config,
      run_date: RUN_DATE
    ).rank(signals)
  end

  def fixed_collection(items)
    {
      "backend" => "TEST_READ_ONLY_FIXTURE",
      "collection_status" => "PARTIAL_ISSUES_ONLY",
      "command_events" => [],
      "discussion_coverage" => {
        "reason_code" => "TEST_FIXTURE",
        "status" => "BLOCKED"
      },
      "external_write_operations_observed" => 0,
      "gh_cli" => {
        "auth_status" => "INVALID",
        "installed" => true,
        "reason_code" => "GH_AUTH_INVALID",
        "search_available" => false,
        "version" => "gh version 2.92.0"
      },
      "http_events" => [{ "method" => "GET" }],
      "items" => items,
      "queries" => [
        {
          "backend" => "TEST_READ_ONLY_FIXTURE",
          "github_total_count" => items.length,
          "query" => "test query is:issue is:open",
          "query_id" => "Q-TEST",
          "retrieved_at" => RETRIEVED_AT.iso8601,
          "retrieved_count" => items.length,
          "status" => "SUCCESS",
          "topic" => "AI_AGENT_AUDIT"
        }
      ],
      "retrieved_at" => RETRIEVED_AT.iso8601,
      "source_types_collected" => ["GITHUB_ISSUE"],
      "source_types_missing" => ["GITHUB_DISCUSSION"],
      "successful_query_count" => 1,
      "total_query_count" => 1
    }
  end

  def recursive_key?(value, target)
    case value
    when Hash
      value.any? do |key, nested|
        key.to_s == target || recursive_key?(nested, target)
      end
    when Array
      value.any? { |nested| recursive_key?(nested, target) }
    else
      false
    end
  end
end
