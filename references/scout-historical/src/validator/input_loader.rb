# frozen_string_literal: true

require "yaml"

module TITMASScout
  module Validator
    module InputLoader
      module_function

      def load_yaml(path)
        YAML.safe_load(
          File.read(path),
          permitted_classes: [],
          permitted_symbols: [],
          aliases: false,
          filename: path
        )
      end
    end
  end
end
