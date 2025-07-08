from enum import Enum
from typing import Literal

from pydantic import BaseModel

class Spieler(BaseModel):
    id: int
    """ Eindeutige ID des Spielers """
    name: str
    """ Name des Spielers """
    x: int
    y: int
    z: int
    rotation: int
    """ Rotation des Spielers von -180 bis 180 """

    @staticmethod
    def von_rohdaten(data: bytes) -> "Spieler":
        """ rohdaten sind index, name, x, y, z """
        _id, name, x, y, z, rot = data.decode("utf-8").split(" ")
        return Spieler(id=int(_id), name=name, x=int(x), y=int(y), z=int(z), rotation=rot)

    def __repr__(self):
        return f"Spieler(id={self.id}, name={self.name}, x={self.x}, y={self.y}, z={self.z}, rotation={self.rotation})"


class Block(BaseModel):
    x: int
    y: int
    z: int
    typ: str
    """ Block Typ """

    def __repr__(self):
        return f"Block(typ={self.typ}, x={self.x}, y={self.y}, z={self.z})"


class Entity(BaseModel):
    """ Modelliert ein Entity """
    typ: str
    """ Typ des Entity's """
    id: str
    """ Einzigartige ID für dieses Entity """

    def __repr__(self):
            return f"Entity(typ={self.typ}, id={self.id}"


class Item(BaseModel):
    """ Modelliert ein Item """
    typ: str

    @staticmethod
    def von_api_format(s: str):
        return Item(typ=s)

    def __repr__(self):
        return f"Item(typ={self.typ})"


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


class KeineDatenFehler(Exception):
    """ Wird geworfen, wenn wir von der API nix empfangen """
    pass


class WertFehler(Exception):
    """ ValueError aber deutsch :clown face: """
    pass
