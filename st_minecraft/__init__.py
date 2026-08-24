""" st_minecraft package """

__author__ = "Chris Geron, Adrian Oeyen & sk stiftung jugend und medien der Sparkasse KölnBonn"
__email__ = "git@chris-ge.de"

from typing import Literal
from typing import NamedTuple


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


__version__ = "1.2.0"
version = VersionInfo(major=1, minor=2, micro=0, releaselevel="final", serial=0)

del NamedTuple, Literal
