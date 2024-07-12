import requests
from packaging import version
from tamaku.utils.Logger import Logger
from tamaku.BaseVersionFetcher import BaseVersionFetcher
from tamaku.utils.Utils import is_semantic_version

logger = Logger()


class TfProviderVersionFetcher(BaseVersionFetcher):
    def __init__(self, registry_url: str, namespace: str, name: str):
        super().__init__(registry_url, namespace, name)

    def fetch_versions(self):
        registry_url_with_path = f"{self.registry_url}/v1/providers/{self.namespace}/{self.name}/versions"
        try:
            response = requests.get(registry_url_with_path)
            response.raise_for_status()
            versions = response.json().get('versions', [])
            self.validate_versions(versions)

        except requests.RequestException as e:
            logger.error(f"Failed to fetch versions for {self.namespace}/{self.name}: {e}")
