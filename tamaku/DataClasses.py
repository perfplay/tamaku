from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class VersionWithPlatform:
    version: str
    platform: str

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
        return cls(
            namespace=data.get("namespace"),
            name=data.get("name"),
            versions=data.get("versions", [])
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
