"""
This module generates the Enums for Material and Entity from a CSV
For it to work as intended, it should be executed from the directory in which it currently resides
"""

from pathlib import Path


def build_german_material_enum(
    block_source_file: Path = Path("blocks_items_validated.csv"),
    target_file: Path = Path("../st_minecraft/de/material.py"),
):
    """
    Auto-generates an Enum for all blocks in a .csv file
    The file must contain: DesiredName,minecraft_name
    Args:
        block_source_file: Path to the CSV file containing block data
        target_file: Path where the generated enum file should be written
    """

    code = """''' Diese Datei ist auto-generiert! Siehe ressourcen/generate_enums.py im git repo! '''

from enum import Enum
from st_minecraft.en.material import MaterialCollection as _Collection


class MaterialSammlung(Enum):

    @staticmethod
    def von_englisch(e: _Collection) -> "MaterialSammlung":
        return MaterialSammlung._value2member_map_[e.value]

    def zu_englisch(self) -> _Collection:
        return _Collection._value2member_map_[self.value]
"""
    _write_german_enum(code, block_source_file, target_file)


def build_material_enum_english(
    block_source_file: Path = Path("blocks_items_validated.csv"),
    target_file: Path = Path("../st_minecraft/en/material.py"),
):
    """
    Auto-generates an English Enum for all blocks in a .csv file
    The file must contain: DesiredName,minecraft_name
    Args:
        block_source_file: Path to the CSV file containing block data
        target_file: Path where the generated enum file should be written
    """

    code = """''' This file is auto-generated! See ressourcen/generate_enums.py in the git repo! '''

from enum import Enum


class MaterialCollection(Enum):
"""
    _write_enum_english(code, block_source_file, target_file)


def build_german_entity_enum(
    entity_source_file: Path = Path("entities_validated.csv"),
    target_file: Path = Path("../st_minecraft/de/entity.py"),
):
    """Analogous to build_material_enum() but for Entities"""
    code = """''' Diese Datei ist auto-generiert! Siehe ressourcen/generate_enums.py im git repo! '''

from enum import Enum
from st_minecraft.en.entity import EntityCollection as _Collection


class EntitySammlung(Enum):
    @staticmethod
    def von_englisch(e: _Collection) -> "EntitySammlung":
        return EntitySammlung._value2member_map_[e.value]

    def zu_englisch(self) -> _Collection:
        return EntitySammlung._value2member_map_[self.value]
"""
    _write_german_enum(code, entity_source_file, target_file)


def build_entity_enum_english(
    entity_source_file: Path = Path("entities_validated.csv"),
    target_file: Path = Path("../st_minecraft/en/entity.py"),
):
    """Analogous to build_material_enum_english() but for Entities"""
    code = """''' This file is auto-generated! See ressourcen/generate_enums.py in the git repo! '''

from enum import Enum


class EntityCollection(Enum):
"""
    _write_enum_english(code, entity_source_file, target_file)


def _write_german_enum(enum_source_code: str, source_file: Path, target_file: Path):
    """
    Fills the body of the enum by simply appending new lines
    Enum then has the style BlockName = "MINECRAFT_ID_ALL_CAPS"
    """
    lines = source_file.read_text().split("\n")
    already_seen_names = set()
    for line in lines:
        if line == "":
            continue

        name, _id = line.split(",")

        if name in already_seen_names:
            continue

        enum_source_code += f'    {name} = "{_id.upper()}"\n'
        already_seen_names.add(name)

    target_file.write_text(enum_source_code)


def _snake_to_title_case(snake_str: str) -> str:
    """Convert snake_case to Title_Case"""
    return "_".join(word.capitalize() for word in snake_str.split("_"))


def _write_enum_english(enum_source_code: str, source_file: Path, target_file: Path):
    """
    Fills the body of the enum with English names in Title_Case format
    Enum then has the style EnglishName = "English_Name"
    """
    lines = source_file.read_text().split("\n")
    already_seen_names = set()
    for line in lines:
        if line == "":
            continue

        _, minecraft_id = line.split(",")
        english_name = _snake_to_title_case(minecraft_id)

        if english_name in already_seen_names:
            continue

        enum_source_code += f'    {english_name} = "{minecraft_id.upper()}"\n'
        already_seen_names.add(english_name)

    target_file.write_text(enum_source_code)


if __name__ == "__main__":
    build_german_material_enum()
    build_german_entity_enum()
    build_material_enum_english()
    build_entity_enum_english()
