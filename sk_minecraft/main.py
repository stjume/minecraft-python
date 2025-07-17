""" haupt funktionalitäten der bibliothek """

import socket

from sk_minecraft.kern import _sende_befehl, _empfangen, _bytes_zu_text, _leerzeichen_behandel, _zu_enum_umwandeln
from sk_minecraft.daten_modelle import Spieler, Material, Entity, Inventar, Item, InventarFeld, WertFehler
from typing import Literal

def setze_block(x: int, y: int, z: int, block_typ: str) -> None:
    """
    Setzt einen Block im Minecraft-Spiel.

    Args:
        x (int): X-Koordinate
        y (int): Y-Koordinate
        z (int): Z-Koordinate
        block_typ (str): Typ des Blocks (resource location), siehe https://minecraft.fandom.com/wiki/Java_Edition_data_values#Blocks
    """
    # TODO: Das genaue Befehlsformat für das Protokoll festlegen
    befehl = f"setBlock {x} {y} {z} {block_typ}"
    _sende_befehl(befehl)


def hole_block(x: int, y: int, z: int) -> Material:
    """
    Frag ab was für ein Block sich an der Koordinate befindet
    Du bekommst ein Block-Objekt zurück, dass unter .typ den typ enthält
    """
    befehl = f"getBlock {x} {y} {z}"
    _sende_befehl(befehl)
    data = _empfangen()
    block = Material.von_string(x=x, y=y, z=z, typ=_bytes_zu_text(data).upper())
    return block


def hole_spieler_koordinaten(index: int = 0) -> Spieler:
    """
    Du bekommst ein Spieler Objekt zurück, welches x, y, z, rotation und name gibt
    Der index ist die Reihenfolge in der die Spieler dem Server beigetreten sind.
    Startend bei 0 für die erste Spielerin
    """
    befehl = f"getPlayer {index}"
    _sende_befehl(befehl)
    data = _empfangen()
    spieler = Spieler.von_rohdaten(data)
    return spieler


def sende_an_chat(nachricht: str):
    """ Sende eine Nachricht in den Chat """
    befehl = f"postChat {nachricht}"
    _sende_befehl(befehl)


def sende_befehl(befehl: str):
    """
    Führe einen Minecraft Command aus.
    Das / am Anfang eines Commands ist nicht notwendig.
    """
    if befehl.startswith("/"):
        print("Achtung: Du hast ein '/' am Anfang des Befehls eingegeben. Das ist vermutlich nicht notwendig!")
    befehl = f"chatCommand {befehl}"
    _sende_befehl(befehl)


def erzeuge_entity(x: int, y: int, z: int, entity: str) -> Entity:
    """
    erzeuge eine entity an einer bestimmten position
    Eine Liste aller Entities findest du hier:
    https://minecraft.fandom.com/wiki/Java_Edition_data_values#Entities
    entity ist der entity name (resource location)

    Du bekommst ein Entity Objekt zurück.
    In diesem befindet sich eine eindeutige id, um später wieder auf das entity zugreifen zu können.
    """
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
        inventar_feld: int | None = None,
        unzerstörbar: bool = False
):
    """
    Gebe einer Spieler:in ein Item
    Eine Liste aller Items kannst du hier finden:
    https://minecraft.fandom.com/wiki/Java_Edition_data_values#Items
    Args:
        spieler: Spieler:in die das item erhalten soll
        item: item name (resource location)
        anzahl: wie viele davon sollen vergeben werden
        name: (optional) wie soll das item heißen?
        inventar_feld: (optional) feld in dem das item landen soll (als zahl)
        unzerstörbar: (optional) wenn das item unzerstörbar sein soll auf True setzen, der standard ist zerstörbar

    """
    if isinstance(item, Item):
        item = item.typ

    befehl = f"addInv {spieler.id} {item} {anzahl}"

    if name is not None:
        befehl += f" name:{_leerzeichen_behandel(name)}"

    if inventar_feld is not None:
        befehl += f" slot:{inventar_feld}"

    if unzerstörbar:
        befehl += f" unbrekable"

    _sende_befehl(befehl)


def hole_inventar(spieler: Spieler) -> Inventar:
    """ Rufe das Inventar eines Spielers ab. Du bekommst ein Inventar Object (wie ein dict) zurück """
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


def spieler_position_setzen(spieler: Spieler, x: int, y: int, z: int, rotation: int = None):
    """
    Verändere die position in x, y, z richtung und rotation
    Args:
        spieler: Zu bearbeitender Spieler
        x: x-koordinate
        y: y-koordinate
        z: z-koordinate
        rotation: rotation: (optional) rotation des spielers

    Returns:

    """
    befehl = f"setPlayerPos {spieler.id} {x} {y} {z}"
    if rotation is not None:
        if not -180 <= rotation <= 180:
            raise WertFehler(f"Die Rotation eines Spielers muss zwischen -180 und 180 sein. Du hast '{rotation}' gesagt.")

        befehl += f" rotation:{rotation}"

    _sende_befehl(befehl)

def validiere_id(id: str, type: Literal["MATERIAL","ENTITY"]):
    befehl = f"validate {type} {id}"
    _sende_befehl(befehl)
    data = _empfangen()

    return _bytes_zu_text(data)
