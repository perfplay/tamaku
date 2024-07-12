from abc import ABC, abstractmethod
from typing import List

from tamaku.utils.Logger import Logger
from packaging import version
from tamaku.utils.Utils import is_semantic_version
from packaging.version import Version

logger = Logger()


class BaseVersionFetcher(ABC):
    def __init__(self, registry_url: str, namespace: str, name: str):
        self.registry_url = registry_url
        self.namespace = namespace
        self.name = name
        self._current_versions = []
        self._current_versions_str = []

    @abstractmethod
    def fetch_versions(self):
        pass

    @property
    def current_versions(self) -> List[Version]:
        return self._current_versions

    @property
    def current_versions_str(self) -> List[str]:
        return self._current_versions_str

    def validate_versions(self, versions: List[dict]):
        current_versions = []
        current_versions_str = []
        for ver in versions:
            try:
                parsed_version = version.parse(ver['version'])
                if not is_semantic_version(ver['version']):
                    logger.warning(f"Non-semantic version, filtered: {ver['version']}")
                    continue
                current_versions.append(parsed_version)
                current_versions_str.append(ver['version'])
            except version.InvalidVersion as e:
                logger.error(f"Invalid version: {ver['version']} - {e}")
                continue

        self._current_versions = sorted(current_versions)
        self._current_versions_str = sorted(current_versions_str)

        logger.info(f"Fetched versions for {self.namespace}/{self.name}: {current_versions_str}")
