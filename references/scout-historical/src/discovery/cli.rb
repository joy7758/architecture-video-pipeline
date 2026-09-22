# frozen_string_literal: true

require "date"
require "json"
require "optparse"
require "time"
require "yaml"
require_relative "action_pack_generator"
require_relative "daily_report"
require_relative "deduplicator"
require_relative "opportunity_ranker"
require_relative "opportunity_selector"
require_relative "signal_extractor"
require_relative "source_collector"
require_relative "status_index"
require_relative "support"

module TITMASScout
  module Discovery
    class CLI
      DEFAULT_CONFIG = "config/discovery-sources.yaml"
      DEFAULT_OUTPUT_ROOT = "reports"

      def self.run(arguments, stdout: $stdout, stderr: $stderr,
                   dependencies: {})
        options = parse_options(arguments)
        config = load_config(options.fetch(:config))
        run_date = Date.iso8601(options.fetch(:date))
        retrieved_at = options[:retrieved_at] ? Time.iso8601(options[:retrieved_at]).utc : Time.now.utc

        collector = dependencies[:collector] || SourceCollector.new(
          config: config,
          run_date: run_date,
          retrieved_at: retrieved_at,
          http_transport: dependencies[:http_transport],
          command_runner: dependencies[:command_runner]
        )
        collection = collector.collect
        deduplication = Deduplicator.new.deduplicate(collection.fetch("items"))
        extractor = SignalExtractor.new(config: config)
        status_index = dependencies[:status_index] || StatusIndex.new(
          reports_root: options.fetch(:output_root)
        )
        signals = deduplication.fetch("items").map do |item|
          signal = extractor.extract(item)
          history_status = status_index.status_for(signal)
          history_status ? signal.merge("history_status" => history_status) : signal
        end
        ranker = OpportunityRanker.new(config: config, run_date: run_date)
        filtering = ranker.filter(signals)
        ranked = ranker.rank(filtering.fetch("retained"))
        tracked = tracked_opportunities(
          filtering.fetch("excluded"),
          status_index.entries.values
        )

        configured_maximum = Integer(
          config.dig("collection_policy", "maximum_selected_opportunities")
        )
        maximum = [options.fetch(:maximum), configured_maximum, 5].min
        selection = OpportunitySelector.new.select(ranked, maximum: maximum)
        generator = ActionPackGenerator.new
        selected = selection.fetch("report_candidates").map do |candidate|
          report_candidate(candidate).merge(
            "action_pack" => generator.generate(candidate),
            "retention_reason" => retention_reason(candidate)
          )
        end

        report_writer = dependencies[:report_writer] || DailyReport.new(
          output_root: options.fetch(:output_root)
        )
        report = report_writer.build(
          run_date: run_date,
          generated_at: retrieved_at,
          config_path: options.fetch(:config),
          config_digest: Support.sha256_file(options.fetch(:config)),
          collection: collection,
          deduplication: deduplication,
          excluded: filtering.fetch("excluded"),
          tracked_opportunities: tracked,
          ranked_candidates: ranked,
          opportunities: selected,
          selection: public_selection(selection)
        )
        paths = report_writer.write(report)
        stdout.puts(JSON.pretty_generate(Support.deep_sort(run_summary(report, paths))))
        collection.fetch("successful_query_count").positive? ? 0 : 2
      rescue OptionParser::ParseError, ArgumentError => error
        stderr.puts("Discovery run failed: #{error.message}")
        2
      rescue Psych::Exception, JSON::ParserError, SystemCallError => error
        stderr.puts("Discovery run failed: #{error.message}")
        2
      end

      def self.parse_options(arguments)
        today = Date.today.iso8601
        options = {
          config: DEFAULT_CONFIG,
          date: today,
          maximum: 5,
          output_root: DEFAULT_OUTPUT_ROOT,
          retrieved_at: nil
        }
        parser = OptionParser.new do |option_parser|
          option_parser.banner = "Usage: ruby src/discovery/cli.rb [options]"
          option_parser.on("--config PATH") { |value| options[:config] = value }
          option_parser.on("--date YYYY-MM-DD") { |value| options[:date] = value }
          option_parser.on("--max N", Integer) { |value| options[:maximum] = value }
          option_parser.on("--output-root PATH") { |value| options[:output_root] = value }
          option_parser.on("--retrieved-at UTC") { |value| options[:retrieved_at] = value }
        end
        parser.parse!(arguments)
        raise ArgumentError, "--max must be between 1 and 5" unless (1..5).cover?(options[:maximum])

        options
      end

      def self.load_config(path)
        value = YAML.safe_load(
          File.read(path),
          permitted_classes: [],
          permitted_symbols: [],
          aliases: false,
          filename: path
        )
        raise ArgumentError, "Discovery config must be a mapping" unless value.is_a?(Hash)

        value
      end

      def self.retention_reason(candidate)
        classifications = candidate.fetch("pain_classifications").map do |item|
          item["classification"]
        end
        "Retained because the public entry is open, unlocked, fresh, and maps #{classifications.join(", ")} to existing bounded TITMAS roles; all acceptance and value claims remain unconfirmed."
      end

      def self.report_candidate(candidate)
        candidate.reject do |key, _value|
          key == "body"
        end
      end

      def self.public_selection(selection)
        {
          "conversion_queue" => selection.fetch("conversion_queue").map { |item| report_candidate(item) },
          "excluded_by_actionability" => selection.fetch("excluded_by_actionability").map { |item| report_candidate(item) },
          "next_conversion_target" => selection["next_conversion_target"] && report_candidate(selection["next_conversion_target"]),
          "research_watchlist" => selection.fetch("research_watchlist").map { |item| report_candidate(item) }
        }
      end

      def self.tracked_opportunities(excluded, historical_entries)
        retrieved = excluded.select { |item| item["tracked_status"] }.map do |item|
          item.merge("source_observed_in_current_run" => true)
        end
        persistent = historical_entries.map do |entry|
          {
            "evidence_paths" => entry.fetch("evidence_paths"),
            "number" => entry.fetch("number"),
            "related_entries" => entry.fetch("related_entries"),
            "repository" => entry.fetch("repository"),
            "root_problem_id" => entry.fetch("root_problem_id"),
            "source" => entry.fetch("source"),
            "source_observed_in_current_run" => false,
            "tracked_status" => entry.fetch("status")
          }
        end
        (retrieved + persistent).group_by { |item| item.fetch("root_problem_id") }
                                .values
                                .map { |items| items.find { |item| item["source_observed_in_current_run"] } || items.first }
                                .sort_by { |item| item.fetch("root_problem_id") }
      end

      def self.run_summary(report, paths)
        {
          "backend" => report.dig("collection", "backend"),
          "candidate_counts" => report.fetch("candidate_counts"),
          "external_action_authorized" => false,
          "paths" => paths,
          "run_status" => report.fetch("run_status")
        }
      end
    end
  end
end

if $PROGRAM_NAME == __FILE__
  exit(TITMASScout::Discovery::CLI.run(ARGV))
end
