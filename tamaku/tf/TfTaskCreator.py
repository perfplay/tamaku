from typing import Dict, Any

from tamaku.BaseTaksCreator import BaseTaskCreator
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfProviderVersionFetcher import TfProviderVersionFetcher
from tamaku.utils.Logger import Logger

logger = Logger()


class TfTaskCreator(BaseTaskCreator):
    def __init__(self, config_path: str, registry_url: str):
        super().__init__(config_path, registry_url)

    def load_config(self) -> Dict[str, Any]:
        loader = TfProviderConfigLoader()
        config = loader.load_config(self.config_path)
        if not config:
            raise ValueError(f"Failed to load config from {self.config_path}")
        return config

    def create_tasks(self) -> Dict[str, Any]:
        tasks = {"tasks": []}
        for provider_data in self.config.get("providers", []):
            provider_versions = TfProviderVersionFetcher(
                registry_url=self.registry_url,
                namespace=provider_data.get("namespace"),
                name=provider_data.get("name")
            )
            provider_versions.fetch_versions()
            provider_data["fetched_versions"] = provider_versions.current_versions_str
            tasks["tasks"].append(provider_data)
        return tasks
