from st_minecraft.core import connect as verbinden  # noqa: unused-import
from st_minecraft.de.boss_leiste import *  # noqa: unused-import
from st_minecraft.de.daten_modelle import *  # noqa: unused-import
from st_minecraft.de.main import *  # noqa: unused-import

try:
    from st_minecraft.de.entity import *  # noqa: unused-import
    from st_minecraft.de.material import *  # noqa: unused-import

except ModuleNotFoundError as e:
    raise RuntimeError(
        f"Es ist nicht möglich die auto-generierten Enums für Material und/oder Entity zu importieren."
        f"Bitte überprüfe, ob diese vorliegen, falls nicht siehe bitte ressourcen/generate_enums.py im git repo."
    ) from e
