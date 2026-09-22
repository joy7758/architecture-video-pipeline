# frozen_string_literal: true

require "json"
require "optparse"
require "time"
require_relative "input_loader"
require_relative "validation_aggregator"
require_relative "support"

module TITMASScout
  module Validator
    class CLI
      def self.run(argv, stdout: $stdout, stderr: $stderr)
        options = {}
        parser = OptionParser.new do |opts|
          opts.banner = "Usage: ruby src/validator/validate.rb [--timestamp UTC] INPUT.yaml"
          opts.on("--timestamp UTC", "Deterministic RFC 3339 UTC evaluation time for research tests") do |value|
            options[:timestamp] = value
          end
        end
        parser.parse!(argv)
        raise OptionParser::MissingArgument, "INPUT.yaml" unless argv.length == 1

        timestamp = parse_timestamp(options[:timestamp])
        path = argv.first
        document = InputLoader.load_yaml(path)
        result = ValidationAggregator.new(clock: -> { timestamp }).validate(
          document,
          input_source: path
        )
        stdout.puts(JSON.pretty_generate(Support.deep_sort(result)))
        result["validation_status"] == "VALID" ? 0 : 1
      rescue OptionParser::ParseError, Errno::ENOENT, Errno::EACCES, Psych::Exception, ArgumentError => error
        timestamp = timestamp_or_now(options && options[:timestamp])
        result = ValidationAggregator.execution_error(
          reason_code: "INPUT_LOAD_OR_PARSE_ERROR",
          message: "Input could not be evaluated: #{error.class}: #{error.message}",
          input_source: argv&.first,
          timestamp: timestamp
        )
        stdout.puts(JSON.pretty_generate(Support.deep_sort(result)))
        stderr.puts(parser) if error.is_a?(OptionParser::ParseError) && parser
        2
      end

      def self.parse_timestamp(value)
        return Time.now.utc unless value
        raise ArgumentError, "--timestamp must use RFC 3339 UTC seconds with Z" unless Support.utc_seconds?(value)

        Time.iso8601(value).utc
      end
      private_class_method :parse_timestamp

      def self.timestamp_or_now(value)
        Support.parse_utc(value) || Time.now.utc
      end
      private_class_method :timestamp_or_now
    end
  end
end

exit(TITMASScout::Validator::CLI.run(ARGV)) if $PROGRAM_NAME == __FILE__
