"""
Generates the English and German Material / Entity enums for st_minecraft.

The single source of truth is the Bukkit API the backend actually runs against:
the `org.bukkit.Material` and `org.bukkit.entity.EntityType` enums shipped inside
the spigot-api jar. The backend validates blocks/entities via
`Material.getMaterial(NAME)` / `EntityType`, so generating our enums from the very
same jar guarantees the frontend never sees a name the backend cannot resolve
(the mismatch we hit before).

German display names are read from the vanilla `de_de.json` language file that
ships with the game client. Enum values (the Bukkit constant names) stay identical
across both languages, so `von_englisch` / `zu_englisch` bridge them by value.

Upgrading to a new Minecraft version:
    1. Point `SPIGOT_API_JAR` at the newer `spigot-api-<version>.jar`.
    2. Point `DE_DE_LANG` at the matching `de_de.json`
       (use `resolve_lang_file()` to pull it from a PrismLauncher instance).
    3. Run this script.

No Java runtime is required: enum constants are read straight from the compiled
`.class` files with a minimal bytecode parser.
"""

import json
import struct
import zipfile
from pathlib import Path

# --- Configuration: point these at the desired game version -------------------

SPIGOT_API_JAR = Path(
    "/Users/chris/copyparty/sk/minecraft-python-backend/bundler/libraries/spigot-api-1.21.5-R0.1-SNAPSHOT.jar"
)
DE_DE_LANG = Path(
    "/Users/chris/Library/Application Support/PrismLauncher/assets/objects/13/"
    "133a5aa6328318f8660b5d69942f1adfd942fab5"
)
OUTPUT_DIR = Path("../st_minecraft")

# --- Class-file constant extraction ------------------------------------------

_CONSTANT_TAG_SIZES = {
    7: 2,  # Class
    9: 4,  # Fieldref
    10: 4,  # Methodref
    11: 4,  # InterfaceMethodref
    8: 2,  # String
    3: 4,  # Integer
    4: 4,  # Float
    5: 8,  # Long   (takes two pool slots)
    6: 8,  # Double (takes two pool slots)
    12: 4,  # NameAndType
    15: 3,  # MethodHandle
    16: 2,  # MethodType
    17: 4,  # Dynamic
    18: 4,  # InvokeDynamic
    19: 2,  # Module
    20: 2,  # Package
}
_ACC_ENUM = 0x4000


def read_enum_constants(jar_path: Path, class_internal_name: str) -> list[str]:
    """Read the enum constant names of a class from a jar, in declaration order.

    Parses the compiled `.class` file directly (no JVM needed). Enum constants are
    the `static final` fields whose descriptor is the enum's own type and whose
    access flags carry ACC_ENUM.

    Args:
        jar_path: Path to the jar containing the class.
        class_internal_name: Internal name, e.g. "org/bukkit/Material".

    Returns:
        Enum constant names in the order they are declared in the class.
    """
    with zipfile.ZipFile(jar_path) as jar:
        data = jar.read(f"{class_internal_name}.class")

    pos = 8  # skip magic (4) + minor (2) + major (2)
    constant_count = struct.unpack_from(">H", data, pos)[0]
    pos += 2

    utf8: dict[int, str] = {}
    index = 1
    while index < constant_count:
        tag = data[pos]
        pos += 1
        if tag == 1:  # Utf8
            length = struct.unpack_from(">H", data, pos)[0]
            pos += 2
            utf8[index] = data[pos : pos + length].decode("utf-8")
            pos += length
        else:
            pos += _CONSTANT_TAG_SIZES[tag]
        # Long and Double occupy two constant-pool slots
        index += 2 if tag in (5, 6) else 1

    pos += 6  # skip access_flags (2) + this_class (2) + super_class (2)
    interfaces_count = struct.unpack_from(">H", data, pos)[0]
    pos += 2 + interfaces_count * 2

    descriptor = f"L{class_internal_name};"
    fields_count = struct.unpack_from(">H", data, pos)[0]
    pos += 2

    constants: list[str] = []
    for _ in range(fields_count):
        access_flags, name_index, descriptor_index, attr_count = struct.unpack_from(">HHHH", data, pos)
        pos += 8
        for _ in range(attr_count):
            attr_length = struct.unpack_from(">I", data, pos + 2)[0]
            pos += 6 + attr_length
        if access_flags & _ACC_ENUM and utf8.get(descriptor_index) == descriptor:
            constants.append(utf8[name_index])

    return constants


# --- German translation lookup -----------------------------------------------


def resolve_lang_file(prism_instance: Path, language: str = "de_de") -> Path:
    """Resolve a language file for a PrismLauncher instance via its asset index.

    Convenience helper for upgrades: given an instance directory (e.g. the folder
    named "1.21.5"), find the hashed language object in the shared asset store.

    Args:
        prism_instance: Path to the PrismLauncher instance directory.
        language: Language code, e.g. "de_de".

    Returns:
        Path to the resolved language JSON object.
    """
    prism_root = prism_instance.parent.parent
    pack = json.loads((prism_instance / "mmc-pack.json").read_text())
    mc_version = next(c["version"] for c in pack["components"] if c["uid"] == "net.minecraft")
    version_meta = json.loads((prism_root / "meta" / "net.minecraft" / f"{mc_version}.json").read_text())
    index_id = version_meta["assetIndex"]["id"]
    index = json.loads((prism_root / "assets" / "indexes" / f"{index_id}.json").read_text())
    obj_hash = index["objects"][f"minecraft/lang/{language}.json"]["hash"]
    return prism_root / "assets" / "objects" / obj_hash[:2] / obj_hash


def _load_translations(lang_file: Path) -> dict[str, str]:
    """Load the language JSON as a flat key -> translation mapping."""
    return json.loads(lang_file.read_text(encoding="utf-8"))


def _german_material(name: str, lang: dict[str, str]) -> str | None:
    """Look up the German name for a Bukkit Material constant.

    Tries the block and item translation keys, then a wall-variant fallback
    (e.g. white_wall_banner -> white_banner) which covers the only gaps.
    """
    key = name.lower()
    for candidate in (key, key.replace("_wall_", "_")):
        for prefix in ("block.minecraft.", "item.minecraft."):
            value = lang.get(f"{prefix}{candidate}")
            if value is not None:
                return value
    return None


def _german_entity(name: str, lang: dict[str, str]) -> str | None:
    """Look up the German name for a Bukkit EntityType constant."""
    return lang.get(f"entity.minecraft.{name.lower()}")


# --- Enum rendering ----------------------------------------------------------


def _title_case(constant: str) -> str:
    """Convert a Bukkit constant (ACACIA_BUTTON) to Title_Case (Acacia_Button)."""
    return "_".join(word.capitalize() for word in constant.split("_"))


def _sanitize_german(name: str) -> str:
    """Turn a German display name into a valid Python identifier.

    German values only ever contain spaces and hyphens as separators; umlauts
    and ß are valid identifier characters in Python 3, so they are kept.
    """
    return name.replace(" ", "_").replace("-", "_")


def _render_english_enum(class_name: str, header: str, constants: list[str]) -> str:
    """Render an English enum: Title_Case member = "BUKKIT_CONSTANT"."""
    lines = [header, "", "from enum import Enum", "", "", f"class {class_name}(Enum):"]
    for constant in constants:
        lines.append(f'    {_title_case(constant)} = "{constant}"')
    return "\n".join(lines) + "\n"


def _render_german_enum(body_header: str, translated: list[tuple[str, str]]) -> str:
    """Render a German enum body from (bukkit_constant, german_name) pairs.

    Collisions (two constants sharing one German name, e.g. banner / wall_banner)
    are disambiguated by suffixing the Bukkit constant, so every value keeps a
    reachable member.
    """
    lines = [body_header]
    used: set[str] = set()
    for constant, german in translated:
        member = _sanitize_german(german)
        if member in used:
            member = f"{member}__{constant}"
        used.add(member)
        lines.append(f'    {member} = "{constant}"')
    return "\n".join(lines) + "\n"


_EN_MATERIAL_HEADER = '"""This file is auto-generated! See ressourcen/generate_enums.py in the git repo! """'
_EN_ENTITY_HEADER = '""" This file is auto-generated! See ressourcen/generate_enums.py in the git repo! """'

_DE_MATERIAL_HEADER = '''"""Diese Datei ist auto-generiert! Siehe ressourcen/generate_enums.py im git repo! """

from enum import Enum
from typing import Optional

from st_minecraft.en.material import MaterialCollection as _Collection


class MaterialSammlung(Enum):

    @staticmethod
    def von_englisch(e: _Collection) -> Optional["MaterialSammlung"]:
        try:
            return MaterialSammlung._value2member_map_[e.value]
        except (KeyError, AttributeError):
            return None

    def zu_englisch(self) -> Optional[_Collection]:
        try:
            return _Collection._value2member_map_[self.value]
        except (KeyError, AttributeError):
            return None
'''

_DE_ENTITY_HEADER = '''"""Diese Datei ist auto-generiert! Siehe ressourcen/generate_enums.py im git repo! """

from enum import Enum
from typing import Optional

from st_minecraft.en.entity import EntityCollection as _Collection


class EntitySammlung(Enum):

    @staticmethod
    def von_englisch(e: _Collection) -> Optional["EntitySammlung"]:
        try:
            return EntitySammlung._value2member_map_[e.value]
        except KeyError:
            return None

    def zu_englisch(self) -> Optional[_Collection]:
        try:
            return _Collection._value2member_map_[self.value]
        except KeyError:
            return None
'''


def generate() -> None:
    """Generate all four enum files from the configured jar and language file."""
    lang = _load_translations(DE_DE_LANG)

    materials = [m for m in read_enum_constants(SPIGOT_API_JAR, "org/bukkit/Material") if not m.startswith("LEGACY_")]
    entities = [e for e in read_enum_constants(SPIGOT_API_JAR, "org/bukkit/entity/EntityType") if e != "UNKNOWN"]

    de_materials = [(m, _german_material(m, lang) or _title_case(m)) for m in materials]
    de_entities = [(e, _german_entity(e, lang) or _title_case(e)) for e in entities]

    (OUTPUT_DIR / "en" / "material.py").write_text(
        _render_english_enum("MaterialCollection", _EN_MATERIAL_HEADER, materials)
    )
    (OUTPUT_DIR / "en" / "entity.py").write_text(_render_english_enum("EntityCollection", _EN_ENTITY_HEADER, entities))
    (OUTPUT_DIR / "de" / "material.py").write_text(_render_german_enum(_DE_MATERIAL_HEADER, de_materials))
    (OUTPUT_DIR / "de" / "entity.py").write_text(_render_german_enum(_DE_ENTITY_HEADER, de_entities))

    print(f"Generated {len(materials)} materials and {len(entities)} entities.")


if __name__ == "__main__":
    generate()
