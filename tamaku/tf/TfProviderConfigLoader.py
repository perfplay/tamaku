import json
import jsonschema
from typing import Dict, Any, Optional
from tamaku.DataClasses import Config, Provider
from tamaku.BaseConfigLoader import BaseConfigLoader
from tamaku.utils.Logger import Logger

logger = Logger()


class TfProviderConfigLoader(BaseConfigLoader):
    def load_config(self, config_file: str) -> Optional[Config]:
        config_dict = self.load_config_file(config_file)
        if config_dict and self.validate_config(config_dict):
            return self.convert_to_dataclass(config_dict)
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
                "mirror_path": {"type": ["string", "null"]},
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
            "required": ["registry", "providers"]
        }
        try:
            jsonschema.validate(instance=config, schema=schema)
            logger.info("Configuration is valid")
            return True
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            return False

    @staticmethod
    def convert_to_dataclass(config: Dict[str, Any]) -> Config:
        providers = [
            Provider(
                namespace=p["namespace"],
                name=p["name"],
                minimal_version=p.get("minimal_version"),
                versions=p.get("versions", [])
            )
            for p in config.get("providers", [])
        ]
        return Config(
            registry=config["registry"],
            platforms=config.get("platforms", []),
            mirror_path=config.get("mirror_path") or "mirror",
            providers=providers
        )