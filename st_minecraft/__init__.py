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


__version__ = "1.1.1"
version = VersionInfo(major=1, minor=1, micro=1, releaselevel="final", serial=0)

del NamedTuple, Literal
