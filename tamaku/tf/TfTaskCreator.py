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

            installed_versions = self.get_installed_versions(installed_providers, provider_data.name, provider_data.namespace)

            filtered_versions = VersionFilter(versions=filtered_versions, exclude=installed_versions).filter_versions()

            # Генерируем задачи с учетом платформ
            tasks_with_platforms = self.generate_task_data(provider_data, filtered_versions, config.platforms)
            logger.debug(f"Generated tasks for {provider_data.namespace}/{provider_data.name}: {tasks_with_platforms}")
            tasks["providers"].append(tasks_with_platforms)

        return tasks

    @staticmethod
    def generate_task_data(provider_data: Provider, versions: List[str], platforms: List[str]) -> Dict[str, Any]:
        tasks = []
        for version in versions:
            for platform in platforms:
                tasks.append(VersionWithPlatform(version=str(version), platform=platform).to_dict())

        task_data = {
            "namespace": provider_data.namespace,
            "name": provider_data.name,
            "versions": tasks
        }
        logger.info(f"Task generated for {provider_data.namespace}/{provider_data.name}: {tasks}")
        return task_data

    @staticmethod
    def get_installed_versions(installed_providers, name, namespace) -> List[str]:
        installed_versions = []
        for provider in installed_providers.providers:
            if provider.name == name and provider.namespace == namespace:
                installed_versions.extend(provider.versions)
                logger.debug(f"Found installed provider: {provider}")
        return [v.version for v in installed_versions]