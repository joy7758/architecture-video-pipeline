# frozen_string_literal: true

require "yaml"
require_relative "review_result"

module TITMASScout
  module Review
    class PolicyError < StandardError; end

    class PolicyLoader
      REQUIRED_KEYS = %w[
        policy_version
        policy_id
        default_mode
        required_reviewers
        reviewer_decisions
        aggregation
        agent_authorizable_actions
        human_exception_actions
        unknown_action
      ].freeze
      AGGREGATION = {
        "all_pass" => "ALLOW",
        "blocking_failure" => "DENY",
        "conflict" => "BLOCKED_BY_CONFLICT",
        "missing_evidence" => "BLOCKED_BY_MISSING_EVIDENCE"
      }.freeze
      AGENT_ACTIONS = %w[
        PUBLIC_READ
        CREATE_FORK
        PUSH_PERSONAL_BRANCH
        OPEN_DRAFT_PR
        MARK_PR_READY_FOR_REVIEW
        POST_BOUNDED_TECHNICAL_COMMENT
        UPDATE_SCOUT_STATUS
      ].freeze
      HUMAN_ACTIONS = %w[
        SIGN_LEGAL_AGREEMENT
        MAKE_PAYMENT
        SUBMIT_BINDING_BID
        MAKE_IRREVOCABLE_IDENTITY_COMMITMENT
        DISCLOSE_RESTRICTED_DATA
        DISCLOSE_SECRET_OR_KEY
        DELETE_REMOTE_ASSET
        CHANGE_ACCOUNT_SECURITY
        MERGE_PROTECTED_BRANCH
      ].freeze

      attr_reader :data

      def self.load(path)
        content = File.read(path)
        reject_duplicate_mapping_keys!(Psych.parse_stream(content))
        data = YAML.safe_load(
          content,
          permitted_classes: [],
          permitted_symbols: [],
          aliases: false,
          filename: path
        )
        new(data)
      end

      def self.reject_duplicate_mapping_keys!(node)
        if node.is_a?(Psych::Nodes::Mapping)
          seen = {}
          node.children.each_slice(2) do |key_node, value_node|
            key = key_node.respond_to?(:value) ? key_node.value : key_node.to_s
            raise PolicyError, "DUPLICATE_POLICY_KEY:#{key}" if seen[key]

            seen[key] = true
            reject_duplicate_mapping_keys!(value_node)
          end
        elsif node.respond_to?(:children)
          Array(node.children).each { |child| reject_duplicate_mapping_keys!(child) }
        end
      end

      def initialize(data)
        @data = deep_copy(data)
        validate!
        deep_freeze(@data)
      end

      def policy_version
        data.fetch("policy_version")
      end

      def policy_id
        data.fetch("policy_id")
      end

      def required_reviewers
        data.fetch("required_reviewers")
      end

      def agent_authorizable_actions
        data.fetch("agent_authorizable_actions")
      end

      def human_exception_actions
        data.fetch("human_exception_actions")
      end

      private

      def deep_copy(value)
        case value
        when Hash
          value.each_with_object({}) do |(key, nested), copy|
            copy[key] = deep_copy(nested)
          end
        when Array
          value.map { |nested| deep_copy(nested) }
        else
          value.dup
        end
      rescue TypeError
        value
      end

      def deep_freeze(value)
        case value
        when Hash
          value.each do |key, nested|
            deep_freeze(key)
            deep_freeze(nested)
          end
        when Array
          value.each { |nested| deep_freeze(nested) }
        end
        value.freeze
      end

      def validate!
        raise PolicyError, "POLICY_NOT_OBJECT" unless data.is_a?(Hash)
        raise PolicyError, "POLICY_KEYS_INVALID" unless data.keys.map(&:to_s).sort == REQUIRED_KEYS.sort
        raise PolicyError, "POLICY_VERSION_INVALID" unless data["policy_version"] == "0.1"
        unless data["policy_id"] == "TITMAS-SCOUT-AGENT-REVIEW-POLICY-V0.1"
          raise PolicyError, "POLICY_ID_INVALID"
        end
        raise PolicyError, "DEFAULT_MODE_INVALID" unless data["default_mode"] == "AGENT_QUORUM"
        unless data["required_reviewers"] == ReviewResult::ROLES
          raise PolicyError, "REQUIRED_REVIEWERS_INVALID"
        end
        unless data["reviewer_decisions"] == ReviewResult::DECISIONS
          raise PolicyError, "REVIEWER_DECISIONS_INVALID"
        end
        raise PolicyError, "AGGREGATION_INVALID" unless data["aggregation"] == AGGREGATION
        unless data["agent_authorizable_actions"] == AGENT_ACTIONS
          raise PolicyError, "AGENT_ACTIONS_INVALID"
        end
        unless data["human_exception_actions"] == HUMAN_ACTIONS
          raise PolicyError, "HUMAN_ACTIONS_INVALID"
        end
        unless (AGENT_ACTIONS & HUMAN_ACTIONS).empty?
          raise PolicyError, "ACTION_CLASSES_OVERLAP"
        end
        raise PolicyError, "UNKNOWN_ACTION_POLICY_INVALID" unless data["unknown_action"] == "DENY"
      end
    end
  end
end
