# frozen_string_literal: true

module TITMASScout
  module Discovery
    class ActionabilityClassifier
      CLASSIFICATIONS = %w[
        ACTIONABLE_NOW ACTIONABLE_AFTER_CONTACT OBSERVE EXCLUDE
      ].freeze
      CONTRIBUTION_LABELS = [
        "contributions welcome", "good first issue", "help wanted"
      ].freeze
      CONTACT_FIRST_PATTERNS = [
        /should\s+(?:first\s+)?talk\s+to/i,
        /talk\s+to\s+\S+\s+first/i,
        /contact\s+(?:the\s+)?maintainer\s+first/i,
        /discuss\s+(?:the\s+)?design\s+first/i
      ].freeze
      RESEARCH_PIPELINE_PATTERNS = [
        /filed\s+via\s+the\s+nightly\s+research/i,
        /nightly\s+research.{0,8}issues\s+pipeline/i
      ].freeze

      def classify(signal)
        classification, reason_code = classification_for(signal)
        {
          "classification" => classification,
          "evidence" => evidence(signal),
          "external_action_authorized" => false,
          "reason_code" => reason_code
        }
      end

      private

      def classification_for(signal)
        unless %w[GITHUB_ISSUE GITHUB_DISCUSSION].include?(signal["source_type"])
          return ["EXCLUDE", "SOURCE_TYPE_UNKNOWN"]
        end
        return ["EXCLUDE", "SOURCE_STATE_UNKNOWN"] unless signal["state"].is_a?(String)
        return ["EXCLUDE", "SOURCE_NOT_OPEN"] unless signal["state"] == "OPEN"
        return ["EXCLUDE", "LOCK_STATE_UNKNOWN"] unless [true, false].include?(signal["is_locked"])
        return ["EXCLUDE", "PUBLIC_ENTRY_LOCKED"] if signal["is_locked"] == true
        return ["EXCLUDE", "ASSIGNEE_EVIDENCE_UNKNOWN"] unless signal["assignees"].is_a?(Array)
        return ["OBSERVE", "AUTOMATED_RESEARCH_SUMMARY_NO_PROJECT_ACTION"] if research_summary?(signal)
        if automated_author?(signal) && !explicit_contribution_signal?(signal)
          return ["OBSERVE", "AUTOMATED_AUTHOR_WITHOUT_EXTERNAL_CONTRIBUTION_INVITATION"]
        end
        if assigned?(signal) && !explicit_contribution_signal?(signal)
          return ["OBSERVE", "ASSIGNED_WITHOUT_EXTERNAL_CONTRIBUTION_INVITATION"]
        end
        return ["ACTIONABLE_AFTER_CONTACT", "CONTACT_FIRST_INSTRUCTION"] if contact_first?(signal)

        ["ACTIONABLE_NOW", "OPEN_PUBLIC_COMMENT_ENTRY"]
      end

      def assigned?(signal)
        !Array(signal["assignees"]).empty?
      end

      def automated_author?(signal)
        signal["author"].to_s.end_with?("[bot]")
      end

      def explicit_contribution_signal?(signal)
        labels = Array(signal["labels"]).map(&:downcase)
        !(labels & CONTRIBUTION_LABELS).empty?
      end

      def contact_first?(signal)
        text = [signal["title"], signal["body"]].join(" ")
        CONTACT_FIRST_PATTERNS.any? { |pattern| pattern.match?(text) }
      end

      def research_summary?(signal)
        text = [signal["title"], signal["body"]].join(" ")
        RESEARCH_PIPELINE_PATTERNS.any? { |pattern| pattern.match?(text) }
      end

      def evidence(signal)
        {
          "assignees" => signal["assignees"]&.sort,
          "comments_count" => signal["comments_count"],
          "is_locked" => signal["is_locked"],
          "labels" => Array(signal["labels"]).sort,
          "source" => signal["url"],
          "state" => signal["state"]
        }
      end
    end
  end
end
