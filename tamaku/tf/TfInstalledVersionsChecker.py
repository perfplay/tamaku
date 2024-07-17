import os
import json
from typing import List, Dict, Optional
from tamaku.utils.Logger import Logger
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.DataClasses import InstalledProvider, VersionWithPlatform

logger = Logger(log_level="DEBUG")


class TfInstalledVersionsChecker:
    def __init__(self, config_path: str):
        self.providers = self.check_installed_versions(config_path)

    def check_installed_versions(self, config_path):
        loader = TfProviderConfigLoader()
        config = loader.load_config(config_path)
        mirror_path = f"{config.mirror_path}/providers"

        providers = []
        registry_path = os.path.join(mirror_path, config.registry)
        logger.info(f"Checking installed versions in {registry_path}")

        if not os.path.exists(registry_path):
            logger.info("No installed versions found.")
            return providers

        for namespace in os.listdir(registry_path):
            namespace_path = os.path.join(registry_path, namespace)
            logger.debug(f"Processing namespace: {namespace}")
            if not os.path.isdir(namespace_path):
                continue

            for provider_name in os.listdir(namespace_path):
                provider_path = os.path.join(namespace_path, provider_name)
                logger.debug(f"Processing provider: {namespace}/{provider_name}")
                if not os.path.isdir(provider_path):
                    continue

                versions = self.get_versions_from_index(provider_path)
                logger.debug(f"Found versions for {namespace}/{provider_name}: {versions}")
                provider = InstalledProvider(
                    namespace=namespace,
                    name=provider_name,
                    versions=versions
                )
                providers.append(provider)

        logger.debug(f"Installed providers: {providers}")
        return providers

    @staticmethod
    def get_versions_from_index(provider_path: str) -> List[VersionWithPlatform]:
        index_file_path = os.path.join(provider_path, "index.json")
        versions = []
        installed_versions = []

        if os.path.exists(index_file_path):
            with open(index_file_path, 'r') as f:
                index_data = json.load(f)
                versions = list(index_data.get("versions", {}).keys())
            logger.debug(f"Found versions in index: {versions}")

        for version in versions:
            version_file_path = os.path.join(provider_path, f"{version}.json")
            if os.path.exists(version_file_path):
                logger.debug(f"Found version file: {version_file_path}")
                with open(version_file_path, 'r') as f:
                    version_data = json.load(f)
                    for platform, platform_data in version_data.get("archives", {}).items():
                        logger.info(f"Version_data: {version} {platform}")
                        installed_versions.append(VersionWithPlatform(version=version, platform=platform))
                        logger.debug(f"Added version: {version} for platform: {platform}")
            else:
                logger.warning(f"Version file not found: {version_file_path}")

        logger.debug(f"Installed versions: {installed_versions}")
        return installed_versions
