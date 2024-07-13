from packaging import version
from typing import List
from tamaku.utils.Logger import Logger

logger = Logger()


class VersionFilter:
    def __init__(self, versions: List[str], exclude: List[str] = None, include: List[str] = None, min_version: str = None):
        self.versions = [version.parse(ver) for ver in versions]
        self.exclude = [version.parse(ver) for ver in exclude] if exclude else []
        self.include = [version.parse(ver) for ver in include] if include else []
        self.min_version = version.parse(min_version) if min_version else None

    def filter_versions(self) -> List[str]:
        filtered_versions = []

        for ver in self.versions:
            if ver in self.exclude:
                continue
            if self.min_version and ver < self.min_version:
                continue
            filtered_versions.append(ver)

        for ver in self.include:
            if ver in self.versions and ver not in filtered_versions:
                filtered_versions.append(ver)
            elif ver not in self.versions:
                logger.warning(f"Included version not found in original list: {ver}")

        filtered_versions.sort()
        return [str(ver) for ver in filtered_versions]
