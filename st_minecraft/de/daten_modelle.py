from enum import Enum
from typing import Optional

from pydantic import BaseModel

from st_minecraft.core.core import InventoryFieldEmptyError
from st_minecraft.core.core import _to_enum
from st_minecraft.de.entity import EntitySammlung
from st_minecraft.de.material import MaterialSammlung
from st_minecraft.en import Entity as _EntityEN
from st_minecraft.en import Inventory as _InventoryEN
from st_minecraft.en import InventoryField as _InventoryFieldEN
from st_minecraft.en import Item as _ItemEN
from st_minecraft.en import Material as _MaterialEN
from st_minecraft.en import Player as _PlayerEN


class RichtungSammlung(Enum):
    """
    Arten, wie Geschwindigkeiten verändert werden können
    Wird u.A. in spieler_geschwindigkeit_setzen() verwendet.
    """

    Hoch = "UP"
    Runter = "DOWN"
    Zurück = "BACK"
    Vorwärts = "LOOKING"


class Material(BaseModel):
    """
    Modelliert einen Block in Minecraft, der sich zum Zeitpunkt der Abfrage an einer bestimmten Koordinate befindet.
    """

    typ: MaterialSammlung | None
    """ Block Typ """
    x: int | None = None
    y: int | None = None
    z: int | None = None

    def __repr__(self):
        return f"Block(typ={self.typ}, x={self.x}, y={self.y}, z={self.z})"

    @staticmethod
    def von_englisch(m: _MaterialEN | None) -> Optional["Material"]:
        if m is None:
            return None

        return Material(typ=MaterialSammlung.von_englisch(m.type), x=m.x, y=m.y, z=m.z)

    def zu_englisch(self) -> _MaterialEN:
        return _MaterialEN(type=self.typ.zu_englisch(), x=self.x, y=self.y, z=self.z)


class Spieler(BaseModel):
    """Momentaufnahme zum Zeitpunkt der Abfrage, die Daten werden NICHT dauerhaft aktualisiert!"""

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
    def von_englisch(p: _PlayerEN):
        return Spieler(
            id=p.id,
            name=p.name,
            x=p.x,
            y=p.y,
            z=p.z,
            rotation=p.rotation,
            schaut_auf=Material.von_englisch(p.looking_at),
            sneaked=p.sneaked,
            max_leben=p.max_health,
            leben=p.health,
            hunger=p.hunger,
            sättigung=p.saturation,
            xp_level=p.xp_level,
            xp_fortschritt=p.xp_progress,
        )

    def zu_englisch(self) -> _PlayerEN:
        return _PlayerEN(
            id=self.id,
            name=self.name,
            x=self.x,
            y=self.y,
            z=self.z,
            rotation=self.rotation,
            looking_at=self.schaut_auf.zu_englisch(),
            sneaked=self.sneaked,
            max_health=self.max_leben,
            health=self.leben,
            hunger=self.hunger,
            saturation=self.sättigung,
            xp_level=self.xp_level,
            xp_progress=self.xp_fortschritt,
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
    """Modelliert ein Entity. Viele der Informationen können leer (None) sein"""

    typ: EntitySammlung
    """ Typ des Entity's """
    id: str | None = None
    """ Einzigartige ID für dieses Entity """
    name: str | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    leben: float | None = None
    ai: bool | None = None

    def __repr__(self):
        return (
            f"Entity("
            f"typ={self.typ}, "
            f"name={self.name}"
            f"x={self.x}, "
            f"y={self.y}, "
            f"z={self.z}, "
            f"leben={self.leben}, "
            f"ai={self.ai}, "
            f"id={self.id}"
            f")"
        )

    @staticmethod
    def von_string(typ: str):
        # TODO: brauchen wir das? falls nein können wir die default-Nones entfernen
        return Entity(typ=_to_enum(EntitySammlung, typ))

    @staticmethod
    def von_englisch(e: _EntityEN):
        return Entity(
            typ=EntitySammlung.von_englisch(e.type), id=e.id, name=e.name, x=e.x, y=e.y, z=e.z, leben=e.health, ai=e.ai
        )

    def zu_englisch(self) -> _EntityEN:
        return _EntityEN(
            type=self.typ.zu_englisch(),
            id=self.id,
            name=self.name,
            x=self.x,
            y=self.y,
            z=self.z,
            health=self.leben,
            ai=self.ai,
        )


class Item(BaseModel):
    """Modelliert ein Item"""

    typ: MaterialSammlung
    anzeige_name: str | None

    def __repr__(self):
        return f"Item(typ={self.typ}, anzeige_name={self.anzeige_name})"

    @staticmethod
    def von_englisch(i: _ItemEN):
        return Item(typ=MaterialSammlung.von_englisch(i.type), anzeige_name=i.display_name)


class InventarFeld(BaseModel):
    """Ein Feld im Inventar eine:r Spieler:in"""

    index: int
    """ Index wo das Feld im Inventar liegt """
    item: Item
    """ Item Objekt, welches Item in dem Feld liegt """
    anzahl: int
    """ Wie viele von dem Item in diesem Feld liegen """

    def __repr__(self):
        return f"InventarFeld(index={self.index}, item={self.item!r}, anzahl={self.anzahl})"

    @staticmethod
    def von_englisch(i: _InventoryFieldEN):
        return InventarFeld(index=i.index, item=Item.von_englisch(i.item), anzahl=i.amount)

    def zu_englisch(self) -> _InventoryFieldEN:
        return _InventoryFieldEN(index=self.index, item=self.item.zu_englisch(), amount=self.anzahl)


class Inventar(dict[int, InventarFeld]):
    """
    Enthält das gesamte Inventar eines Spielers.
    Die Struktur ist ein dict.
    Das dict zeigt von Index des Inventars auf ein Objekt vom Typ InventarFeld, welcher die Infos über das Element in dem Feld enthält.
    Hinweis: Felder, die Leer sind, sind nicht in dem dict enthalten!
    """

    def __contains__(self, item: Item):
        """Überprüfe, ob ein Item im Inventar ist"""
        for _, v in self.items():
            if v.item == item:
                return True
        return False

    def __getitem__(self, item: int):
        try:
            super().__getitem__(item)
        # ich glaube, hier ist der peak der library. ein nicht-generischer wrapper um den KeyError.
        except KeyError:
            raise InventoryFieldEmptyError(f"Das Feld {item} ist leer. Daher kannst du hier nicht drauf zugreifen.")

    @staticmethod
    def von_englisch(i: _InventoryEN):
        return Inventar({index: InventarFeld.von_englisch(field) for index, field in i.items()})

    def zu_englisch(self) -> _InventoryEN:
        return _InventoryEN({index: field.zu_englisch() for index, field in self.items()})
