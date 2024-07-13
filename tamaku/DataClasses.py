from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Provider:
    namespace: str
    name: str
    minimal_version: Optional[str] = None
    versions: List[str] = field(default_factory=list)

@dataclass
class Config:
    registry: str
    platforms: List[str] = field(default_factory=list)
    providers: List[Provider] = field(default_factory=list)