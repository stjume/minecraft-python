""" st_minecraft package """

from st_minecraft.core import connect  # noqa: unused-import
from st_minecraft.main import *  # noqa: unused-import

try:
    from st_minecraft.entity import *  # noqa: unused-import
    from st_minecraft.material import *  # noqa: unused-import

except ModuleNotFoundError as e:
    raise RuntimeError(
        f"Es ist nicht möglich die auto-generierten Enums für Material und/oder Entity zu importieren."
        f"Bitte überprüfe, ob diese vorliegen, falls nicht siehe bitte ressourcen/generiere_enums.py im git repo."
    ) from e
