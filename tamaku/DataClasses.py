from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class VersionWithPlatform:
    def __init__(self, version: str, platform: str):
        self.version = version
        self.platform = platform

    @classmethod
    def from_dict(cls, data: Dict) -> 'VersionWithPlatform':
        return cls(
            version=data.get("version"),
            platform=data.get("platform")
        )

    def to_dict(self):
        return {
            "version": self.version,
            "platform": self.platform
        }

    def __eq__(self, other):
        if isinstance(other, VersionWithPlatform):
            return self.version == other.version and self.platform == other.platform
        return False

    def __hash__(self):
        return hash((self.version, self.platform))

    def __repr__(self):
        return f"VersionWithPlatform(version={self.version}, platform={self.platform})"


@dataclass
class Provider:
    namespace: str
    name: str
    minimal_version: Optional[str] = None
    versions: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Provider':
        return cls(
            namespace=data.get("namespace"),
            name=data.get("name"),
            versions=data.get("versions", [])
        )


@dataclass
class TaskProvider:
    namespace: str
    name: str
    minimal_version: Optional[str] = None
    versions: List[VersionWithPlatform] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict) -> 'TaskProvider':
        versions = [VersionWithPlatform.from_dict(vp) for vp in data.get("versions", [])]
        return cls(
            namespace=data.get("namespace"),
            name=data.get("name"),
            versions=versions
        )


@dataclass
class InstalledProvider:
    namespace: str
    name: str
    versions: List[VersionWithPlatform] = field(default_factory=list)


@dataclass
class Config:
    registry: str
    platforms: List[str] = field(default_factory=list)
    providers: List[Provider] = field(default_factory=list)
    mirror_path: Optional[str] = None
