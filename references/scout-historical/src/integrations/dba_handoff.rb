# frozen_string_literal: true

require "fileutils"
require "json"

module TITMASScout
  module Integrations
    class DbaHandoff
      STATUS = "READY_FOR_READ_ONLY_REVIEW_NOT_INTEGRATED"

      def initialize(output_root: "reports/titmas")
        @output_root = output_root
      end

      def write(name, payload)
        raise ArgumentError, "UNKNOWN_HANDOFF" unless %w[latest-run latest-opportunities latest-actions latest-evidence].include?(name)

        FileUtils.mkdir_p(@output_root)
        path = File.join(@output_root, "#{name}.json")
        document = {
          "artifact_type" => "TITMAS_SCOUT_DBA_HANDOFF",
          "schema_version" => "0.1",
          "handoff_status" => STATUS,
          "dba_repository_modified" => false,
          "dba_ingestion_observed" => false,
          "payload" => payload
        }
        temporary = "#{path}.tmp-#{Process.pid}"
        File.write(temporary, JSON.pretty_generate(document) + "\n")
        File.rename(temporary, path)
        path
      ensure
        File.delete(temporary) if defined?(temporary) && File.exist?(temporary)
      end
    end
  end
end
