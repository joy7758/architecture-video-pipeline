# frozen_string_literal: true

require "fileutils"
require "json"
require_relative "support"

module TITMASScout
  module Discovery
    class DailyReport
      REPORT_SCHEMA_VERSION = "0.1"

      def initialize(output_root:)
        @output_root = output_root
      end

      def build(run_date:, generated_at:, config_path:, config_digest:,
                collection:, deduplication:, excluded:, tracked_opportunities:,
                ranked_candidates:, opportunities:, selection: nil)
        selection ||= {
          "conversion_queue" => [],
          "excluded_by_actionability" => [],
          "next_conversion_target" => nil,
          "research_watchlist" => []
        }
        filter_counts = excluded.each_with_object(Hash.new(0)) do |item, counts|
          Array(item["reasons"]).each { |reason| counts[reason] += 1 }
        end
        paths = output_paths(run_date)

        {
          "artifact_type" => "TITMAS_SCOUT_DAILY_OPPORTUNITY_REPORT",
          "candidate_counts" => {
            "duplicate_count" => deduplication.fetch("duplicate_count"),
            "eligible_count" => ranked_candidates.length,
            "excluded_count" => excluded.length,
            "raw_retrieved_count" => collection.fetch("items").length,
            "selected_count" => opportunities.length,
            "tracked_conversion_count" => tracked_opportunities.length,
            "unique_count" => deduplication.fetch("unique_count")
          },
          "collection" => collection.reject { |key, _| key == "items" },
          "config" => {
            "content_digest" => "sha256:#{config_digest}",
            "path" => config_path
          },
          "external_action_authorized" => false,
          "filtered_candidates" => excluded,
          "filter_reason_counts" => filter_counts,
          "generated_at" => generated_at.utc.iso8601,
          "heuristic_model" => "heuristic_unvalidated_v0.1",
          "local_output_paths" => paths,
          "non_claims" => [
            "ranking_is_not_calibrated",
            "no_success_probability",
            "no_customer_or_revenue_claim",
            "open_issue_does_not_imply_contribution_acceptance",
            "report_does_not_authorize_external_action"
          ],
          "no_write_evidence" => no_write_evidence(collection),
          "opportunities" => opportunities,
          "opportunity_selection" => selection,
          "report_date" => run_date.iso8601,
          "run_status" => report_status(collection),
          "schema_version" => REPORT_SCHEMA_VERSION,
          "trust_guard" => {
            "invoked" => false,
            "reason" => "Discovery report generation does not itself invoke review authorization or external action.",
            "status" => "FROZEN_AUXILIARY_GUARD",
            "version" => "TITMAS_SCOUT_TRUST_GUARD_V0.1"
          },
          "tracked_opportunities" => tracked_opportunities,
          "unselected_candidates" => unselected_candidates(
            ranked_candidates,
            opportunities
          )
        }
      end

      def write(report)
        paths = report.fetch("local_output_paths")
        FileUtils.mkdir_p(File.dirname(paths.fetch("json")))

        json = JSON.pretty_generate(Support.deep_sort(report)) + "\n"
        File.write(paths.fetch("json"), json)
        daily_digest = Support.sha256_file(paths.fetch("json"))
        File.write(paths.fetch("markdown"), render_markdown(report))

        latest = build_latest(report, daily_digest)
        File.write(
          paths.fetch("latest"),
          JSON.pretty_generate(Support.deep_sort(latest)) + "\n"
        )

        {
          "daily_json_digest" => "sha256:#{daily_digest}",
          "json" => paths.fetch("json"),
          "latest" => paths.fetch("latest"),
          "markdown" => paths.fetch("markdown")
        }
      end

      private

      def output_paths(run_date)
        date = run_date.iso8601
        daily_root = File.join(@output_root, "daily")
        {
          "json" => File.join(daily_root, "#{date}-opportunity-report.json"),
          "latest" => File.join(@output_root, "latest-opportunities.json"),
          "markdown" => File.join(daily_root, "#{date}-opportunity-report.md")
        }
      end

      def report_status(collection)
        case collection["collection_status"]
        when "BLOCKED"
          "BLOCKED_NO_LIVE_DATA"
        when "PARTIAL_ISSUES_ONLY"
          "LIVE_READ_ONLY_PARTIAL_SOURCE_COVERAGE"
        else
          "LIVE_READ_ONLY_PARTIAL_QUERY_COVERAGE"
        end
      end

      def no_write_evidence(collection)
        methods = Array(collection["http_events"]).map { |event| event["method"] }.uniq.sort
        {
          "all_observed_http_methods_are_get" => methods.all? { |method| method == "GET" },
          "external_write_operations_observed" => collection.fetch("external_write_operations_observed"),
          "github_commands_declared_read_only" => Array(collection["command_events"]).all? do |event|
            event["read_only"] == true
          end,
          "observed_http_methods" => methods,
          "output_scope" => "LOCAL_REPORT_FILES_ONLY"
        }
      end

      def build_latest(report, daily_digest)
        {
          "architecture_handoff" => {
            "dba_repository_modified" => false,
            "integration_request" => "READ_ONLY_REVIEW_AND_FUTURE_INGESTION_ASSESSMENT",
            "status" => "READY_FOR_READ_ONLY_REVIEW_NOT_INTEGRATED",
            "target" => "digital-biosphere-architecture"
          },
          "artifact_type" => "TITMAS_SCOUT_LATEST_OPPORTUNITIES",
          "data_coverage" => {
            "backend" => report.dig("collection", "backend"),
            "collection_status" => report.dig("collection", "collection_status"),
            "discussion_coverage" => report.dig("collection", "discussion_coverage"),
            "source_types_collected" => report.dig("collection", "source_types_collected"),
            "source_types_missing" => report.dig("collection", "source_types_missing")
          },
          "external_action_authorized" => false,
          "generated_at" => report.fetch("generated_at"),
          "heuristic_model" => report.fetch("heuristic_model"),
          "default_selection_mode" => "AGENT_QUORUM",
          "human_exception_review_required" => "CONDITIONAL",
          "opportunities" => report.fetch("opportunities"),
          "opportunity_selection" => report.fetch("opportunity_selection"),
          "tracked_opportunities" => report.fetch("tracked_opportunities"),
          "report_date" => report.fetch("report_date"),
          "schema_version" => REPORT_SCHEMA_VERSION,
          "source_report" => {
            "content_digest" => "sha256:#{daily_digest}",
            "path" => report.dig("local_output_paths", "json")
          },
          "trust_guard" => report.fetch("trust_guard")
        }
      end

      def unselected_candidates(ranked_candidates, opportunities)
        selected_urls = opportunities.map { |item| item["url"] }
        ranked_candidates.reject do |candidate|
          selected_urls.include?(candidate["url"])
        end.map do |candidate|
          {
            "reason" => "REPORT_LIMIT_MAX_FIVE",
            "repository" => candidate["repository"],
            "source" => candidate["url"],
            "title" => candidate["title"]
          }
        end
      end

      def render_markdown(report)
        counts = report.fetch("candidate_counts")
        lines = []
        lines << "# TITMAS Scout Opportunity Report — #{report.fetch("report_date")}"
        lines << ""
        lines << "<!-- markdownlint-disable MD013 -->"
        lines << ""
        lines << "> Read-only discovery report. Heuristic ordering is unvalidated."
        lines << "> Policy-selected review is required; this report does not authorize external action."
        lines << ""
        lines << "## Run Summary"
        lines << ""
        lines << "- Status: `#{report.fetch("run_status")}`"
        lines << "- Backend: `#{report.dig("collection", "backend")}`"
        lines << "- Retrieved at: `#{report.dig("collection", "retrieved_at")}`"
        lines << "- Raw retrieved candidates: #{counts.fetch("raw_retrieved_count")}"
        lines << "- Unique candidates: #{counts.fetch("unique_count")}"
        lines << "- Excluded candidates: #{counts.fetch("excluded_count")}"
        lines << "- Selected candidates: #{counts.fetch("selected_count")}"
        lines << "- Tracked active conversions: #{counts.fetch("tracked_conversion_count")}"
        lines << "- Discussions: `#{report.dig("collection", "discussion_coverage", "status")}`"
        lines << ""
        lines << "## Data Coverage"
        lines << ""
        lines << "The local GitHub CLI is preferred, but this run records its actual"
        lines << "authentication status and any anonymous public REST fallback. GitHub"
        lines << "Discussion results are absent when authenticated GraphQL is unavailable."
        lines << ""
        lines << "### Raw Queries"
        lines << ""
        report.dig("collection", "queries").each do |query|
          lines << "- `#{query.fetch("query_id")}` — #{query.fetch("query")}"
          lines << "  (`#{query.fetch("status")}`, retrieved #{query.fetch("retrieved_count")})"
        end
        lines << ""
        lines << "## Selected Opportunities"
        lines << ""

        if report.fetch("opportunities").empty?
          lines << "No candidate passed the current evidence and actionability filters."
          lines << ""
        else
          report.fetch("opportunities").each do |candidate|
            render_candidate(lines, candidate)
          end
        end

        lines << "## Conversion Selection"
        lines << ""
        target = report.dig("opportunity_selection", "next_conversion_target")
        if target
          lines << "- Next conversion target: [#{markdown_text(target["repository"])}##{target["number"]}](#{target["url"]})"
          lines << "- Classification: `#{target.dig("actionability_classification", "classification")}`"
        else
          lines << "- Next conversion target: none"
        end
        lines << "- Conversion queue count: #{report.dig("opportunity_selection", "conversion_queue").length}"
        lines << "- Research watchlist count: #{report.dig("opportunity_selection", "research_watchlist").length}"
        lines << ""

        lines << "## Existing Conversion State"
        lines << ""
        if report.fetch("tracked_opportunities").empty?
          lines << "- No retrieved signal matched an existing conversion or review record."
        else
          report.fetch("tracked_opportunities").each do |item|
            lines << "- `#{item.fetch("tracked_status")}` — [#{markdown_text(item["repository"])}##{item["number"]}](#{item["source"]})"
            observation = item["source_observed_in_current_run"] ? "observed again" : "carried from immutable local history"
            lines << "  (`#{item.fetch("root_problem_id")}`; #{observation}; excluded from new discovery)"
          end
        end
        lines << ""

        lines << "## Filtering Summary"
        lines << ""
        if report.fetch("filter_reason_counts").empty?
          lines << "- No candidates were excluded after deduplication."
        else
          report.fetch("filter_reason_counts").sort.each do |reason, count|
            lines << "- `#{reason}`: #{count}"
          end
        end
        lines << ""
        lines << "## Review and Trust Boundary"
        lines << ""
        lines << "The report is a review queue. Ordinary open-source actions require the"
        lines << "five-role Agent Review Quorum; legal, payment, binding identity,"
        lines << "restricted-data, deletion, account-security, and protected-branch merge"
        lines << "actions require human exception review. Trust Guard was not invoked"
        lines << "because report generation does not itself select an external action."
        lines << ""
        lines << "```text"
        lines << "HEURISTIC_RANKING_CALIBRATED=false"
        lines << "DEFAULT_SELECTION_MODE=AGENT_QUORUM"
        lines << "HUMAN_EXCEPTION_REVIEW_REQUIRED=CONDITIONAL"
        lines << "EXTERNAL_ACTION_AUTHORIZED=false"
        lines << "CUSTOMER_ACQUIRED=false"
        lines << "```"
        lines << ""
        lines.join("\n")
      end

      def render_candidate(lines, candidate)
        pack = candidate.fetch("action_pack")
        lines << "### #{candidate.fetch("priority_position")}. #{markdown_text(candidate["title"])}"
        lines << ""
        lines << "- Source: [#{markdown_text(candidate["repository"])}](#{candidate["url"]})"
        lines << "- Current state: `#{candidate["state"]}`"
        lines << "- Pain point: #{markdown_text(candidate["pain_point"])}"
        components = candidate.fetch("capability_mappings").map { |item| item["capability_id"] }
        lines << "- TITMAS components: #{components.map { |item| "`#{item}`" }.join(", ")}"
        lines << "- Action entry: [open public entry](#{candidate["url"]})"
        lines << "- Suggested next step: `#{pack["suggested_action_type"]}`"
        lines << "- Retention reason: #{markdown_text(candidate["retention_reason"])}"
        lines << "- Ranking status: `#{candidate["ranking_status"]}`"
        lines << "- Unconfirmed facts: #{candidate["unconfirmed_facts"].join(", ")}"
        lines << "- Minimum contribution: #{markdown_text(pack["minimum_contribution"])}"
        lines << "- External action authorized: `false`"
        lines << ""
      end

      def markdown_text(value)
        Support.normalize_text(value).gsub("|", "\\|")
      end
    end
  end
end
