from pydantic import BaseModel

class Spieler(BaseModel):
    id: int
    name: str
    x: int
    y: int
    z: int
    rotation: int

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

    def __repr__(self):
        return f"Block(typ={self.typ}, x={self.x}, y={self.y}, z={self.z})"


class Entity(BaseModel):
    typ: str
    id: str

    def __repr__(self):
            return f"Entity(typ={self.typ}, id={self.id}"


class Item(BaseModel):
    typ: str

    @staticmethod
    def von_api_format(s: str):
        return Item(typ=s)

    def __repr__(self):
        return f"Item(typ={self.typ})"


class InventarFeld(BaseModel):
    """ Ein Feld im Inventar eine:r Spieler:in """
    index: int
    item: Item
    anzahl: int

    @staticmethod
    def von_api_format(s: str):
        idx, itm, anz = s.split(":")

        itm = Item.von_api_format(itm)
        return InventarFeld(index=int(idx), item=itm, anzahl=int(anz))

    def __repr__(self):
        return f"InventarFeld(index={self.index}, item={repr(self.item)}, anzahl={self.anzahl})"


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
