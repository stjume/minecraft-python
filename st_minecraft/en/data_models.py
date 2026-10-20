from datetime import datetime
from enum import Enum
from typing import Literal
from typing import Optional

from pydantic import BaseModel
from pydantic import ValidationError

from st_minecraft.core import ARG_SEPARATOR_SECOND_LEVEL
from st_minecraft.core import InventoryFieldEmptyError
from st_minecraft.core.core import ARG_SEPARATOR
from st_minecraft.core.core import _bytes_to_text
from st_minecraft.core.core import _coords_to_int
from st_minecraft.core.core import _to_enum
from st_minecraft.en.entity import EntityCollection
from st_minecraft.en.material import MaterialCollection

dimensionT = Literal["world", "world_nether", "world_the_end"]


def _to_float(f: str) -> float:
    """
    handler that can handle dot- and comma-separated strings
    why? - because paper-mc returns comma-separated coordinates :D
    """
    if "," in f:
        f = f.replace(",", ".")

    if not f:
        return 0.0

    return float(f)


class Dimension(Enum):
    World = "world"
    Nether = "world_nether"
    End = "world_the_end"


class DirectionCollection(Enum):
    """
    Ways in which speeds can be changed
    Used among others in set_player_velocity()
    """

    Up = "UP"
    Down = "DOWN"
    Back = "BACK"
    Forward = "LOOKING"


class Material(BaseModel):
    """
    Models a block in Minecraft that is located at a specific coordinate at the time of the query.
    """

    type: MaterialCollection | None
    """ Block type """
    x: float | None = None
    y: float | None = None
    z: float | None = None
    dimension: Dimension | None = None

    @property
    def coords(self) -> tuple[float | None, float | None, float | None]:
        """Shorthand to get all coords as tuple (x, y, z)"""
        return self.x, self.y, self.z

    @property
    def coords_int(self) -> tuple[int, int, int]:
        """
        Shorthand to get all coords as tuple (x, y, z) as integers

        warning: coordinates are rounded like Minecraft does it internally.
        this means that negative numbers are rounded up and positives are rounded down

        """
        return _coords_to_int(self.coords)

    def __repr__(self):
        return f"Block(type={self.type}, x={self.x}, y={self.y}, z={self.z}, dimension={self.dimension})"

    def __eq__(self, other):
        # einfachen vergleich mit typ erlauben
        if isinstance(other, MaterialCollection):
            return self.type == other

        if not isinstance(other, type(self)):
            return False

        return self.type == other.type and self.coords_int == other.coords_int and self.dimension == other.dimension

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def from_api_format(s: str):
        _type, x, y, z, dim = s.split(":")

        _type_enum = Material._validate_material(_type)

        return Material(type=_type_enum, x=int(x), y=int(y), z=int(z), dimension=_to_enum(Dimension, dim))

    @staticmethod
    def from_string(
        type: str,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
        dimension: str | None = None,
    ) -> Optional["Material"]:

        _type_enum = Material._validate_material(type)
        return Material(type=_type_enum, x=x, y=y, z=z, dimension=_to_enum(Dimension, dimension))

    @staticmethod
    def _validate_material(m: str):
        try:
            _type = _to_enum(MaterialCollection, m)
        except ValidationError:
            _type = None
            print(f"Block '{m}' is not supported by the library. The type of the block is set to None.")
        return _type


class Entity(BaseModel):
    """Models an entity. Many of the information can be empty (None)"""

    type: EntityCollection
    """ Type of the entity """
    id: str | None = None
    """ Unique ID for this entity """
    name: str | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    dimension: Dimension | None = None
    health: float | None = None
    ai: bool | None = None

    @property
    def coords(self) -> tuple[float | None, float | None, float | None]:
        """Shorthand to get all coords as tuple (x, y, z)"""
        return self.x, self.y, self.z

    @property
    def coords_int(self) -> tuple[int, int, int]:
        """
        Shorthand to get all coords as tuple (x, y, z) as integers

        warning: coordinates are rounded like Minecraft does it internally.
        this means that negative numbers are rounded up and positives are rounded down

        """
        return _coords_to_int(self.coords)

    def __eq__(self, other):
        if isinstance(other, EntityCollection):
            return self.type == other

        if not isinstance(other, type(self)):
            return False

        return self.id == other.id

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return (
            f"Entity("
            f"type={self.type}, "
            f"name={self.name}, "
            f"x={self.x}, "
            f"y={self.y}, "
            f"z={self.z}, "
            f"dimension={self.dimension}, "
            f"health={self.health}, "
            f"ai={self.ai}, "
            f"id={self.id}"
            f")"
        )

    @staticmethod
    def from_string(type: str):
        # TODO: do we need this? if not we can remove the default Nones
        return Entity(type=_to_enum(EntityCollection, type))

    @staticmethod
    def from_api_format(s: str, separator=ARG_SEPARATOR):
        _id, type, name, x, y, z, dimension, health, ai = s.split(separator)
        _type = _to_enum(EntityCollection, type)
        if _type is None:
            return None
        return Entity(
            id=_id,
            type=_type,
            name=name if name != "null" else None,
            x=_to_float(x),
            y=_to_float(y),
            z=_to_float(z),
            dimension=_to_enum(Dimension, dimension),
            health=_to_float(health),
            ai=ai == "true",
        )


class Player(BaseModel):
    """Snapshot at the time of the query, the data is NOT permanently updated!"""

    id: int
    """ Unique ID of the player """
    name: str
    """ Name of the player """
    x: float
    y: float
    z: float
    dimension: Dimension
    rotation: int
    """ Rotation of the player from -180 to 180 """
    looking_at_block: Material | None
    """ The next block the player is looking at (maximum 200 blocks away) """
    looking_at_entity: Entity | None
    """ The next entity the player is looking at (maximum 200 blocks away) """
    sneaked: bool
    """ True if player is sneaking """
    max_health: float
    health: float
    hunger: float
    saturation: float
    xp_level: float
    xp_progress: float
    holds_item: Optional["InventoryField"]

    @property
    def coords(self) -> tuple[float, float, float]:
        """Shorthand to get all coords as tuple (x, y, z)"""
        return self.x, self.y, self.z

    @property
    def coords_int(self) -> tuple[int, int, int]:
        """
        Shorthand to get all coords as tuple (x, y, z) as integers

        warning: coordinates are rounded like Minecraft does it internally (math.floor).
        this means that negative numbers are rounded up and positives are rounded down
        """
        return _coords_to_int(self.coords)

    @staticmethod
    def from_raw_data(data: bytes) -> "Player":
        """raw data is index, name, x, y, z"""
        if data == b"error invalid_index\n":
            raise ConnectionError(f"Can't fetch player. Are you sure this player is connected?")

        split = _bytes_to_text(data).split(ARG_SEPARATOR)
        (
            _id,
            name,
            x,
            y,
            z,
            dimension,
            rot,
            looking_at_block,
            looking_at_entity,
            sneaked,
            max_health,
            health,
            hunger,
            saturation,
            xp_level,
            xp_progress,
            held_item_data,
        ) = split

        return Player(
            id=int(_id),
            name=name,
            x=_to_float(x),
            y=_to_float(y),
            z=_to_float(z),
            dimension=_to_enum(Dimension, dimension),
            rotation=int(rot),
            looking_at_block=Material.from_api_format(looking_at_block),
            looking_at_entity=Entity.from_api_format(looking_at_entity, separator=ARG_SEPARATOR_SECOND_LEVEL),
            sneaked=sneaked.lower() == "true",
            max_health=_to_float(max_health),
            hunger=_to_float(hunger),
            saturation=_to_float(saturation),
            xp_level=_to_float(xp_level),
            xp_progress=_to_float(xp_progress),
            health=_to_float(health),
            holds_item=InventoryField.from_api_format(held_item_data),
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
            f"health={self.health}, "
            f"max_health={self.max_health}, "
            f"hunger={self.hunger}, "
            f"saturation={self.saturation}, "
            f"xp_level={self.xp_level}, "
            f"xp_progress={self.xp_progress}, "
            f"sneaked={self.sneaked}, "
            f"looking_at_block=<{self.looking_at_block}>, "
            f"looking_at_entity=<{self.looking_at_entity}>, "
            f"holds_item=<{self.holds_item}>"
            ")"
        )


class Item(BaseModel):
    """Models an item"""

    type: MaterialCollection
    display_name: str | None

    @staticmethod
    def from_api_format(s: str):
        """we expect ; separated contents here"""
        _type, display_name = s.split(";")
        if not display_name:
            display_name = None

        if not _type:
            _type = MaterialCollection.Air.value

        return Item(type=_to_enum(MaterialCollection, _type), display_name=display_name)

    def __repr__(self):
        return f"Item(type={self.type}, display_name={self.display_name})"


class InventoryField(Item):
    """A field in a player's inventory"""

    index: int
    """ Index where the field is located in the inventory """
    amount: int
    """ How many of the item are in this field """

    @staticmethod
    def from_api_format(s: str):
        split = s.split(":")

        idx, itm, amt = split
        itm = Item.from_api_format(itm)

        if not amt:
            amt = 0

        return InventoryField(index=int(idx), type=itm.type, display_name=itm.display_name, amount=int(amt))

    def __repr__(self):
        return f"InventoryField(index={self.index}, type={self.type}, diplay_name={self.display_name!r}, amount={self.amount})"

    def __eq__(self, other: object) -> bool:
        """
        Compare this field against another InventoryField, an Item or a MaterialCollection member.
        Against an InventoryField all fields are compared, against an Item only the Item fields
        (type and display name) and against a MaterialCollection member only the type.
        """
        if isinstance(other, InventoryField):
            return (
                self.type == other.type
                and self.display_name == other.display_name
                and self.index == other.index
                and self.amount == other.amount
            )

        if isinstance(other, Item):
            return self.type == other.type and self.display_name == other.display_name

        if isinstance(other, MaterialCollection):
            return self.type == other

        raise NotComparableException(f"Can't compare type '{type(other).__name__}' to type 'InventoryField'")


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
            if v == item:
                return True
        return False

    def __getitem__(self, item: int) -> InventoryField:
        try:
            return super().__getitem__(item)
        # I think this is the peak of the library. A non-generic wrapper around KeyError.
        except KeyError:
            raise InventoryFieldEmptyError(f"Field {item} is empty. Therefore you cannot access it here.")


class Message(BaseModel):
    """
    Represents a message sent to the chat by the user
    """

    text: str
    """The text sent to the chat"""
    sender_name: str
    """Name of the player that sent this message"""
    sender_id: int
    """ID of player that sent this message"""
    time_when_sent: datetime
    """Time when message was sent to chat"""

    def __eq__(self, other):
        if isinstance(other, str):
            return self.text == other

        if not isinstance(other, type(self)):
            return False

        # we can skip check for sender name
        #  they're just different identifier for the same player
        return (
            self.text == other.text
            and self.sender_id == other.sender_id
            and self.time_when_sent == other.time_when_sent
        )

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def from_unformatted_string(data: str):
        """from a value e.g. 'jumebonn1:2026|08|26|20|42|46:0:aaaa'"""
        sender_name, _date, sender_id, text = data.split(":")
        year, month, day, hour, minute, second = map(int, _date.split("|"))
        time_of_receival = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

        return Message(text=text, sender_name=sender_name, sender_id=int(sender_id), time_when_sent=time_of_receival)


class NotComparableException(NotImplementedError):
    """To be called when things can't be compared"""
