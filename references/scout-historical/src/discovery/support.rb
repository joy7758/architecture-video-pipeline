# frozen_string_literal: true

require "digest"
require "time"

module TITMASScout
  module Discovery
    module Support
      BAND_VALUES = {
        "HIGH" => 3,
        "MEDIUM" => 2,
        "LOW" => 1,
        "NEEDS_REVIEW" => 0
      }.freeze

      EFFORT_VALUES = {
        "LOW_EFFORT" => 3,
        "MEDIUM_EFFORT" => 2,
        "HIGH_EFFORT" => 1,
        "NEEDS_REVIEW" => 0
      }.freeze

      module_function

      def deep_sort(value)
        case value
        when Hash
          value.keys.sort.each_with_object({}) do |key, sorted|
            sorted[key] = deep_sort(value[key])
          end
        when Array
          value.map { |item| deep_sort(item) }
        else
          value
        end
      end

      def normalize_text(value)
        value.to_s
             .encode("UTF-8", invalid: :replace, undef: :replace, replace: "")
             .gsub(/```.*?```/m, " ")
             .gsub(/\[([^\]]+)\]\((?:https?:\/\/|mailto:)[^)]+\)/i, '\\1')
             .gsub(%r{https?://\S+}i, "[public-link-omitted]")
             .gsub(/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i,
                   "[public-email-redacted]")
             .gsub(/[`*_>#]/, " ")
             .gsub(/\s+/, " ")
             .strip
      end

      def truncate(value, maximum)
        text = normalize_text(value)
        return text if text.length <= maximum

        cutoff = maximum - 1
        excerpt = text[0, cutoff].rstrip
        boundary = excerpt.rindex(/\s/)
        excerpt = excerpt[0, boundary].rstrip if boundary && boundary >= cutoff / 2
        "#{excerpt}…"
      end

      def parse_time(value)
        Time.iso8601(value.to_s).utc
      rescue ArgumentError
        nil
      end

      def sha256_file(path)
        Digest::SHA256.file(path).hexdigest
      end

      def band_value(value)
        BAND_VALUES.fetch(value, 0)
      end

      def effort_value(value)
        EFFORT_VALUES.fetch(value, 0)
      end

      def string_array(value)
        Array(value).map(&:to_s).reject(&:empty?)
      end
    end
  end
end
