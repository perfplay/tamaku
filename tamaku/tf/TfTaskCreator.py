from typing import Dict, Any, List
from tamaku.BaseTaskCreator import BaseTaskCreator
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfProviderVersionFetcher import TfProviderVersionFetcher
from tamaku.utils.Logger import Logger
from tamaku.utils.VersionFilter import VersionFilter

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
            versions_fetcher = TfProviderVersionFetcher(
                registry_url=self.registry_url,
                namespace=provider_data.get("namespace"),
                name=provider_data.get("name")
            )

            versions = versions_fetcher.fetch_versions()

            include_versions = provider_data.get("versions", [])
            min_version = provider_data.get("minimal_version")

            version_filter = VersionFilter(versions=versions, include=include_versions, min_version=min_version)
            filtered_versions = version_filter.filter_versions()

            task_data = self.generate_task_data(provider_data, filtered_versions)
            tasks["tasks"].append(task_data)
        return tasks

    @staticmethod
    def generate_task_data(provider_data: Dict[str, Any], versions: List[str]) -> Dict[str, Any]:
        task_data = {
            "namespace": provider_data.get("namespace"),
            "name": provider_data.get("name"),
            "versions": versions
        }
        return task_data
