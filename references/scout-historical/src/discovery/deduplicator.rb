# frozen_string_literal: true

module TITMASScout
  module Discovery
    class Deduplicator
      def deduplicate(items)
        groups = {}
        Array(items).each do |item|
          key = canonical_key(item)
          if groups.key?(key)
            groups[key]["query_ids"] = (
              Array(groups[key]["query_ids"]) + Array(item["query_ids"])
            ).uniq.sort
          else
            groups[key] = Marshal.load(Marshal.dump(item))
          end
        end

        unique = groups.keys.sort.map { |key| groups.fetch(key) }
        {
          "duplicate_count" => Array(items).length - unique.length,
          "input_count" => Array(items).length,
          "items" => unique,
          "unique_count" => unique.length
        }
      end

      private

      def canonical_key(item)
        repository = item["repository"].to_s.downcase
        number = item["number"].to_s
        source_type = item["source_type"].to_s
        return [source_type, repository, number].join(":") unless repository.empty? || number.empty?

        [source_type, item["url"].to_s.downcase.sub(%r{/+\z}, "")].join(":")
      end
    end
  end
end
