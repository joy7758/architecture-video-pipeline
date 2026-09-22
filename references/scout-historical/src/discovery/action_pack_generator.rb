# frozen_string_literal: true

require_relative "actionability_classifier"
require_relative "support"

module TITMASScout
  module Discovery
    class ActionPackGenerator
      ALLOWED_ACTIONS = %w[
        COMMENT DISCUSSION PR APPLICATION BID CONTACT OBSERVE
      ].freeze

      PROHIBITED_TEXT = [
        /```/,
        /\b(?:curl|wget)\b/i,
        /\bgh\s+(?:api|issue|pr|repo)\b/i,
        /api\.github\.com/i,
        /\b(?:POST|PUT|PATCH|DELETE)\s+https?:/i,
        /send\s+(?:this|the)\s+(?:message|email|application)/i
      ].freeze

      def generate(candidate)
        action = suggested_action(candidate)
        pack = {
          "estimated_effort" => candidate.dig("ranking_factors", "effort", "band"),
          "external_action_authorized" => false,
          "human_exception_decisions_required" => human_exception_decisions(action),
          "key_risks" => key_risks(candidate),
          "minimum_contribution" => minimum_contribution(action),
          "opportunity_summary" => Support.truncate(candidate["title"], 220),
          "original_source" => candidate["url"],
          "pain_point" => Support.truncate(candidate["pain_point"], 420),
          "possible_acceptance_reasons" => acceptance_reasons(candidate),
          "possible_rejection_reasons" => rejection_reasons,
          "reusable_components" => reusable_components(candidate),
          "suggested_action_type" => action
        }
        validate!(pack)
        pack
      end

      def validate!(pack)
        action = pack["suggested_action_type"]
        raise ArgumentError, "Unknown action suggestion" unless ALLOWED_ACTIONS.include?(action)
        raise ArgumentError, "Action Pack cannot authorize external action" unless pack["external_action_authorized"] == false

        text_values(pack).each do |value|
          if PROHIBITED_TEXT.any? { |pattern| pattern.match?(value) }
            raise ArgumentError, "Action Pack contains executable or send-ready content"
          end
        end
        true
      end

      private

      def suggested_action(candidate)
        readiness = candidate.dig("actionability_classification", "classification")
        unless ActionabilityClassifier::CLASSIFICATIONS.include?(readiness)
          raise ArgumentError, "Actionability classification is missing or unknown"
        end
        return "OBSERVE" if %w[OBSERVE EXCLUDE].include?(readiness)
        return "COMMENT" if readiness == "ACTIONABLE_AFTER_CONTACT"
        return "DISCUSSION" if candidate["source_type"] == "GITHUB_DISCUSSION"

        text = [candidate["title"], candidate["body"]].join(" ").downcase
        title = candidate["title"].to_s.downcase
        labels = Array(candidate["labels"]).map(&:downcase)
        return "COMMENT" if title.include?("[rfc]") || title.start_with?("rfc")
        return "OBSERVE" if text.include?("private vulnerability") || text.include?("security disclosure")
        return "PR" if (labels & ["help wanted", "good first issue", "contributions welcome"]).any?
        return "COMMENT" if text.match?(/\b(?:rfc|proposal|feedback|design|question)\b/)

        "COMMENT"
      end

      def minimum_contribution(action)
        case action
        when "PR"
          "Prepare a small reproducible test, documentation clarification, or bounded proof of concept for Agent Review Quorum before any submission."
        when "COMMENT", "DISCUSSION"
          "Prepare an evidence-backed scope question and a bounded component-mapping note for Agent Review Quorum; do not post automatically."
        else
          "Verify current maintainer interest, contribution policy, and scope before proposing participation."
        end
      end

      def reusable_components(candidate)
        candidate.fetch("capability_mappings").map do |mapping|
          {
            "bounded_role" => mapping["bounded_role"],
            "capability_id" => mapping["capability_id"],
            "mapping_evidence" => mapping["evidence_snippet"],
            "repository" => mapping["repository"]
          }
        end
      end

      def acceptance_reasons(candidate)
        [
          "The public source states a problem aligned with #{candidate["pain_classifications"].map { |item| item["classification"] }.join(", ")}.",
          "A bounded existing component role may support a small, reviewable contribution."
        ]
      end

      def rejection_reasons
        [
          "Maintainer interest and preferred contribution path are unconfirmed.",
          "The mapped TITMAS role may not fit repository architecture or scope.",
          "A similar fix may already exist outside the retrieved Issue record."
        ]
      end

      def key_risks(candidate)
        [
          "Keyword mapping can overstate relevance and is unvalidated.",
          "Open state does not imply permission to implement or contact anyone.",
          "Effort, license, and security facts require evidence; legal, payment, identity, privacy, deletion, and account-security exceptions require human review.",
          "Source freshness is limited to updated_at=#{candidate["updated_at"]}."
        ]
      end

      def human_exception_decisions(action)
        return [] if %w[COMMENT DISCUSSION PR OBSERVE].include?(action)

        [
          "Check whether #{action} creates a legal, payment, binding identity, privacy, deletion, account-security, or protected-branch exception.",
          "Obtain a separate human exception decision before any such effect."
        ]
      end

      def text_values(value)
        case value
        when Hash
          value.flat_map { |key, nested| [key.to_s] + text_values(nested) }
        when Array
          value.flat_map { |nested| text_values(nested) }
        else
          [value.to_s]
        end
      end
    end
  end
end
