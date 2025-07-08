""" haupt funktionalitäten der bibliothek """

import socket

from sk_minecraft.kern import _sende_befehl, _empfangen, _bytes_zu_text, _leerzeichen_behandel
from sk_minecraft.daten_modelle import Spieler, Block, Entity, Inventar, Item, InventarFeld


def setze_block(x: int, y: int, z: int, block_typ: str) -> None:
    """
    Setzt einen Block im Minecraft-Spiel.

    Args:
        x (int): X-Koordinate
        y (int): Y-Koordinate
        z (int): Z-Koordinate
        block_typ (str): Typ des Blocks
    """
    # TODO: Das genaue Befehlsformat für das Protokoll festlegen
    befehl = f"setBlock {x} {y} {z} {block_typ}"
    _sende_befehl(befehl)


def hole_block(x: int, y: int, z: int):
    befehl = f"getBlock {x} {y} {z}"
    _sende_befehl(befehl)
    data = _empfangen()
    block = Block(x=x, y=y, z=z, typ=_bytes_zu_text(data))
    return block


def hole_spieler_koordinaten(index: int = 0) -> Spieler:
    """
    Gibt die Koordinaten des Spielers zurück.
    """
    befehl = f"getPlayerLoc {index}"
    _sende_befehl(befehl)
    print("befehl gesendet")
    data = _empfangen()
    spieler = Spieler.von_rohdaten(data)
    return spieler


def send_an_chat(nachricht: str):
    befehl = f"postChat {nachricht}"
    _sende_befehl(befehl)


def sende_befehl(befehl: str):
    """Führe einen Minecraft Command aus. Das / am Anfang eines Commands ist nicht notwendig."""
    if befehl.startswith("/"):
        print("Achtung: Du hast ein '/' am Anfang des Befehls eingegeben. Das ist vermutlich nicht notwendig!")
    befehl = f"chatCommand {befehl}"
    _sende_befehl(befehl)


def erzeuge_entity(x: int, y: int, z: int, entity: str) -> Entity:
    befehl = f"spawnEntity {x} {y} {z} {entity}"
    _sende_befehl(befehl)
    entity_id = _empfangen()
    entity = Entity(typ=entity, id=_bytes_zu_text(entity_id))
    return entity


def gebe_item(
        spieler: Spieler,
        item: Item | str,
        anzahl: int,
        name: str | None = None,
        feld: int | None = None,
        unzerstörbar: bool = False
):
    if isinstance(item, Item):
        item = item.typ

    befehl = f"addInv {spieler.id} {item} {anzahl}"

    if name is not None:
        befehl += f" name:{_leerzeichen_behandel(name)}"

    if feld is not None:
        befehl += f" slot:{feld}"

    if unzerstörbar:
        befehl += f" unbrekable"

    _sende_befehl(befehl)


def hole_inventar(spieler: Spieler):
    befehl = f"getInv {spieler.id}"
    _sende_befehl(befehl)
    data = _empfangen()

    # beispiel für (simple) empfangende daten:
    # (index,name;optional;infos:anzahl)
    # 0:LILY_OF_THE_VALLEY:1 4:STONE_PRESSURE_PLATE:1 25:DISPENSER:1 29:TARGET:1
    inventar_info = _bytes_zu_text(data)
    item_infos = inventar_info.split(" ")

    # baue inventar dict zusammen
    inventar = Inventar()
    for item in item_infos:
        feld = InventarFeld.von_api_format(item)
        inventar[feld.index] = feld

    return inventar
