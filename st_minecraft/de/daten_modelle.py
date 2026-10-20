from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from st_minecraft.core.core import _coords_to_int
from st_minecraft.core.core import _to_enum
from st_minecraft.de._exceptions import InventarFeldLeerFehler
from st_minecraft.de._exceptions import NichtVergleichbarFehler
from st_minecraft.de.entity import EntitySammlung
from st_minecraft.de.material import MaterialSammlung
from st_minecraft.en import Dimension
from st_minecraft.en import DirectionCollection as _DirectionCollection
from st_minecraft.en import Entity as _EntityEN
from st_minecraft.en import Inventory as _InventoryEN
from st_minecraft.en import InventoryField as _InventoryFieldEN
from st_minecraft.en import Item as _ItemEN
from st_minecraft.en import Material as _MaterialEN
from st_minecraft.en import Message as _MessageEN
from st_minecraft.en import NotComparableException as _NotComparableExceptionEN
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

    @staticmethod
    def von_englisch(e: _DirectionCollection) -> "RichtungSammlung":
        return RichtungSammlung._value2member_map_[e.value]

    def zu_englisch(self) -> _DirectionCollection:
        return _DirectionCollection._value2member_map_[self.value]


class Material(BaseModel):
    """
    Modelliert einen Block in Minecraft, der sich zum Zeitpunkt der Abfrage an einer bestimmten Koordinate befindet.
    """

    typ: MaterialSammlung | None
    """ Block Typ """
    x: float | None = None
    y: float | None = None
    z: float | None = None
    dimension: Dimension | None = None

    @property
    def coords(self) -> tuple[float | None, float | None, float | None]:
        """Abkürzung um alle Koordinaten als Tuple zu bekommen (x, y, z)"""
        return self.x, self.y, self.z

    @property
    def coords_int(self) -> tuple[int, int, int]:
        """
        Abkürzung um alle Koordinaten als Tuple aus Ganzzahlen zu bekommen (x, y, z)

        Warnung: Die die Koordinaten werden gerundet, wie minecraft es intern tut (math.floor).
        Bedeutet, dass negative Zahlen aufgerundet werden und positive abgerundet.

        """
        return _coords_to_int(self.coords)

    def __repr__(self):
        return f"Block(typ={self.typ}, x={self.x}, y={self.y}, z={self.z}, dimension={self.dimension})"

    def __eq__(self, other):
        """
        Vergleiche diesen Block mit einem anderen Block oder einem Mitglied der MaterialSammlung.
        Der Vergleich selber passiert in der englischen Implementierung.
        """
        anderes = other.zu_englisch() if isinstance(other, (Material, MaterialSammlung)) else other

        return self.zu_englisch() == anderes

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def von_englisch(m: _MaterialEN | None) -> Optional["Material"]:
        if m is None:
            return None

        return Material(
            typ=MaterialSammlung.von_englisch(m.type) if m.type is not None else None,
            x=m.x,
            y=m.y,
            z=m.z,
            dimension=m.dimension,
        )

    def zu_englisch(self) -> _MaterialEN:
        return _MaterialEN(
            type=self.typ.zu_englisch() if self.typ is not None else None,
            x=self.x,
            y=self.y,
            z=self.z,
            dimension=self.dimension,
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
    dimension: Dimension | None = None
    leben: float | None = None
    ai: bool | None = None

    @property
    def coords(self) -> tuple[float | None, float | None, float | None]:
        """Abkürzung um alle Koordinaten als Tuple zu bekommen (x, y, z)"""
        return self.x, self.y, self.z

    @property
    def coords_int(self) -> tuple[int, int, int]:
        """
        Abkürzung um alle Koordinaten als Tuple aus Ganzzahlen zu bekommen (x, y, z)

        Warnung: Die die Koordinaten werden gerundet, wie minecraft es intern tut (math.floor).
        Bedeutet, dass negative Zahlen aufgerundet werden und positive abgerundet.
        """
        return _coords_to_int(self.coords)

    def __eq__(self, other):
        """
        Vergleiche dieses Entity mit einem anderen Entity oder einem Mitglied der EntitySammlung.
        Der Vergleich selber passiert in der englischen Implementierung.
        """
        anderes = other.zu_englisch() if isinstance(other, (Entity, EntitySammlung)) else other

        return self.zu_englisch() == anderes

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return (
            f"Entity("
            f"typ={self.typ}, "
            f"name={self.name}, "
            f"x={self.x}, "
            f"y={self.y}, "
            f"z={self.z}, "
            f"dimension={self.dimension}, "
            f"leben={self.leben}, "
            f"ai={self.ai}, "
            f"id={self.id}, "
            ")"
        )

    @staticmethod
    def von_string(typ: str):
        # TODO: brauchen wir das? falls nein können wir die default-Nones entfernen
        return Entity(typ=_to_enum(EntitySammlung, typ))

    @staticmethod
    def von_englisch(e: _EntityEN | None) -> Optional["Entity"]:
        if e is None:
            return None

        return Entity(
            typ=EntitySammlung.von_englisch(e.type),
            id=e.id,
            name=e.name,
            x=e.x,
            y=e.y,
            z=e.z,
            dimension=e.dimension,
            leben=e.health,
            ai=e.ai,
        )

    def zu_englisch(self) -> _EntityEN:
        return _EntityEN(
            type=self.typ.zu_englisch(),
            id=self.id,
            name=self.name,
            x=self.x,
            y=self.y,
            z=self.z,
            dimension=self.dimension,
            health=self.leben,
            ai=self.ai,
        )


class Spieler(BaseModel):
    """Momentaufnahme zum Zeitpunkt der Abfrage, die Daten werden NICHT dauerhaft aktualisiert!"""

    id: int
    """ Eindeutige ID des Spielers """
    name: str
    """ Name des Spielers """
    x: float
    y: float
    z: float
    dimension: Dimension
    rotation: int
    """ Rotation des Spielers von -180 bis 180 """
    schaut_auf_block: Material | None
    """ Der nächste Block auf den Spieler schaut (maximal 200 Blöcke weit entfernt) """
    schaut_auf_entity: Entity | None
    """ Das nächste Entity auf das Spieler schaut (maximal 200 Blöcke weit entfernt) """
    sneaked: bool
    """ True wenn Player sneaked """
    max_leben: float
    leben: float
    hunger: float
    sättigung: float
    xp_level: float
    xp_fortschritt: float
    """ Platz in der Hotbar (Schnellzugriffsleiste), der aktuell ausgewählt ist """
    hält_item: Optional["InventarFeld"]
    """ Item, das der Spieler aktuell in der Hand hält - None, wenn die Hand leer ist """

    @property
    def coords(self) -> tuple[float, float, float]:
        """Abkürzung um alle Koordinaten als Tuple zu bekommen (x, y, z)"""
        return self.x, self.y, self.z

    @property
    def coords_int(self) -> tuple[int, int, int]:
        """
        Abkürzung um alle Koordinaten als Tuple aus Ganzzahlen zu bekommen (x, y, z)

        Warnung: Die die Koordinaten werden gerundet, wie minecraft es intern tut (math.floor).
        Bedeutet, dass negative Zahlen aufgerundet werden und positive abgerundet.

        """
        return _coords_to_int(self.coords)

    @staticmethod
    def von_englisch(p: _PlayerEN):
        return Spieler(
            id=p.id,
            name=p.name,
            x=p.x,
            y=p.y,
            z=p.z,
            dimension=p.dimension,
            rotation=p.rotation,
            schaut_auf_block=Material.von_englisch(p.looking_at_block),
            schaut_auf_entity=Entity.von_englisch(p.looking_at_entity),
            sneaked=p.sneaked,
            max_leben=p.max_health,
            leben=p.health,
            hunger=p.hunger,
            sättigung=p.saturation,
            xp_level=p.xp_level,
            xp_fortschritt=p.xp_progress,
            hält_item=InventarFeld.von_englisch(p.holds_item),
        )

    def zu_englisch(self) -> _PlayerEN:
        return _PlayerEN(
            id=self.id,
            name=self.name,
            x=self.x,
            y=self.y,
            z=self.z,
            dimension=self.dimension,
            rotation=self.rotation,
            looking_at_block=self.schaut_auf_block.zu_englisch() if self.schaut_auf_block is not None else None,
            looking_at_entity=self.schaut_auf_entity.zu_englisch() if self.schaut_auf_entity is not None else None,
            sneaked=self.sneaked,
            max_health=self.max_leben,
            health=self.leben,
            hunger=self.hunger,
            saturation=self.sättigung,
            xp_level=self.xp_level,
            xp_progress=self.xp_fortschritt,
            holds_item=self.hält_item.zu_englisch() if self.hält_item is not None else None,
        )

    def __repr__(self):
        return (
            f"Spieler("
            f"id={self.id}, "
            f"name={self.name}, "
            f"x={self.x}, "
            f"y={self.y}, "
            f"z={self.z}, "
            f"dimension={self.dimension}, "
            f"rotation={self.rotation}, "
            f"leben={self.leben}, "
            f"max_leben={self.max_leben}, "
            f"hunger={self.hunger}, "
            f"sättigung={self.sättigung}, "
            f"xp_level={self.xp_level}, "
            f"xp_fortschritt={self.xp_fortschritt}, "
            f"sneaked={self.sneaked}, "
            f"schaut_auf_block=<{self.schaut_auf_block}>, "
            f"schaut_auf_entity=<{self.schaut_auf_entity}>, "
            f"hält_item=<{self.hält_item}>"
            ")"
        )


class Item(BaseModel):
    """Modelliert ein Item"""

    typ: MaterialSammlung
    anzeige_name: str | None

    def __repr__(self):
        return f"Item(typ={self.typ}, anzeige_name={self.anzeige_name})"

    def __eq__(self, other: object) -> bool:
        """
        Vergleiche dieses Item mit einem anderen Item oder einem Mitglied der MaterialSammlung.
        Gegen ein Item werden die Item-Felder (Typ und Anzeige-Name) verglichen,
        gegen ein Mitglied der MaterialSammlung nur der Typ.
        Der Vergleich selber passiert in der englischen Implementierung.
        """
        anderes = other.zu_englisch() if isinstance(other, (Item, MaterialSammlung)) else other

        try:
            return self.zu_englisch() == anderes
        except _NotComparableExceptionEN:
            raise NichtVergleichbarFehler(
                f"Der Typ '{type(other).__name__}' kann nicht mit dem Typ '{type(self).__name__}' verglichen werden"
            ) from None

    @staticmethod
    def von_englisch(i: _ItemEN):
        return Item(typ=MaterialSammlung.von_englisch(i.type), anzeige_name=i.display_name)

    def zu_englisch(self) -> _ItemEN:
        return _ItemEN(type=self.typ.zu_englisch(), display_name=self.anzeige_name)


class InventarFeld(Item):
    """Ein Feld im Inventar eine:r Spieler:in"""

    index: int
    """ Index wo das Feld im Inventar liegt """
    anzahl: int
    """ Wie viele von dem Item in diesem Feld liegen """

    def __repr__(self):
        return f"InventarFeld(index={self.index}, typ={self.typ}, item={self.anzeige_name!r}, anzahl={self.anzahl})"

    @staticmethod
    def von_englisch(i: _InventoryFieldEN):
        return InventarFeld(
            index=i.index, anzeige_name=i.display_name, typ=MaterialSammlung.von_englisch(i.type), anzahl=i.amount
        )

    def zu_englisch(self) -> _InventoryFieldEN:
        return _InventoryFieldEN(
            index=self.index,
            display_name=self.anzeige_name,
            type=MaterialSammlung.zu_englisch(self.typ),
            amount=self.anzahl,
        )

    # __eq__ is handled by Item and it's translation layer eq method


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
            if v == item:
                return True
        return False

    def __getitem__(self, item: int) -> InventarFeld:
        try:
            return super().__getitem__(item)
        # ich glaube, hier ist der peak der library. ein nicht-generischer wrapper um den KeyError.
        except KeyError:
            raise InventarFeldLeerFehler(f"Das Feld {item} ist leer. Daher kannst du hier nicht drauf zugreifen.")

    @staticmethod
    def von_englisch(i: _InventoryEN):
        return Inventar({index: InventarFeld.von_englisch(field) for index, field in i.items()})

    def zu_englisch(self) -> _InventoryEN:
        return _InventoryEN({index: field.zu_englisch() for index, field in self.items()})


class Nachricht(BaseModel):
    """
    Repräsentiert eine Nachricht, die vom Nutzer an den Chat gesendet wurde
    """

    text: str
    """Der in den Chat gesendete Text"""
    absender_name: str
    """Name des Spielers, der diese Nachricht gesendet hat"""
    absender_id: int
    """ID des spielers, der die Nachricht gesendet hat"""
    versandzeit: datetime

    def __eq__(self, other):
        """
        Vergleiche diese Nachricht mit einer anderen Nachricht oder einem String.
        Der Vergleich selber passiert in der englischen Implementierung.
        """
        anderes = other.zu_englisch() if isinstance(other, Nachricht) else other

        return self.zu_englisch() == anderes

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def von_englisch(m: _MessageEN):
        return Nachricht(
            text=m.text, absender_name=m.sender_name, absender_id=m.sender_id, versandzeit=m.time_when_sent
        )

    def zu_englisch(self) -> _MessageEN:
        return _MessageEN(
            text=self.text, sender_name=self.absender_name, sender_id=self.absender_id, time_when_sent=self.versandzeit
        )
