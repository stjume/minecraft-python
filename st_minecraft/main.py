"""haupt funktionalitäten der bibliothek"""

from typing import Literal

from st_minecraft.core import ARG_SEPARATOR
from st_minecraft.core import WertFehler
from st_minecraft.core import _build_command
from st_minecraft.core import _bytes_to_text
from st_minecraft.core import _receive
from st_minecraft.core import _send_command
from st_minecraft.daten_modelle import Entity
from st_minecraft.daten_modelle import Inventar
from st_minecraft.daten_modelle import InventarFeld
from st_minecraft.daten_modelle import Item
from st_minecraft.daten_modelle import Material
from st_minecraft.daten_modelle import RichtungSammlung
from st_minecraft.daten_modelle import Spieler
from st_minecraft.entity import EntitySammlung
from st_minecraft.material import MaterialSammlung


def setze_block(x: int, y: int, z: int, block_typ: MaterialSammlung) -> None:
    """
    Setzt einen Block im Minecraft-Spiel.
    Du kannst damit auch bereits existierende Blöcke ersetzen.
    Wenn du einen Block "löschen" möchtest, kannst du ihn einfach mit MaterialSammlung.Luft ersetzen.
    Eine Übersicht aller Blöcke findest du hier:
    https://minecraft.fandom.com/wiki/Java_Edition_data_values#Blocks

    Args:
        x (int): X-Koordinate für den Block
        y (int): Y-Koordinate für den Block
        z (int): Z-Koordinate für den Block
        block_typ (MaterialSammlung): Block als Element aus der MaterialSammlung, z.B. MaterialSammlung.Melone
    """
    # TODO: Das genaue Befehlsformat für das Protokoll festlegen
    befehl = _build_command("setBlock", x, y, z, block_typ.value)
    _send_command(befehl)


def hole_block(x: int, y: int, z: int) -> Material:
    """
    Frag ab was für ein Block sich an der Koordinate befindet
    Du bekommst ein Block-Objekt zurück, dass unter .typ den typ enthält
    Hinweis: Ein "leerer" Block wird als Luft-Block behandelt.

    Args:
        x (int): X-Koordinate des Blocks
        y (int): Y-Koordinate des Blocks
        z (int): Z-Koordinate des Blocks
    Returns:
        Den Block an der Koordinate als Datentyp `Material`
    """
    befehl = _build_command("getBlock", x, y, z)
    _send_command(befehl)
    data = _receive()
    block = Material.von_string(x=x, y=y, z=z, typ=_bytes_to_text(data).upper())
    return block


def hole_entity(entity: Entity) -> Entity:
    """Bekomme den aktuellsten zustand eines bereits erstellten Entities
    Args:
        Das Entity Objekt von dem du ein Update abfragen möchtest
    Returns:
        Eine aktualisierte Version des entsprechenden Entities

    """
    befehl = _build_command("getEntity", entity.id)
    _send_command(befehl)
    data = _receive()
    entity = Entity.von_api_format(_bytes_to_text(data))
    return entity


def hole_spieler(index: int = 0) -> Spieler:
    """
    Frage den Zustand eines Spielers ab.
    Die Spieler sind durchnummeriert in der Reihenfolge in der sie dem Server beigetreten sind.
    Startend bei 0 für die erste Spieler:in
    Args:
        index: Index der abzufragenden Spieler:in ist optional (wenn du keinen Index angibst, wird Index 0 verwendet)
    Returns:
        Du bekommst ein Spieler Objekt zurück, welches eine Menge Infos über den Spieler enthält
    """
    befehl = _build_command("getPlayer", index)
    _send_command(befehl)
    data = _receive()
    spieler = Spieler.von_rohdaten(data)
    return spieler


def sende_an_chat(nachricht: str):
    """
    Sende eine Nachricht in den Ingame Chat.
    Du kannst auch besondere Formatierungen vornehmen, siehe diesen Wiki Eintrag:
    https://minecraft.fandom.com/de/wiki/Formatierungscodes
    Args:
        nachricht: Die Nachricht, die du versenden willst
    """
    befehl = _build_command("postChat", nachricht)
    _send_command(befehl)


def hole_chat():
    """
    Hole alle Nachrichten die seit der letzen Abfrage in den Chat geschrieben wurden.
    Returns:
        Du bekommst eine Liste aller gesendeten Nachrichten zurück
    """
    befehl = _build_command("pollChat")

    _send_command(befehl)
    data = _receive()

    nachrichten_str = _bytes_to_text(data)

    if nachrichten_str == "":
        return []

    nachrichten = nachrichten_str.split(ARG_SEPARATOR)
    return nachrichten


def sende_befehl(befehl: str):
    """
    Führe einen Minecraft Command aus, als würdest du ihn auf dem Server eingeben.
    Das / am Anfang eines Commands ist nicht notwendig.
    Args:
        befehl: Der Befehl als String ohne das Slash / am Anfang.
    """
    if befehl.startswith("/"):
        print("Achtung: Du hast ein '/' am Anfang des Befehls eingegeben. Das ist vermutlich nicht notwendig!")
    befehl = _build_command("chatCommand", befehl)
    _send_command(befehl)


def erzeuge_entity(x: int, y: int, z: int, entity: EntitySammlung) -> Entity:
    """
    Erzeuge eine entity an einer bestimmten Position
    Eine Liste aller Entities findest du hier:
    Auf Deutsch: https://minecraft.fandom.com/de/wiki/Objekt#ID-Namen
    Auf Englisch (dafür ausführlicher): https://minecraft.fandom.com/wiki/Java_Edition_data_values#Entities
    Args:
        x (int): X-Koordinate an der das Entity gespawnt werden soll
        y (int): Y-Koordinate an der das Entity gespawnt werden soll
        z (int): Z-Koordinate an der das Entity gespawnt werden soll
        entity: Ein Element aus der EntitySammlung z.B. EntitySammlung.Schaf

    Returns:
        Du bekommst ein Entity Objekt zurück. Mit diesem kannst du später wieder auf das Entity zugreifen.
    """
    befehl = _build_command("spawnEntity", x, y, z, entity.value)
    print(befehl)
    _send_command(befehl)
    data = _receive()
    entity = Entity.von_api_format(_bytes_to_text(data))
    return entity


def gebe_item(
    spieler: Spieler,
    item: MaterialSammlung,
    anzahl: int,
    name: str | None = None,
    inventar_feld: int | None = None,
    unzerstörbar: bool = False,
) -> Inventar:
    """
    Gebe einer Spieler:in ein Item
    Die verfügbaren Items befinden sich auch in der MaterialSammlung
    Eine Liste aller Items kannst du hier finden:
    https://minecraft.fandom.com/wiki/Java_Edition_data_values#Items (ist auf englisch)
    Args:
        spieler: Spieler:in die das item erhalten soll
        item: Item als Element der MaterialSammlung, z.B. MaterialSammlung.Diamantschwert
        anzahl: Wie viele davon sollen vergeben werden
        name: (optional) Wie soll das item heißen?
        inventar_feld: (optional) Feld in dem das item landen soll (als zahl)
        unzerstörbar: (optional) Wenn das item unzerstörbar sein soll auf True setzen, der standard ist zerstörbar

    Returns:
        Du bekommst Informationen über den Inventarzustand der Spielerin nach der Item-Vergabe zurück

    """
    if isinstance(item, Item):
        item = item.typ

    args = ["addInv", spieler.id, item.value, anzahl]

    if name is not None:
        args.append(f"name:{name}")

    if inventar_feld is not None:
        args.append(f"slot:{inventar_feld}")

    if unzerstörbar:
        args.append("unbreakable")

    befehl = _build_command(*args)
    _send_command(befehl)

    return hole_inventar(spieler)


def hole_inventar(spieler: Spieler) -> Inventar:
    """
    Rufe das Inventar eines Spielers ab.
    Args:
        spieler: Spieler von dem du das Inventar abfragen willst

    Returns:
        Du bekommst ein Inventar Object (wie ein dict) zurück"""
    befehl = _build_command("getInv", spieler.id)
    _send_command(befehl)
    data = _receive()

    # beispiel für (simple) empfangende daten:
    # (index,name;optional;infos:anzahl)
    # 0:LILY_OF_THE_VALLEY:1𝇉4:STONE_PRESSURE_PLATE:1𝇉25:DISPENSER:1𝇉29:TARGET:1
    inventar_info = _bytes_to_text(data)
    if not inventar_info:
        return Inventar()

    item_infos = inventar_info.split(ARG_SEPARATOR)

    # baue inventar dict zusammen
    inventar = Inventar()
    for item in item_infos:
        # leere strings abfangen
        if not item:
            continue
        feld = InventarFeld.von_api_format(item)
        inventar[feld.index] = feld

    return inventar


def spieler_position_setzen(spieler: Spieler, x: int, y: int, z: int, rotation: int = None) -> Spieler:
    """
    Verändere die position in x-, y-, z-Richtung und Rotation
    Args:
        spieler: Zu bearbeitender Spieler
        x: neue x-koordinate
        y: neue y-koordinate
        z: neue z-koordinate
        rotation: rotation: (optional) rotation des spielers (von -180 bis 180), wenn du sie nicht angibst, wird sie nicht verändert.

    Returns:
        Du bekommst eine aktualisierte Version des Spielers zurück (Zustand, nachdem er bewegt wurde)
    """
    args = ["setPlayerPos", spieler.id, x, y, z]
    if rotation is not None:
        if not -180 <= rotation <= 180:
            raise WertFehler(
                f"Die Rotation eines Spielers muss zwischen -180 und 180 sein. Du hast '{rotation}' gesagt."
            )

        args.append(f"rotation:{rotation}")

    befehl = _build_command(*args)
    _send_command(befehl)

    return hole_spieler(spieler.id)


def spieler_geschwindigkeit_setzen(spieler: Spieler, richtung: RichtungSammlung, wert: float) -> Spieler:
    """
    Verändere die Bewegungsgeschwindigkeit einer Spieler:in in verschiedene Richtungen.
    Alle Richtungen, die du beeinflussen kannst, findest du in der RichtungSammlung

    Args:
        spieler: Spieler Objekt, dass beeinflusst werden soll
        richtung: Richtung die verändert werden soll, als Element der RichtungSammlung, z.B. RichtungSammlung.Vorwärts
        wert: 1 ist normale geschwindigkeit, 0 ist einfrieren, die Zahl darf beliebig groß (und damit beliebig schnell) werden
    Returns:
        Du bekommst eine aktualisierte Version des Spielers zurück (Zustand, nachdem die Geschwindigkeit verändert wurde)

    """
    befehl = _build_command("setPlayerVelocity", richtung.value, spieler.id, wert)
    _send_command(befehl)
    return hole_spieler(spieler.id)


def spieler_max_leben_setzten(spieler: Spieler, wert: float) -> Spieler:
    """Setze die maximalen Leben einer Spielerin"""
    _setzt_spieler_eigenschaft("MAX_HEALTH", spieler, wert)
    return hole_spieler(spieler.id)


def spieler_leben_setzen(spieler: Spieler, wert: float) -> Spieler:
    """
    Setze die aktuellen Leben einer Spielerin
    Ist der Wert größer als das gesetzte Maximum werden alle überschüssigen Leben ignoriert
    Args:
        spieler: Spieler Objekt, dass beeinflusst werden soll
        wert: Anzahl an Leben als Kommazahl.
    Returns:
        Du bekommst eine aktualisierte Version des Spielers zurück (Zustand, nachdem die Leben verändert wurden)
    """
    _setzt_spieler_eigenschaft("HEALTH", spieler, wert)
    return hole_spieler(spieler.id)


def spieler_hunger_setzen(spieler: Spieler, wert: float, sättigung: float | None = None) -> Spieler:
    """
    Setze den Hunger eines Spielers.
    Du kannst optional auch noch die Sättigung setzen.

    Args:
        spieler: Spieler Objekt, dass beeinflusst werden soll
        wert: Anzahl an Hunger als Kommazahl.
        sättigung: (optional) Du kannst die Sättigung mit setzen. Lässt du sie leer, wird sie nicht verändert.
    Returns:
        Du bekommst eine aktualisierte Version des Spielers zurück (Zustand, nachdem der Hunger verändert wurde)
    """
    _setzt_spieler_eigenschaft("FOOD_LEVEL", spieler, wert)
    if sättigung is not None:
        _setzt_spieler_eigenschaft("SATURATION", spieler, sättigung)

    return hole_spieler(spieler.id)


def spieler_xp_level_setzen(spieler: Spieler, wert: float) -> Spieler:
    """
    Setze das aktuelle Level einer Spielerin

    Args:
        spieler: Spieler Objekt, dass beeinflusst werden soll
        wert: Level als Kommazahl
    Returns:
        Du bekommst eine aktualisierte Version des Spielers zurück (Zustand, nachdem das Level verändert wurde)
    """
    _setzt_spieler_eigenschaft("XP_LEVEL", spieler, wert)
    return hole_spieler(spieler.id)


def spieler_xp_fortschritt_setzen(spieler: Spieler, wert: float) -> Spieler:
    """
    Setze den Fortschritt innerhalb des Levels eines Spielers
    Args:
        spieler: Spieler Objekt, dass beeinflusst werden soll
        wert: Fortschritt als Kommazahl
    Returns:
        Du bekommst eine aktualisierte Version des Spielers zurück (Zustand, nachdem der Fortschritt verändert wurde)
    """
    _setzt_spieler_eigenschaft("XP_PROGRESS", spieler, wert)
    return hole_spieler(spieler.id)


def _setzt_spieler_eigenschaft(typ: str, spieler: Spieler, wert: float):
    """interne funktion für Leben, hunger und xp verändern"""
    befehl = _build_command("setPlayerStat", typ, spieler.id, wert)
    _send_command(befehl)


def entity_name_setzen(entity: Entity, name: str) -> Entity:
    """
    Setzen den Namen eines Entities
    Args:
        entity: Das zu bearbeitende Entity, nicht EntitySammlung!
        name: Der neue Name des Entities
    Returns:
        Eine aktualisierte Version des Entities (Zustand nach der Veränderung)
    """
    befehl = _build_command("editEntity", entity.id, f"name:{name}")
    _send_command(befehl)
    return hole_entity(entity)


def entity_position_setzen(entity: Entity, x: float, y: float, z: float) -> Entity:
    """
    Setzen die Position eines Entities

    Args:
        entity: Das zu bearbeitende Entity, nicht EntitySammlung!
        x (int): neue X-Koordinate
        y (int): neue Y-Koordinate
        z (int): neue Z-Koordinate
    Returns:
        Eine aktualisierte Version des Entities (Zustand nach der Veränderung)
    """
    befehl = _build_command("editEntity", entity.id, f"position:{x};{y};{z}")
    _send_command(befehl)
    return hole_entity(entity)


def entity_ai_setzen(entity: Entity, status: bool) -> Entity:
    """
    Setzen den AI eines Entities. Wenn es keine AI hat (False), bewegt es sich nicht.

    Args:
        entity: Das zu bearbeitende Entity, nicht EntitySammlung!
        status: True (wenn es sich bewegen soll), sonst False

    Returns:
        Eine aktualisierte Version des Entities (Zustand nach der Veränderung)
    """
    befehl = _build_command("editEntity", entity.id, f"ai:{status}")
    _send_command(befehl)
    return hole_entity(entity)


def entity_leben_setzen(entity: Entity, leben: float) -> Entity:
    """
    Setzen den Leben eines Entities. Wenn Leben auf 0 gesetzt werden, stirbt es.

    Args:
        entity: Das zu bearbeitende Entity, nicht EntitySammlung!
        leben: Wie viele Leben das Entity haben soll (0=tot).
    """
    befehl = _build_command("editEntity", entity.id, f"health:{leben}")
    _send_command(befehl)
    return hole_entity(entity)


def _validiere_id(id: str, type: Literal["MATERIAL", "ENTITY"]):
    """nur für interne nutzung"""
    befehl = _build_command("validate", type, id)
    _send_command(befehl)
    data = _receive()

    return _bytes_to_text(data)
