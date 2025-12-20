from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import ValidationError

from st_minecraft.core.core import ARG_SEPARATOR
from st_minecraft.core.core import InventoryFieldEmptyError
from st_minecraft.core.core import _bytes_to_text
from st_minecraft.core.core import _to_enum
from st_minecraft.entity import EntitySammlung
from st_minecraft.material import MaterialSammlung


class RichtungSammlung(Enum):
    """
    Ways in which speeds can be changed
    Used among others in set_player_velocity()
    """

    Hoch = "UP"
    Runter = "DOWN"
    Zurück = "BACK"
    Vorwärts = "LOOKING"


class Material(BaseModel):
    """
    Models a block in Minecraft that is located at a specific coordinate at the time of the query.
    """

    type: MaterialSammlung | None
    """ Block type """
    x: int | None = None
    y: int | None = None
    z: int | None = None

    def __repr__(self):
        return f"Block(type={self.type}, x={self.x}, y={self.y}, z={self.z})"

    @staticmethod
    def from_string(
        type: str, x: int | None = None, y: int | None = None, z: int | None = None
    ) -> Optional["Material"]:
        try:
            _type = _to_enum(MaterialSammlung, type)
        except ValidationError:
            _type = None
            print(f"Block '{type}' is not supported by the library. The type of the block is set to None.")

        return Material(type=_type, x=x, y=y, z=z)


class Player(BaseModel):
    """Snapshot at the time of the query, the data is NOT permanently updated!"""

    id: int
    """ Unique ID of the player """
    name: str
    """ Name of the player """
    x: int
    y: int
    z: int
    rotation: int
    """ Rotation of the player from -180 to 180 """
    looking_at: Material
    """ The next block the player is looking at (maximum 100 blocks away) """
    sneaked: bool
    """ True if player is sneaking """
    max_health: float
    health: float
    hunger: float
    saturation: float
    xp_level: float
    xp_progress: float

    @staticmethod
    def from_raw_data(data: bytes) -> "Player":
        """raw data is index, name, x, y, z"""
        (
            _id,
            name,
            x,
            y,
            z,
            rot,
            looking_at,
            sneaked,
            max_health,
            health,
            hunger,
            saturation,
            xp_level,
            xp_progress,
        ) = _bytes_to_text(data).split(ARG_SEPARATOR)
        return Player(
            id=int(_id),
            name=name,
            x=int(x),
            y=int(y),
            z=int(z),
            rotation=int(rot),
            looking_at=Material.from_string(looking_at),
            sneaked=sneaked.lower() == "true",
            max_health=float(max_health),
            hunger=float(hunger),
            saturation=float(saturation),
            xp_level=float(xp_level),
            xp_progress=float(xp_progress),
            health=float(health),
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
            f"health={self.health}, "
            f"max_health={self.max_health}, "
            f"hunger={self.hunger}, "
            f"saturation={self.saturation}, "
            f"xp_level={self.xp_level}, "
            f"xp_progress={self.xp_progress}, "
            f"sneaked={self.sneaked}, "
            f"looking_at={self.looking_at}, "
            ")"
        )


class Entity(BaseModel):
    """Models an entity. Many of the information can be empty (None)"""

    type: EntitySammlung
    """ Type of the entity """
    id: str | None = None
    """ Unique ID for this entity """
    name: str | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    health: float | None = None
    ai: bool | None = None

    def __repr__(self):
        return (
            f"Entity("
            f"type={self.type}, "
            f"name={self.name}, "
            f"x={self.x}, "
            f"y={self.y}, "
            f"z={self.z}, "
            f"health={self.health}, "
            f"ai={self.ai}, "
            f"id={self.id}"
            f")"
        )

    @staticmethod
    def from_string(type: str):
        # TODO: do we need this? if not we can remove the default Nones
        return Entity(type=_to_enum(EntitySammlung, type))

    @staticmethod
    def from_api_format(s: str):
        _id, type, name, x, y, z, health, ai = s.split(ARG_SEPARATOR)
        _type = _to_enum(EntitySammlung, type)
        return Entity(
            id=_id,
            type=_type,
            name=name if name != "null" else None,
            x=float(x),
            y=float(y),
            z=float(z),
            health=float(health),
            ai=ai == "true",
        )


class Item(BaseModel):
    """Models an item"""

    type: MaterialSammlung
    display_name: str | None

    @staticmethod
    def from_api_format(s: str):
        """we expect ; separated contents here"""
        type, display_name = s.split(";")
        if not display_name:
            display_name = None

        return Item(type=_to_enum(MaterialSammlung, type), display_name=display_name)

    def __repr__(self):
        return f"Item(type={self.type}, display_name={self.display_name})"


class InventoryField(BaseModel):
    """A field in a player's inventory"""

    index: int
    """ Index where the field is located in the inventory """
    item: Item
    """ Item object, which item is in the field """
    amount: int
    """ How many of the item are in this field """

    @staticmethod
    def from_api_format(s: str):
        idx, itm, amt = s.split(":")

        itm = Item.from_api_format(itm)
        return InventoryField(index=int(idx), item=itm, amount=int(amt))

    def __repr__(self):
        return f"InventarFeld(index={self.index}, item={self.item!r}, amount={self.amount})"


class Inventory(dict[int, InventoryField]):
    """
    Contains the entire inventory of a player.
    The structure is a dict.
    The dict maps from inventory index to an object of type InventarFeld, which contains the info about the element in the field.
    Note: Fields that are empty are not included in the dict!
    """

    def __contains__(self, item: Item):
        """Check if an item is in the inventory"""
        for _, v in self.items():
            if v.item == item:
                return True
        return False

    def __getitem__(self, item: int):
        try:
            return super().__getitem__(item)
        # I think this is the peak of the library. A non-generic wrapper around KeyError.
        except KeyError:
            raise InventoryFieldEmptyError(f"Field {item} is empty. Therefore you cannot access it here.")
