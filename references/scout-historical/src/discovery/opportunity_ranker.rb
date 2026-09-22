# frozen_string_literal: true

require "date"
require_relative "actionability_classifier"
require_relative "support"

module TITMASScout
  module Discovery
    class OpportunityRanker
      HEURISTIC_ID = "heuristic_unvalidated_v0.1"

      def initialize(config:, run_date:)
        @config = config
        @policy = config.fetch("collection_policy")
        @exclusions = config.fetch("exclusion_policy")
        @ranking_policy = config.fetch("ranking_policy")
        @run_date = run_date
        @actionability_classifier = ActionabilityClassifier.new
      end

      def filter(signals)
        retained = []
        excluded = []

        Array(signals).each do |signal|
          reasons = exclusion_reasons(signal)
          if reasons.empty?
            retained << signal
          else
            excluded << {
              "number" => signal["number"],
              "repository" => signal["repository"],
              "source" => signal["url"],
              "title" => signal["title"],
              "reasons" => reasons.sort,
              "tracked_status" => signal.dig("history_status", "status"),
              "root_problem_id" => signal.dig("history_status", "root_problem_id"),
              "related_entries" => signal.dig("history_status", "related_entries"),
              "status_evidence_paths" => signal.dig("history_status", "evidence_paths")
            }
          end
        end

        {
          "excluded" => excluded.sort_by { |item| item["source"].to_s },
          "retained" => retained.sort_by { |item| item["url"].to_s }
        }
      end

      def rank(signals)
        ranked = Array(signals).map do |signal|
          classification = @actionability_classifier.classify(signal)
          factors = factor_results(signal, classification)
          signal.merge(
            "actionability_classification" => classification,
            "heuristic_model" => HEURISTIC_ID,
            "heuristic_unvalidated" => true,
            "ranking_factors" => factors,
            "ranking_status" => ranking_status(factors),
            "success_probability" => nil
          )
        end

        sorted = ranked.sort_by { |candidate| sort_tuple(candidate) }
        sorted.each_with_index.map do |candidate, index|
          candidate.merge(
            "ordering_basis" => ordering_basis(candidate),
            "priority_position" => index + 1
          )
        end
      end

      private

      def exclusion_reasons(signal)
        reasons = []
        reasons << "SOURCE_URL_MISSING" if signal["url"].to_s.empty?
        reasons << "SOURCE_NOT_OPEN" unless signal["state"] == "OPEN"
        reasons << "PUBLIC_ENTRY_LOCKED" if signal["is_locked"] == true
        reasons << "PULL_REQUEST_NOT_DISCOVERY_ISSUE" if signal["is_pull_request"] == true
        reasons << "STALE_NO_RECENT_ACTIVITY" if stale?(signal)
        reasons << "OUTSIDE_TITMAS_CAPABILITY_BOUNDARY" if signal["capability_mappings"].empty?
        reasons << "PAIN_POINT_NOT_CLASSIFIED" if signal["pain_classifications"].empty?
        reasons << "EXCLUDED_HISTORICAL_SIGNAL_636_NO_NEW_ENTRY" if excluded_url?(signal)
        reasons << "EXCLUDED_LABEL" if excluded_label?(signal)
        reasons << "PURE_NEWS_OR_ANNOUNCEMENT" if pure_news?(signal)
        reasons << "PROHIBITED_OR_PRIVATE_PARTICIPATION_PATH" if prohibited_entry?(signal)
        reasons << "ASSIGNED_INTERNAL_WORK_ITEM" if assigned_internal_work?(signal)
        if signal["history_status"]
          reasons << "ALREADY_TRACKED:#{signal.dig('history_status', 'status')}"
        end
        reasons
      end

      def stale?(signal)
        updated = Support.parse_time(signal["updated_at"])
        return true unless updated

        updated.to_date < (@run_date - Integer(@policy.fetch("freshness_days")))
      end

      def excluded_url?(signal)
        Array(@exclusions["excluded_source_urls"]).include?(signal["url"])
      end

      def excluded_label?(signal)
        labels = Array(signal["labels"]).map(&:downcase)
        excluded = Array(@exclusions["excluded_labels"]).map(&:downcase)
        !(labels & excluded).empty?
      end

      def pure_news?(signal)
        title = signal["title"].to_s.downcase
        Array(@exclusions["pure_news_keywords"]).any? do |keyword|
          title.include?(keyword.downcase)
        end
      end

      def prohibited_entry?(signal)
        text = [signal["title"], signal["body"]].join(" ").downcase
        Array(@exclusions["private_or_abusive_entry_keywords"]).any? do |keyword|
          text.include?(keyword.downcase)
        end
      end

      def assigned_internal_work?(signal)
        policy = @exclusions.fetch("assigned_internal_work", {})
        title = signal["title"].to_s
        body = signal["body"].to_s.downcase
        title_match = Array(policy["title_patterns"]).any? do |pattern|
          Regexp.new(pattern, Regexp::IGNORECASE).match?(title)
        end
        body_match = Array(policy["body_keywords"]).any? do |keyword|
          body.include?(keyword.downcase)
        end

        title_match && body_match
      end

      def factor_results(signal, classification)
        {
          "actionability" => actionability(classification),
          "effort" => effort(signal),
          "evidence_quality" => evidence_quality(signal),
          "expected_learning" => expected_learning(signal),
          "freshness" => freshness(signal),
          "pain_explicitness" => pain_explicitness(signal),
          "potential_value" => potential_value(signal),
          "titmas_relevance" => titmas_relevance(signal)
        }
      end

      def pain_explicitness(signal)
        length = Support.normalize_text(signal["body"]).length
        band = if length >= 300
                 "HIGH"
               elsif length >= 100
                 "MEDIUM"
               else
                 "LOW"
               end
        factor(band, "Source body length and explicit matched pain terms are reviewable.",
               signal["pain_classifications"].map { |match| match["evidence_snippet"] })
      end

      def titmas_relevance(signal)
        count = signal["capability_mappings"].length
        direct = direct_relevance_terms(signal)
        band = count >= 2 && !direct.empty? ? "HIGH" : "MEDIUM"
        factor(
          band,
          "#{count} bounded role mapping(s); direct title terms: #{direct.empty? ? "none" : direct.join(", ")}.",
          signal["capability_mappings"].map { |mapping| mapping["evidence_snippet"] }
        )
      end

      def actionability(classification)
        value = classification.fetch("classification")
        band = {
          "ACTIONABLE_NOW" => "HIGH",
          "ACTIONABLE_AFTER_CONTACT" => "MEDIUM",
          "OBSERVE" => "LOW",
          "EXCLUDE" => "LOW"
        }.fetch(value)
        factor(
          band,
          "Conversion readiness is #{value}; this classification does not authorize external action.",
          [classification.fetch("reason_code"), classification.dig("evidence", "source")]
        )
      end

      def expected_learning(signal)
        text = [signal["title"], signal["body"]].join(" ").downcase
        implementation_terms = %w[test implementation reproduce trace audit policy security rfc feature proposal]
        matched = implementation_terms.select { |term| text.include?(term) }
        title_direct = direct_relevance_terms(signal)
        band = matched.length >= 2 || !title_direct.empty? ? "HIGH" : "MEDIUM"
        factor(band, "A bounded contribution could test existing components; actual scope needs policy-selected review.",
               (matched + title_direct).uniq)
      end

      def potential_value(signal)
        factor(
          "NEEDS_REVIEW",
          "The Issue record does not establish adoption, collaboration, reputation, or revenue value.",
          [signal["url"]]
        )
      end

      def effort(signal)
        labels = Array(signal["labels"]).map(&:downcase)
        if labels.include?("good first issue")
          factor("LOW_EFFORT", "Repository labels the item as good first issue; scope still needs verification.",
                 ["good first issue"])
        else
          factor("NEEDS_REVIEW", "Repository code and contribution scope were not inspected.", [])
        end
      end

      def freshness(signal)
        updated = Support.parse_time(signal["updated_at"])
        return factor("NEEDS_REVIEW", "Updated timestamp is missing or invalid.", []) unless updated

        days = (@run_date - updated.to_date).to_i
        band = if days <= 14
                 "HIGH"
               elsif days <= 45
                 "MEDIUM"
               else
                 "LOW"
               end
        factor(band, "Source was updated #{days} day(s) before the run date.",
               [signal["updated_at"]])
      end

      def evidence_quality(signal)
        body_length = Support.normalize_text(signal["body"]).length
        labels = Array(signal["labels"])
        association = signal["author_association"].to_s.upcase
        maintainer_authored = %w[OWNER MEMBER COLLABORATOR].include?(association)
        band = if body_length >= 400 && (!labels.empty? || maintainer_authored)
                 "HIGH"
               elsif body_length >= 100
                 "MEDIUM"
               else
                 "LOW"
               end
        factor(band, "Public source metadata and a bounded source excerpt are available.",
               [signal["url"], "body_characters=#{body_length}", association])
      end

      def direct_relevance_terms(signal)
        title = signal["title"].to_s.downcase
        Array(@ranking_policy["direct_relevance_keywords"]).select do |keyword|
          title.include?(keyword.downcase)
        end.sort
      end

      def factor(band, reason, evidence)
        {
          "band" => band,
          "evidence" => Array(evidence).reject { |item| item.to_s.empty? },
          "reason" => reason
        }
      end

      def ranking_status(factors)
        values = factors.values.map { |factor_result| factor_result["band"] }
        values.include?("NEEDS_REVIEW") ? "NEEDS_REVIEW" : "HEURISTIC_ORDERED"
      end

      def sort_tuple(candidate)
        factors = candidate.fetch("ranking_factors")
        [
          actionability_priority(candidate),
          -Support.band_value(factors.dig("titmas_relevance", "band")),
          -Support.band_value(factors.dig("actionability", "band")),
          -Support.band_value(factors.dig("pain_explicitness", "band")),
          -Support.band_value(factors.dig("expected_learning", "band")),
          -Support.band_value(factors.dig("freshness", "band")),
          -Support.band_value(factors.dig("evidence_quality", "band")),
          -Support.band_value(factors.dig("potential_value", "band")),
          -Support.effort_value(factors.dig("effort", "band")),
          candidate["url"].to_s
        ]
      end

      def actionability_priority(candidate)
        {
          "ACTIONABLE_NOW" => 0,
          "ACTIONABLE_AFTER_CONTACT" => 1,
          "OBSERVE" => 2,
          "EXCLUDE" => 3
        }.fetch(candidate.dig("actionability_classification", "classification"), 4)
      end

      def ordering_basis(candidate)
        [{
          "factor" => "conversion_readiness",
          "band" => candidate.dig("actionability_classification", "classification")
        }] + %w[
          titmas_relevance actionability pain_explicitness expected_learning
          freshness evidence_quality potential_value effort
        ].map do |name|
          { "factor" => name, "band" => candidate.dig("ranking_factors", name, "band") }
        end
      end
    end
  end
end
