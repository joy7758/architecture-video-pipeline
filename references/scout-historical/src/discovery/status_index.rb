# frozen_string_literal: true

require "json"

module TITMASScout
  module Discovery
    class StatusIndex
      STATUS_PRIORITY = {
        "DISCOVERED" => 0,
        "SELECTED" => 1,
        "ACTIVE_CONVERSION" => 2,
        "READY_FOR_REVIEW" => 3
      }.freeze
      HISTORY_DIRECTORIES = %w[
        conversion-runs publication-runs review-runs titmas-runs
        self-improvement-runs
      ].freeze
      ISSUE_URL = %r{https://github\.com/([^/]+/[^/]+)/issues/(\d+)}i
      PR_URL = %r{https://github\.com/([^/]+/[^/]+)/pull/(\d+)}i

      def initialize(reports_root: "reports")
        @reports_root = reports_root
        @entries = {}
        build
      end

      def status_for(signal)
        key = issue_key(signal["repository"], signal["number"])
        entry = @entries[key]
        entry && Marshal.load(Marshal.dump(entry))
      end

      def entries
        Marshal.load(Marshal.dump(@entries))
      end

      private

      def build
        history_paths.each do |path|
          document = JSON.parse(File.read(path))
          strings = collect_strings(document)
          issues = extract_issues(strings)
          pull_requests = extract_pull_requests(strings)
          status = status_for_path(path, document)
          issues.each do |issue|
            record(issue, status, path, related_entries: pull_requests)
          end
        rescue JSON::ParserError, Errno::ENOENT, Errno::EACCES
          next
        end
      end

      def history_paths
        HISTORY_DIRECTORIES.flat_map do |directory|
          Dir[File.join(@reports_root, directory, "**", "*.json")]
        end.uniq.sort
      end

      def collect_strings(value)
        case value
        when Hash
          value.flat_map { |key, nested| [key.to_s] + collect_strings(nested) }
        when Array
          value.flat_map { |nested| collect_strings(nested) }
        when String
          [value]
        else
          []
        end
      end

      def extract_issues(strings)
        found = []
        strings.each do |text|
          text.scan(ISSUE_URL) { |repository, number| found << issue_identity(repository, number) }
        end
        found.uniq { |item| item.fetch("root_problem_id") }
      end

      def extract_pull_requests(strings)
        strings.flat_map do |text|
          text.scan(PR_URL).map do |repository, number|
            "github:#{repository.downcase}:pull:#{number}"
          end
        end.uniq.sort
      end

      def issue_identity(repository, number)
        {
          "repository" => repository.downcase,
          "number" => Integer(number),
          "root_problem_id" => "github:#{repository.downcase}:issue:#{number}"
        }
      end

      def status_for_path(path, document)
        return "READY_FOR_REVIEW" if path.include?("/review-runs/") || path.include?("/titmas-runs/")
        if path.include?("/publication-runs/")
          serialized = JSON.generate(document)
          return "READY_FOR_REVIEW" if serialized.include?("READY_FOR_REVIEW")
          return "ACTIVE_CONVERSION"
        end
        return "ACTIVE_CONVERSION" if path.include?("/conversion-runs/")

        "SELECTED"
      end

      def record(issue, status, path, related_entries:)
        key = issue_key(issue.fetch("repository"), issue.fetch("number"))
        current = @entries[key]
        if current.nil? || STATUS_PRIORITY.fetch(status) > STATUS_PRIORITY.fetch(current.fetch("status"))
          current = {
            "number" => issue.fetch("number"),
            "repository" => issue.fetch("repository"),
            "status" => status,
            "root_problem_id" => issue.fetch("root_problem_id"),
            "source" => "https://github.com/#{issue.fetch('repository')}/issues/#{issue.fetch('number')}",
            "evidence_paths" => [],
            "related_entries" => []
          }
          @entries[key] = current
        end
        current["evidence_paths"] = (current.fetch("evidence_paths") + [relative_path(path)]).uniq.sort
        current["related_entries"] = (current.fetch("related_entries") + related_entries).uniq.sort
      end

      def relative_path(path)
        path.delete_prefix("#{@reports_root}/").prepend("reports/")
      end

      def issue_key(repository, number)
        "#{repository.to_s.downcase}##{number}"
      end
    end
  end
end
