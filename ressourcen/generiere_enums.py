"""
Dieses Modul generiert die Enums für Material und Entity aus einer CSV
Damit sie wie gewünscht funktioniert, sollte sie aus dem Verzeichnis, in dem sie gerade liegt ausgeführt werden
"""

from pathlib import Path


def baue_material_enum(
        block_quelldatei: Path = Path("blocks_items_validated.csv"),
        ziel_datei: Path = Path("../sk_minecraft/material.py")
):
    """
    Auto generiert ein Enum für alle Blöcke in einer .csv datei
    Die datei muss enthalten: GewünschterName,minecraft_name
    Args:
        block_quelldatei:
        ziel_datei:
    """

    code = """''' Diese Datei ist auto-generiert! Siehe ressourcen/generiere_enums.py im git repo! '''

from enum import Enum


class MaterialSammlung(Enum):
"""
    _schreibe_enum(code, block_quelldatei, ziel_datei)


def baue_entity_enum(
        entity_quelldatei: Path = Path("entities_validated.csv"),
        ziel_datei: Path = Path("../sk_minecraft/entity.py")
):
    """ analog zu baue_block_enum() aber für Entities """
    code = """''' Diese Datei ist auto-generiert! Siehe ressourcen/generiere_enums.py im git repo! '''

from enum import Enum


class EntitySammlung(Enum):
"""
    _schreibe_enum(code, entity_quelldatei, ziel_datei)


def _schreibe_enum(enum_quellcode: str, block_quelldatei: Path, ziel_datei: Path):
    """
    füllt den körper des enums durch simples anhängen neuer zeilen
    enum hat dann den stil NameDesBlocks = "MINECRAFT_ID_ALL_CAPS"
    """
    zeilen = block_quelldatei.read_text().split("\n")
    bereits_gesehene_namen = set()
    for line in zeilen:
        if line == "":
            continue

        deutscher_name, _id = line.split(",")

        if deutscher_name in bereits_gesehene_namen:
            continue

        enum_quellcode += f'    {deutscher_name} = "{_id.upper()}"\n'
        bereits_gesehene_namen.add(deutscher_name)

    ziel_datei.write_text(enum_quellcode)

if __name__ == '__main__':
    baue_material_enum()
    baue_entity_enum()
