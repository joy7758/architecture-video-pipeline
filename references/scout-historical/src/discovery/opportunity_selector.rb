# frozen_string_literal: true

require_relative "actionability_classifier"

module TITMASScout
  module Discovery
    class OpportunitySelector
      CONVERSION_CLASSIFICATIONS = %w[
        ACTIONABLE_NOW ACTIONABLE_AFTER_CONTACT
      ].freeze

      def select(ranked_candidates, maximum:)
        candidates = Array(ranked_candidates)
        queue = candidates.select do |candidate|
          CONVERSION_CLASSIFICATIONS.include?(classification(candidate))
        end
        watchlist = candidates.select do |candidate|
          classification(candidate) == "OBSERVE"
        end
        excluded = candidates.each_with_object([]) do |candidate, items|
          value = classification(candidate)
          if value == "EXCLUDE"
            items << candidate
          elsif !ActionabilityClassifier::CLASSIFICATIONS.include?(value)
            items << unknown_exclusion(candidate)
          end
        end

        bounded_queue = queue.first(maximum)
        remaining = [maximum - bounded_queue.length, 0].max
        bounded_watchlist = watchlist.first(remaining)

        {
          "conversion_queue" => bounded_queue,
          "excluded_by_actionability" => excluded,
          "next_conversion_target" => queue.first,
          "report_candidates" => bounded_queue + bounded_watchlist,
          "research_watchlist" => bounded_watchlist
        }
      end

      private

      def classification(candidate)
        candidate.dig("actionability_classification", "classification")
      end

      def unknown_exclusion(candidate)
        candidate.merge(
          "actionability_classification" => {
            "classification" => "EXCLUDE",
            "evidence" => { "source" => candidate["url"] },
            "external_action_authorized" => false,
            "reason_code" => "ACTIONABILITY_CLASSIFICATION_UNKNOWN"
          }
        )
      end
    end
  end
end
