from st_minecraft.core import connect  # noqa: unused-import
from st_minecraft.en.boss_bar import *  # noqa: unused-import
from st_minecraft.en.data_models import *  # noqa: unused-import
from st_minecraft.en.main import *  # noqa: unused-import

try:
    from st_minecraft.en.entity import *  # noqa: unused-import
    from st_minecraft.en.material import *  # noqa: unused-import

except ModuleNotFoundError as e:
    raise RuntimeError(
        f"It is not possible to import the auto-generated Enums for Material and/or Entity."
        f"Please check if these exist; if not, see resources/generate_enums.py in the git repo."
    ) from e
