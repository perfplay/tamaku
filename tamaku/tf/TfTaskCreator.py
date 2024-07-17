from typing import Dict, Any, List
from tamaku.BaseTaskCreator import BaseTaskCreator
from tamaku.tf.TfInstalledVersionsChecker import TfInstalledVersionsChecker
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.tf.TfProviderVersionFetcher import TfProviderVersionFetcher
from tamaku.utils.Logger import Logger
from tamaku.utils.VersionFilter import VersionFilter
from tamaku.DataClasses import Config, Provider, VersionWithPlatform

logger = Logger()


class TfTaskCreator(BaseTaskCreator):
    def __init__(self, config_path: str, registry_url: str):
        super().__init__(config_path, registry_url)

    def create_tasks(self) -> Dict[str, Any]:
        tasks = {"providers": []}
        loader = TfProviderConfigLoader()
        config = loader.load_config(self.config_path)

        installed_providers = TfInstalledVersionsChecker(self.config_path)
        logger.debug(f"Installed providers: {installed_providers.providers}")

        for provider_data in config.providers:
            versions_fetcher = TfProviderVersionFetcher(
                registry_url=config.registry,
                namespace=provider_data.namespace,
                name=provider_data.name
            )

            versions = versions_fetcher.fetch_versions()

            include_versions = provider_data.versions
            min_version = provider_data.minimal_version

            version_filter = VersionFilter(versions=versions, include=include_versions, min_version=min_version)
            filtered_versions = version_filter.filter_versions()
            logger.debug(f"Filtered versions for {provider_data.namespace}/{provider_data.name}: {filtered_versions}")

            filtered_versions_with_platforms = self.create_version_with_platforms(filtered_versions, config.platforms)
            logger.debug(f"Filtered versions with platforms: {filtered_versions_with_platforms}")

            installed_versions_with_platforms = self.get_installed_versions_with_platforms(installed_providers, provider_data.name, provider_data.namespace)
            logger.debug(f"Installed versions with platforms: {installed_versions_with_platforms}")

            tasks_versions_with_platforms = self.filter_installed_versions(filtered_versions_with_platforms, installed_versions_with_platforms)

            if tasks_versions_with_platforms:
                tasks_with_platforms = self.generate_task_data(provider_data, tasks_versions_with_platforms)
                tasks["providers"].append(tasks_with_platforms)
        logger.debug(f"Tasks created: {tasks}")
        return tasks

    @staticmethod
    def generate_task_data(provider_data: Provider, versions: List[VersionWithPlatform]) -> Dict[str, Any]:
        versions_dict = []
        for version in versions:
            versions_dict.append(version.to_dict())

        task_data = {
            "namespace": provider_data.namespace,
            "name": provider_data.name,
            "versions": versions_dict
        }
        logger.info(f"Task generated for {task_data['namespace']}/{task_data['name']} with versions {task_data['versions']}")
        return task_data

    @staticmethod
    def get_installed_versions_with_platforms(installed_providers, name, namespace) -> List[VersionWithPlatform]:
        for provider in installed_providers.providers:
            if provider.name == name and provider.namespace == namespace:
                logger.debug(f"Found installed versions for {namespace}/{name}: {provider.versions}")
                return provider.versions
        return []

    @staticmethod
    def create_version_with_platforms(filtered_versions: List[str], platforms: List[str]) -> List[VersionWithPlatform]:
        versions_with_platforms = []
        for version in filtered_versions:
            for platform in platforms:
                versions_with_platforms.append(VersionWithPlatform(version=version, platform=platform))
        return versions_with_platforms

    @staticmethod
    def filter_installed_versions(filtered_versions_with_platforms: List[VersionWithPlatform],
                                  installed_versions_with_platforms: List[VersionWithPlatform]) -> List[VersionWithPlatform]:
        installed_set = set(installed_versions_with_platforms)
        return [v for v in filtered_versions_with_platforms if v not in installed_set]
