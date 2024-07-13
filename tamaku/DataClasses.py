from dataclasses import dataclass, field
from typing import List, Optional, Dict


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
class InstalledVersion:
    version: str
    platform: str


@dataclass
class InstalledProvider:
    namespace: str
    name: str
    versions: List[InstalledVersion] = field(default_factory=list)


@dataclass
class Config:
    registry: str
    platforms: List[str] = field(default_factory=list)
    providers: List[Provider] = field(default_factory=list)
    mirror_path: Optional[str] = None
