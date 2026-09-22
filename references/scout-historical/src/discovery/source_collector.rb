# frozen_string_literal: true

require "json"
require "date"
require "net/http"
require "open3"
require "openssl"
require "socket"
require "uri"
require_relative "support"

module TITMASScout
  module Discovery
    class SourceCollector
      HttpResponse = Struct.new(:status, :body, :headers)

      class HttpTransport
        attr_reader :events

        def initialize
          @events = []
        end

        def get(uri, headers)
          raise ArgumentError, "Only HTTPS GitHub API GET is allowed" unless allowed_uri?(uri)

          request = Net::HTTP::Get.new(uri)
          headers.each { |key, value| request[key] = value }
          response = Net::HTTP.start(
            uri.host,
            uri.port,
            use_ssl: true,
            open_timeout: 15,
            read_timeout: 30
          ) { |http| http.request(request) }

          event = {
            "host" => uri.host,
            "method" => "GET",
            "path" => uri.path,
            "status" => response.code.to_i
          }
          @events << event

          HttpResponse.new(
            response.code.to_i,
            response.body.to_s,
            {
              "x-ratelimit-limit" => response["x-ratelimit-limit"],
              "x-ratelimit-remaining" => response["x-ratelimit-remaining"],
              "x-ratelimit-reset" => response["x-ratelimit-reset"],
              "x-ratelimit-resource" => response["x-ratelimit-resource"]
            }
          )
        end

        private

        def allowed_uri?(uri)
          uri.is_a?(URI::HTTPS) && uri.host == "api.github.com"
        end
      end

      class CommandRunner
        def call(arguments)
          stdout, stderr, status = Open3.capture3(*arguments)
          {
            "stdout" => stdout,
            "stderr" => stderr,
            "success" => status.success?,
            "exit_status" => status.exitstatus
          }
        end
      end

      GH_ISSUE_FIELDS = %w[
        assignees author authorAssociation body commentsCount createdAt id isLocked
        isPullRequest labels number repository state title updatedAt url
      ].join(",").freeze

      READ_ONLY_GH_COMMANDS = [
        %w[gh version],
        %w[gh auth status],
        %w[gh search issues]
      ].freeze

      TRANSIENT_NETWORK_ERRORS = [
        EOFError,
        Errno::ECONNRESET,
        Errno::ETIMEDOUT,
        IOError,
        Net::OpenTimeout,
        Net::ReadTimeout,
        OpenSSL::SSL::SSLError,
        SocketError
      ].freeze

      PUBLIC_REST_MAX_ATTEMPTS = 3

      attr_reader :http_transport

      def initialize(config:, run_date:, retrieved_at:, http_transport: nil,
                     command_runner: nil)
        @config = config
        @policy = config.fetch("collection_policy")
        @run_date = run_date
        @retrieved_at = retrieved_at.utc
        @http_transport = http_transport || HttpTransport.new
        @command_runner = command_runner || CommandRunner.new
        @command_events = []
      end

      def collect
        gh = probe_github_cli
        backend = choose_backend(gh)
        query_records = []
        items = []

        configured_queries.each do |query_definition|
          record = collect_query(query_definition, backend)
          query_records << record.reject { |key, _| key == "items" }
          items.concat(record.fetch("items", []))
        end

        successful = query_records.count { |record| record["status"] == "SUCCESS" }
        coverage = if successful.zero?
                     "BLOCKED"
                   elsif successful == query_records.length
                     "PARTIAL_ISSUES_ONLY"
                   else
                     "PARTIAL_QUERY_FAILURES_AND_ISSUES_ONLY"
                   end

        {
          "backend" => backend,
          "collection_status" => coverage,
          "command_events" => @command_events,
          "discussion_coverage" => discussion_coverage(gh),
          "external_write_operations_observed" => 0,
          "gh_cli" => gh,
          "http_events" => http_events,
          "items" => items,
          "queries" => query_records,
          "retrieved_at" => @retrieved_at.iso8601,
          "source_types_collected" => successful.positive? ? ["GITHUB_ISSUE"] : [],
          "source_types_missing" => ["GITHUB_DISCUSSION"],
          "successful_query_count" => successful,
          "total_query_count" => query_records.length
        }
      end

      private

      def configured_queries
        maximum = Integer(@policy.fetch("maximum_queries_per_run"))
        @config.fetch("queries").first(maximum)
      end

      def probe_github_cli
        version = run_command(%w[gh version], "GH_VERSION")
        unless version["success"]
          return {
            "auth_status" => "NOT_CHECKED",
            "installed" => false,
            "reason_code" => "GH_NOT_INSTALLED",
            "search_available" => false,
            "version" => nil
          }
        end

        auth = run_command(
          %w[gh auth status --hostname github.com],
          "GH_AUTH_STATUS"
        )
        {
          "auth_status" => auth["success"] ? "AUTHENTICATED" : "INVALID",
          "installed" => true,
          "reason_code" => auth["success"] ? nil : "GH_AUTH_INVALID",
          "search_available" => auth["success"],
          "version" => version["stdout"].lines.first.to_s.strip
        }
      end

      def choose_backend(gh)
        return "GH_CLI_AUTHENTICATED" if gh["search_available"]
        return "GITHUB_PUBLIC_REST_GET_ONLY" if @policy["fallback_allowed"]

        "UNAVAILABLE"
      end

      def collect_query(definition, backend)
        topic_query = definition.fetch("query")
        raw_query = final_query(topic_query)
        base = {
          "backend" => backend,
          "github_total_count" => nil,
          "items" => [],
          "query" => raw_query,
          "query_id" => definition.fetch("query_id"),
          "retrieved_at" => @retrieved_at.iso8601,
          "topic_query" => topic_query,
          "topic" => definition.fetch("topic")
        }

        case backend
        when "GH_CLI_AUTHENTICATED"
          collect_with_gh(base)
        when "GITHUB_PUBLIC_REST_GET_ONLY"
          collect_with_public_rest(base)
        else
          base.merge(
            "error" => "No live GitHub read backend is available.",
            "reason_code" => "SOURCE_BACKEND_UNAVAILABLE",
            "retrieved_count" => 0,
            "status" => "BLOCKED"
          )
        end
      rescue JSON::ParserError => error
        base.merge(
          "error" => Support.truncate(error.message, 240),
          "reason_code" => "SOURCE_RESPONSE_INVALID_JSON",
          "retrieved_count" => 0,
          "status" => "FAILED"
        )
      rescue StandardError => error
        base.merge(
          "error" => Support.truncate(error.message, 240),
          "reason_code" => "SOURCE_COLLECTION_ERROR",
          "retrieved_count" => 0,
          "status" => "FAILED"
        )
      end

      def final_query(base_query)
        cutoff = @run_date - Integer(@policy.fetch("freshness_days"))
        [
          base_query,
          "is:issue",
          "is:open",
          "archived:false",
          "updated:>=#{cutoff.iso8601}"
        ].join(" ")
      end

      def collect_with_gh(base)
        arguments = [
          "gh", "search", "issues", base.fetch("topic_query"),
          "--archived=false",
          "--state", "open",
          "--updated", ">=#{freshness_cutoff}",
          "--visibility", "public",
          "--limit", @policy.fetch("per_query_limit").to_s,
          "--json", GH_ISSUE_FIELDS
        ]
        result = run_command(arguments, "GH_SEARCH_ISSUES")
        unless result["success"]
          return base.merge(
            "error" => Support.truncate(result["stderr"], 240),
            "reason_code" => "GH_SEARCH_FAILED",
            "retrieved_count" => 0,
            "status" => "FAILED"
          )
        end

        parsed = JSON.parse(result["stdout"])
        items = parsed.map { |item| normalize_gh_item(item, base) }
        base.merge(
          "github_total_count" => nil,
          "items" => items,
          "rate_limit" => {},
          "retrieved_count" => items.length,
          "status" => "SUCCESS"
        )
      end

      def freshness_cutoff
        (@run_date - Integer(@policy.fetch("freshness_days"))).iso8601
      end

      def collect_with_public_rest(base)
        uri = URI("#{@policy.fetch("public_api_base")}/search/issues")
        uri.query = URI.encode_www_form(
          "order" => "desc",
          "per_page" => Integer(@policy.fetch("per_query_limit")),
          "q" => base.fetch("query"),
          "sort" => "updated"
        )
        response, transport_retry_count = public_rest_get_with_retry(
          uri,
          {
            "Accept" => "application/vnd.github+json",
            "User-Agent" => @policy.fetch("user_agent"),
            "X-GitHub-Api-Version" => "2022-11-28"
          }
        )

        unless response.status == 200
          return base.merge(
            "error" => public_error(response),
            "rate_limit" => compact_headers(response.headers),
            "reason_code" => "PUBLIC_REST_SEARCH_FAILED",
            "retrieved_count" => 0,
            "status" => "FAILED"
          )
        end

        parsed = JSON.parse(response.body)
        items = parsed.fetch("items", []).map do |item|
          normalize_rest_item(item, base)
        end
        base.merge(
          "github_total_count" => parsed["total_count"],
          "items" => items,
          "rate_limit" => compact_headers(response.headers),
          "retrieved_count" => items.length,
          "transport_retry_count" => transport_retry_count,
          "status" => "SUCCESS"
        )
      end

      def public_rest_get_with_retry(uri, headers)
        attempts = 0

        begin
          attempts += 1
          response = @http_transport.get(uri, headers)
          [response, attempts - 1]
        rescue *TRANSIENT_NETWORK_ERRORS
          raise if attempts >= PUBLIC_REST_MAX_ATTEMPTS

          sleep(0.2 * attempts)
          retry
        end
      end

      def normalize_rest_item(item, base)
        repository = item.fetch("repository_url", "").split("/repos/").last
        {
          "assignees" => normalized_assignees(item, "assignees"),
          "author" => item.dig("user", "login"),
          "author_association" => item["author_association"],
          "body" => item["body"],
          "comments_count" => item["comments"],
          "created_at" => item["created_at"],
          "id" => item["node_id"] || item["id"].to_s,
          "is_locked" => normalized_boolean(item, "locked"),
          "is_pull_request" => item.key?("pull_request"),
          "labels" => Array(item["labels"]).map { |label| label["name"] },
          "number" => item["number"],
          "query_ids" => [base.fetch("query_id")],
          "repository" => repository,
          "source_type" => "GITHUB_ISSUE",
          "state" => item["state"].to_s.upcase,
          "title" => item["title"],
          "updated_at" => item["updated_at"],
          "url" => item["html_url"]
        }
      end

      def normalize_gh_item(item, base)
        {
          "assignees" => normalized_assignees(item, "assignees"),
          "author" => item.dig("author", "login"),
          "author_association" => item["authorAssociation"],
          "body" => item["body"],
          "comments_count" => item["commentsCount"],
          "created_at" => item["createdAt"],
          "id" => item["id"],
          "is_locked" => normalized_boolean(item, "isLocked"),
          "is_pull_request" => item["isPullRequest"] == true,
          "labels" => Array(item["labels"]).map { |label| label["name"] },
          "number" => item["number"],
          "query_ids" => [base.fetch("query_id")],
          "repository" => item.dig("repository", "nameWithOwner"),
          "source_type" => "GITHUB_ISSUE",
          "state" => item["state"].to_s.upcase,
          "title" => item["title"],
          "updated_at" => item["updatedAt"],
          "url" => item["url"]
        }
      end

      def discussion_coverage(gh)
        if gh["auth_status"] == "AUTHENTICATED"
          {
            "reason_code" => "GLOBAL_DISCUSSION_COLLECTION_NOT_ENABLED_V0_1",
            "status" => "NOT_COLLECTED"
          }
        else
          {
            "reason_code" => "GH_AUTH_INVALID_GRAPHQL_UNAVAILABLE",
            "status" => "BLOCKED"
          }
        end
      end

      def normalized_assignees(item, key)
        value = item[key]
        return nil unless value.is_a?(Array)

        logins = value.map do |assignee|
          next unless assignee.is_a?(Hash)

          login = assignee["login"]
          login if login.is_a?(String) && !login.empty?
        end
        return nil if logins.any?(&:nil?)

        logins.sort
      end

      def normalized_boolean(item, key)
        value = item[key]
        [true, false].include?(value) ? value : nil
      end

      def run_command(arguments, kind)
        unless read_only_command?(arguments)
          raise ArgumentError, "GitHub command is outside the read-only allowlist"
        end

        result = @command_runner.call(arguments)
        @command_events << {
          "arguments" => arguments,
          "exit_status" => result["exit_status"],
          "kind" => kind,
          "read_only" => true
        }
        result
      end

      def read_only_command?(arguments)
        READ_ONLY_GH_COMMANDS.any? do |prefix|
          arguments.first(prefix.length) == prefix
        end
      end

      def http_events
        return [] unless @http_transport.respond_to?(:events)

        @http_transport.events
      end

      def compact_headers(headers)
        headers.each_with_object({}) do |(key, value), compact|
          compact[key] = value unless value.nil? || value.to_s.empty?
        end
      end

      def public_error(response)
        parsed = JSON.parse(response.body)
        Support.truncate(parsed["message"] || response.body, 240)
      rescue JSON::ParserError
        Support.truncate(response.body, 240)
      end
    end
  end
end
