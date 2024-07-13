import os
import json
from typing import List, Dict, Optional
from tamaku.utils.Logger import Logger
from tamaku.DataClasses import InstalledProvider
from tamaku.tf.TfProviderConfigLoader import TfProviderConfigLoader
from tamaku.DataClasses import Config

logger = Logger()


class TfInstalledVersionsChecker:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.providers = []
        self.check_installed_versions(config_path)

    def check_installed_versions(self, config_path):
        loader = TfProviderConfigLoader()
        config = loader.load_config(config_path)
        mirror_path = f"{config.mirror_path}/providers"

        providers = []
        registry_path = os.path.join(mirror_path, config.registry)
        logger.info(f"Checking installed versions in {registry_path}")

        for namespace in os.listdir(registry_path):
            namespace_path = os.path.join(registry_path, namespace)
            if not os.path.isdir(namespace_path):
                continue

            for provider_name in os.listdir(namespace_path):
                provider_path = os.path.join(namespace_path, provider_name)
                if not os.path.isdir(provider_path):
                    continue

                versions = self.get_versions_from_index(provider_path)
                provider = InstalledProvider(
                    namespace=namespace,
                    name=provider_name,
                    versions=versions
                )
                providers.append(provider)

        self.providers = providers

    @staticmethod
    def get_versions_from_index(provider_path: str) -> List[str]:
        index_file_path = os.path.join(provider_path, "index.json")
        versions = []
        if os.path.exists(index_file_path):
            with open(index_file_path, 'r') as f:
                index_data = json.load(f)
                versions = list(index_data.get("versions", {}).keys())
        return versions
