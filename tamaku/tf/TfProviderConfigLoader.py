import json
import jsonschema
from typing import Dict, Any
from tamaku.BaseConfigLoader import BaseConfigLoader
from tamaku.utils.Logger import Logger

logger = Logger()


class TfProviderConfigLoader(BaseConfigLoader):
    def load_config(self, config_file: str) -> Dict[str, Any]:
        config = self.load_config_file(config_file)
        if config and self.validate_config(config):
            return config
        return None

    def validate_config(self, config: Dict[str, Any]) -> bool:
        schema = {
            "type": "object",
            "properties": {
                "registry": {"type": "string"},
                "platforms": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "providers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "namespace": {"type": "string"},
                            "name": {"type": "string"},
                            "minimal_version": {"type": ["string", "null"]},
                            "versions": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["namespace", "name"]
                    }
                }
            },
            "required": ["providers"]
        }
        try:
            jsonschema.validate(instance=config, schema=schema)
            logger.info("Configuration is valid")
            return True
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            return False
