# frozen_string_literal: true

require_relative "support"

module TITMASScout
  module Discovery
    class SignalExtractor
      def initialize(config:)
        @config = config
        @taxonomy = config.fetch("pain_point_taxonomy")
        @capabilities = config.fetch("capability_mappings")
      end

      def extract(item)
        text = combined_text(item)
        classifications = extract_classifications(text)
        mappings = extract_capability_mappings(text)
        evidence_excerpt = source_evidence_excerpt(item, classifications)

        item.merge(
          "action_entry" => action_entry(item),
          "capability_mappings" => mappings,
          "pain_classifications" => classifications,
          "pain_point" => pain_point(item, evidence_excerpt),
          "source_evidence_excerpt" => evidence_excerpt,
          "unconfirmed_facts" => unconfirmed_facts
        )
      end

      private

      def combined_text(item)
        [
          item["title"],
          item["body"],
          Array(item["labels"]).join(" ")
        ].join(" ").downcase
      end

      def extract_classifications(text)
        @taxonomy.each_with_object([]) do |(classification, definition), matches|
          keywords = Array(definition["keywords"]).select do |keyword|
            text.include?(keyword.downcase)
          end
          next if keywords.empty?

          matches << {
            "classification" => classification,
            "evidence_snippet" => evidence_snippet(text, keywords.first),
            "matched_keywords" => keywords.sort
          }
        end.sort_by { |match| match.fetch("classification") }
      end

      def extract_capability_mappings(text)
        @capabilities.each_with_object([]) do |definition, matches|
          keywords = Array(definition["keywords"]).select do |keyword|
            text.include?(keyword.downcase)
          end
          next if keywords.empty?

          matches << {
            "bounded_role" => definition.fetch("bounded_role"),
            "capability_id" => definition.fetch("capability_id"),
            "evidence_snippet" => evidence_snippet(text, keywords.first),
            "matched_keywords" => keywords.sort,
            "repository" => definition.fetch("repository")
          }
        end.sort_by { |mapping| mapping.fetch("capability_id") }
      end

      def evidence_snippet(text, keyword)
        index = text.index(keyword.downcase) || 0
        start = [index - 70, 0].max
        if start.positive?
          boundary = text.index(/\s/, start)
          start = boundary + 1 if boundary && boundary < index
        end
        Support.truncate(text[start, 220], 200)
      end

      def source_evidence_excerpt(item, classifications)
        classified_excerpt = classifications.first&.fetch("evidence_snippet", nil)
        return classified_excerpt unless classified_excerpt.to_s.empty?

        Support.truncate(item["body"], 360)
      end

      def pain_point(item, evidence_excerpt)
        title = Support.truncate(item["title"], 180)
        excerpt = Support.truncate(evidence_excerpt, 240)
        return title if excerpt.empty?

        "#{title}: #{excerpt}"
      end

      def action_entry(item)
        {
          "entry_type" => item["source_type"],
          "is_locked" => item["is_locked"] == true,
          "public_url" => item["url"],
          "state" => item["state"]
        }
      end

      def unconfirmed_facts
        [
          "maintainer_interest",
          "contribution_acceptance",
          "current_unresolved_scope_beyond_open_state",
          "implementation_effort",
          "customer_demand",
          "commercial_budget_or_value",
          "legal_and_license_fit"
        ]
      end
    end
  end
end
