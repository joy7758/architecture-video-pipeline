# frozen_string_literal: true

require "json"
require "optparse"
require_relative "policy_loader"
require_relative "quorum_aggregator"
require_relative "review_result"
require_relative "review_input"

module TITMASScout
  module Review
    class CLI
      DEFAULT_POLICY = "config/agent-review-policy.yaml"

      def self.run(arguments, stdout: $stdout, stderr: $stderr)
        options = { policy: DEFAULT_POLICY }
        parser = OptionParser.new do |opts|
          opts.banner = "Usage: ruby src/review/cli.rb --input INPUT.json --action ACTION REVIEW.json..."
          opts.on("--policy PATH") do |value|
            raise ArgumentError, "--policy provided more than once" if options[:policy_explicit]

            options[:policy] = value
            options[:policy_explicit] = true
          end
          opts.on("--input PATH") do |value|
            raise ArgumentError, "--input provided more than once" if options[:input]

            options[:input] = value
          end
          opts.on("--action ACTION") do |value|
            raise ArgumentError, "--action provided more than once" if options[:action]

            options[:action] = value
          end
        end
        paths = parser.parse(arguments)
        raise ArgumentError, "--input is required" unless options[:input]
        raise ArgumentError, "--action is required" unless options[:action]

        policy = PolicyLoader.load(options.fetch(:policy))
        review_input = ReviewInput.load(options.fetch(:input))
        reviews = paths.map { |path| ReviewResult.load(path) }
        result = QuorumAggregator.new(policy).aggregate(
          reviews,
          review_input: review_input,
          requested_action: options.fetch(:action)
        )
        stdout.puts(JSON.pretty_generate(result))
        result["decision"] == "ALLOW" ? 0 : 1
      rescue OptionParser::ParseError, Errno::ENOENT, Errno::EACCES,
             Psych::Exception, JSON::ParserError, DuplicateJSONKeyError,
             PolicyError, ArgumentError => error
        ruleset = policy&.policy_version || "UNKNOWN"
        result = QuorumAggregator.fail_closed_result(
          actions: options && options[:action] ? [options[:action]] : [],
          reason: "INPUT_LOAD_OR_POLICY_ERROR:#{error.class}",
          ruleset_version: ruleset
        )
        stdout.puts(JSON.pretty_generate(result))
        stderr.puts(error.message)
        2
      end
    end
  end
end

exit(TITMASScout::Review::CLI.run(ARGV)) if $PROGRAM_NAME == __FILE__
