import json
from tamaku.utils.Logger import Logger
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = Logger()


class BaseConfigLoader(ABC):
    @abstractmethod
    def load_config(self, config_file: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        pass

    @staticmethod
    def load_config_file(config_file: str) -> Dict[str, Any]:
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Loaded configuration from {config_file}")
            return config
        except Exception as e:
            logger.error(f"Failed to load configuration file: {e}")
            return None
