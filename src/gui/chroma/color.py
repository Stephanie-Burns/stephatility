from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class Color:
    name                : str
    code                : str
    brighten            : List[str] = field(default_factory=list)
    darken              : List[str] = field(default_factory=list)
    desaturate          : List[str] = field(default_factory=list)
    hue                 : List[str] = field(default_factory=list)
    analogous           : List[str] = field(default_factory=list)
    monochromatic       : List[str] = field(default_factory=list)
    complementary       : List[str] = field(default_factory=list)
    split_complement    : List[str] = field(default_factory=list)
    triad               : List[str] = field(default_factory=list)
    tetrad              : List[str] = field(default_factory=list)
