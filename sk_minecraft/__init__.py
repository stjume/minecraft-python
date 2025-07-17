""" sk_minecraft package """
from pathlib import Path

from sk_minecraft.kern import verbinden
from sk_minecraft.main import *
try:
    from sk_minecraft.material import *
    from sk_minecraft.entity import *

except ModuleNotFoundError as e:
    raise RuntimeError(
        f"Es ist nicht möglich die auto-generierten Enums für Material und/oder Entity zu importieren."
        f"Bitte überprüfe, ob diese vorliegen, falls nicht siehe bitte ressourcen/generiere_enums.py im git repo."
    ) from e
