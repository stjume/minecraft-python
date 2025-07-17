from enum import Enum
from typing import Optional

from pydantic import BaseModel, ValidationError

from sk_minecraft.entity import EntitySammlung
from sk_minecraft.material import MaterialSammlung
from sk_minecraft.kern import _zu_enum_umwandeln, _bytes_zu_text


class RichtungSammlung(Enum):
    """ wird genutzt um Geschwindigkeiten zu modifizieren """
    Hoch = "UP"
    Runter = "DOWN"
    Zurück = "BACK"
    Vorwärts = "LOOKING"


class Material(BaseModel):
    typ: MaterialSammlung | None
    """ Block Typ """
    x: int | None = None
    y: int | None = None
    z: int | None = None

    def __repr__(self):
        return f"Block(typ={self.typ}, x={self.x}, y={self.y}, z={self.z})"

    @staticmethod
    def von_string(typ: str, x: int | None = None, y: int | None = None, z: int | None = None) -> Optional["Material"]:
        try:
            _typ = _zu_enum_umwandeln(MaterialSammlung, typ)
        except ValidationError:
            _typ = None
            print(f"Block '{typ}' ist von der Library nicht unterstützt. Der typ des Blocks ist auf None gesetzt.")

        return Material(
            typ=_typ,
            x=x,
            y=y,
            z=z
        )


class Spieler(BaseModel):
    """ Momentaufnahme zum Zeitpunkt der Abfrage, die Daten werden NICHT dauerhaft geupdated """
    id: int
    """ Eindeutige ID des Spielers """
    name: str
    """ Name des Spielers """
    x: int
    y: int
    z: int
    rotation: int
    """ Rotation des Spielers von -180 bis 180 """
    schaut_auf: Material
    """ Der nächste Block auf den Spieler schaut (maximal 100 Blöcke weit entfernt) """
    sneaked: bool
    """ True wenn Player sneaked """
    max_leben: float
    leben: float
    hunger: float
    sättigung: float
    xp_level: float
    xp_fortschritt: float


    @staticmethod
    def von_rohdaten(data: bytes) -> "Spieler":
        """ rohdaten sind index, name, x, y, z """
        _id, name, x, y, z, rot, schaut_auf, sneaked, max_leben, leben, hunger, sättigung, xp_level, xp_progress = _bytes_zu_text(data).split(" ")
        return Spieler(
            id=int(_id),
            name=name,
            x=int(x),
            y=int(y),
            z=int(z),
            rotation=int(rot),
            schaut_auf=Material.von_string(schaut_auf),
            sneaked=sneaked.lower() == "true",
            max_leben=float(leben),
            hunger=float(hunger),
            sättigung=float(sättigung),
            xp_level=float(xp_level),
            xp_fortschritt=float(xp_level),
            leben=float(leben)
        )

    def __repr__(self):
        return (
            f"Spieler("
            f"id={self.id}, "
            f"name={self.name}, "
            f"x={self.x}, "
            f"y={self.y}, "
            f"z={self.z}, "
            f"rotation={self.rotation}, "
            f"leben={self.leben}"
            f"max_leben={self.max_leben}, "
            f"hunger={self.hunger}, "
            f"sättigung={self.sättigung}, "
            f"xp_level={self.xp_level}, "
            f"xp_fortschritt={self.xp_fortschritt}, "
            f"sneaked={self.sneaked}, "
            f"schaut_auf={self.schaut_auf}, "
            ")"
        )


class Entity(BaseModel):
    """ Modelliert ein Entity """
    typ: EntitySammlung
    """ Typ des Entity's """
    id: str | None
    """ Einzigartige ID für dieses Entity """
    name: str | None
    x: float | None
    y: float | None
    z: float | None
    leben: float | None
    ai: bool | None

    def __repr__(self):
            return (f"Entity("
                    f"typ={self.typ}, "
                    f"name={self.name}"
                    f"x={self.x}, "
                    f"y={self.y}, "
                    f"z={self.z}, "
                    f"leben={self.leben}, "
                    f"ai={self.ai}, "
                    f"id={self.id}"
                    f")")

    @staticmethod
    def von_string(typ: str):
        return Entity(typ=_zu_enum_umwandeln(EntitySammlung, typ))

    @staticmethod
    def von_api_format(s: str):
        _id, typ, name, x, y, z, leben, ai = s.split()
        _typ = _zu_enum_umwandeln(EntitySammlung, typ)
        return Entity(
            id=_id,
            typ=_typ,
            name=name if name != "null" else None,
            x=float(x),
            y=float(y),
            z=float(z),
            leben=float(leben),
            ai=ai == "true"
        )


class Item(BaseModel):
    """ Modelliert ein Item """
    typ: MaterialSammlung
    anzeige_name: str | None

    @staticmethod
    def von_api_format(s: str):
        """ wir erwarten hier ; getrennt inhalte"""
        typ, anzeige_name = s.split(";")
        if not anzeige_name:
            anzeige_name = None

        return Item(typ=_zu_enum_umwandeln(MaterialSammlung, typ), anzeige_name=anzeige_name)

    def __repr__(self):
        return f"Item(typ={self.typ}, anzeige_name={self.anzeige_name})"


class InventarFeld(BaseModel):
    """ Ein Feld im Inventar eine:r Spieler:in """
    index: int
    """ Index wo das Feld im Inventar liegt """
    item: Item
    """ Item Objekt, welches Item in dem Feld liegt """
    anzahl: int
    """ Wie viele von dem Item in diesem Feld liegen """

    @staticmethod
    def von_api_format(s: str):
        idx, itm, anz = s.split(":")

        itm = Item.von_api_format(itm)
        return InventarFeld(index=int(idx), item=itm, anzahl=int(anz))

    def __repr__(self):
        return f"InventarFeld(index={self.index}, item={self.item!r}, anzahl={self.anzahl})"


class Inventar(dict[int, InventarFeld]):
    """ Zeigt von index des inventars auf InventarFeld """
    def __contains__(self, item: Item):
        """ Überprüfe, ob ein Item im Inventar ist """
        for _, v in self.items():
            if v.item == item:
                return True
        return False
