"""main functionalities of the library"""

from typing import Literal
from typing import cast

from st_minecraft.core.core import ARG_SEPARATOR
from st_minecraft.core.core import WertFehler
from st_minecraft.core.core import _build_command
from st_minecraft.core.core import _bytes_to_text
from st_minecraft.core.core import _receive
from st_minecraft.core.core import _send_command
from st_minecraft.en.data_models import Dimension
from st_minecraft.en.data_models import DirectionCollection
from st_minecraft.en.data_models import Entity
from st_minecraft.en.data_models import Inventory
from st_minecraft.en.data_models import InventoryField
from st_minecraft.en.data_models import Item
from st_minecraft.en.data_models import Material
from st_minecraft.en.data_models import Message
from st_minecraft.en.data_models import Player
from st_minecraft.en.data_models import dimensionT
from st_minecraft.en.entity import EntityCollection
from st_minecraft.en.material import MaterialCollection


def set_block(x: int, y: int, z: int, block_type: MaterialCollection, dimension: Dimension = Dimension.World) -> None:
    """
    Places a block in the Minecraft game.
    You can also use this to replace already existing blocks.
    If you want to "delete" a block, you can simply replace it with MaterialSammlung.Luft.
    An overview of all blocks can be found here:
    https://minecraft.fandom.com/wiki/Java_Edition_data_values#Blocks

    Args:
        x (int): X coordinate for the block
        y (int): Y coordinate for the block
        z (int): Z coordinate for the block
        block_type (MaterialCollection): Block as an element from MaterialCollection, e.g. MaterialCollection.Melone
        dimension (Dimension): dimension to look for the block (default.: Dimension.World)
    """
    # TODO: Determine the exact command format for the protocol
    command = _build_command("setBlock", x, y, z, dimension.value, block_type.value)
    _send_command(command)


def get_block(x: int, y: int, z: int, dimension: Dimension = Dimension.World) -> Material:
    """
    Query what type of block is at the coordinate
    You get a block object back that contains the type under .typ
    Note: An "empty" block is treated as an air block.

    Args:
        x (int): X coordinate of the block
        y (int): Y coordinate of the block
        z (int): Z coordinate of the block
        dimension (Dimension): dimension to look for the block (default.: Dimension.World)
    Returns:
        The block at the coordinate as data type `Material`
    """
    command = _build_command("getBlock", x, y, z, dimension.value)
    _send_command(command)
    data = _receive()
    block = Material.from_string(
        x=x, y=y, z=z, dimension=cast(dimensionT, dimension.value), type=_bytes_to_text(data).upper()
    )
    return block


def get_entity(entity: Entity) -> Entity:
    """Get the most current state of an already created entity
    Args:
        The Entity object from which you want to query an update
    Returns:
        An updated version of the corresponding entity

    """
    command = _build_command("getEntity", entity.id)
    _send_command(command)
    data = _receive()
    entity = Entity.from_api_format(_bytes_to_text(data))
    return entity


def get_player(index: int = 0) -> Player:
    """
    Query the state of a player.
    Players are numbered in the order in which they joined the server.
    Starting at 0 for the first player
    Args:
        index: Index of the player to query is optional (if you don't specify an index, index 0 is used)
    Returns:
        You get a player object back that contains a lot of information about the player
    """
    command = _build_command("getPlayer", index)
    _send_command(command)
    data = _receive()
    player = Player.from_raw_data(data)
    return player


def send_to_chat(message: str):
    """
    Send a message to the ingame chat.
    You can also apply special formatting, see this wiki entry:
    https://minecraft.fandom.com/de/wiki/Formatierungscodes
    Args:
        message: The message you want to send
    """
    command = _build_command("postChat", message)
    _send_command(command)


def get_chat() -> list[Message]:
    """
    Get all messages that have been written to the chat since the last query.
    Returns:
        You get a list of all sent messages back
    """
    command = _build_command("pollChat")

    _send_command(command)
    data = _receive()

    messages_str = _bytes_to_text(data)

    if messages_str == "":
        return []

    messages_str = messages_str.split(ARG_SEPARATOR)

    messages = [
        Message(text=text, sender_name=player_name) for player_name, text in map(lambda s: s.split(":"), messages_str)
    ]

    return messages


def seconds_to_ticks(seconds: float) -> int:
    """Converts seconds to ticks (rounding mode: floor)"""
    # there are 20 ticks per second
    return int(seconds * 20)


def show_title(
    text: str,
    *,
    subtitle: str = "",
    player_index: int = -1,
    fade_in_time: float = 1,
    display_time: float = 5,
    fade_out_time: float = 1,
):
    """
    Show a title message to a set of players.
    All arguments beside `text` are mandatory keyword-arguments e.g. show_title("hello", player_index=0, display_time=5)

    Args:
        text: The title to show (required)
        subtitle: The subtitle to show
        player_index: Index of a player, if the index is smaller then 0 the title is shown to all players
        fade_in_time: Time (in seconds) it takes for the title to fade in
        display_time: Time (in seconds) the title is displayed
        fade_out_time: Time (in seconds) it takes for the title to fade out
    """

    command = _build_command(
        "showTitle",
        player_index,
        text,
        subtitle,
        seconds_to_ticks(fade_in_time),
        seconds_to_ticks(display_time),
        seconds_to_ticks(fade_out_time),
    )
    _send_command(command)


def send_command(command: str):
    """
    Execute a Minecraft command, as if you were entering it on the server.
    The / at the beginning of a command is not necessary.
    Args:
        command: The command as a string without the slash / at the beginning.
    """
    if command.startswith("/"):
        print("Warning: You entered a '/' at the beginning of the command. This is probably not necessary!")
    command = _build_command("chatCommand", command)
    _send_command(command)


def spawn_entity(x: int, y: int, z: int, entity: EntityCollection, dimension: Dimension = Dimension.World) -> Entity:
    """
    Spawn an entity at a specific position
    A list of all entities can be found here:
    In German: https://minecraft.fandom.com/de/wiki/Objekt#ID-Namen
    In English (more detailed): https://minecraft.fandom.com/wiki/Java_Edition_data_values#Entities
    Args:
        x (int): X coordinate where the entity should be spawned
        y (int): Y coordinate where the entity should be spawned
        z (int): Z coordinate where the entity should be spawned
        entity: An element from EntitySammlung e.g. EntitySammlung.Schaf
        dimension (Dimension): dimension to look for the block (default.: Dimension.World)

    Returns:
        You get an Entity object back. With this you can later access the entity again.
    """
    command = _build_command("spawnEntity", x, y, z, dimension.value, entity.value)
    print(command)
    _send_command(command)
    data = _receive()
    entity = Entity.from_api_format(_bytes_to_text(data))
    return entity


def give_item(
    player: Player,
    item: MaterialCollection,
    amount: int,
    name: str | None = None,
    inventory_slot: int | None = None,
    unbreakable: bool = False,
) -> Inventory:
    """
    Give a player an item
    The available items are also in MaterialSammlung
    A list of all items can be found here:
    https://minecraft.fandom.com/wiki/Java_Edition_data_values#Items (is in English)
    Args:
        player: Player who should receive the item
        item: Item as an element of MaterialSammlung, e.g. MaterialSammlung.Diamantschwert
        amount: How many should be given
        name: (optional) What should the item be called?
        inventory_slot: (optional) Slot where the item should land (as a number)
        unbreakable: (optional) If the item should be unbreakable set to True, the default is breakable

    Returns:
        You get information about the inventory state of the player after the item was given

    """
    if isinstance(item, Item):
        item = item.typ

    args = ["addInv", player.id, item.value, amount]

    if name is not None:
        args.append(f"name:{name}")

    if inventory_slot is not None:
        args.append(f"slot:{inventory_slot}")

    if unbreakable:
        args.append("unbreakable")

    command = _build_command(*args)
    _send_command(command)

    return get_inventory(player)


def get_inventory(player: Player) -> Inventory:
    """
    Retrieve the inventory of a player.
    Args:
        player: Player from whom you want to query the inventory

    Returns:
        You get an inventory object (like a dict) back"""
    command = _build_command("getInv", player.id)
    _send_command(command)
    data = _receive()

    # example for (simple) received data:
    # (index,name;optional;infos:amount)
    # 0:LILY_OF_THE_VALLEY:1𝇉4:STONE_PRESSURE_PLATE:1𝇉25:DISPENSER:1𝇉29:TARGET:1
    inventory_info = _bytes_to_text(data)
    if not inventory_info:
        return Inventory()

    item_infos = inventory_info.split(ARG_SEPARATOR)

    # build inventory dict together
    inventory = Inventory()
    for item in item_infos:
        # catch empty strings
        if not item:
            continue
        field = InventoryField.from_api_format(item)
        inventory[field.index] = field

    return inventory


def set_player_position(
    player: Player, x: int, y: int, z: int, *, rotation: int = None, dimension: Dimension = Dimension.World
) -> Player:
    """
    Change the position in x-, y-, z-direction and rotation
    Args:
        player: Player to be edited
        x: new x coordinate
        y: new y coordinate
        z: new z coordinate
        rotation: (optional) rotation of the player (from -180 to 180), if you don't specify it, it won't be changed.
        dimension (Dimension): dimension to put the player in (default.: Dimension.World)


    Returns:
        You get an updated version of the player back (state after being moved)
    """
    args = ["setPlayerPos", player.id, x, y, z, dimension.value]
    if rotation is not None:
        if not -180 <= rotation <= 180:
            raise WertFehler(f"A player's rotation must be between -180 and 180. You said '{rotation}'.")

        args.append(f"rotation:{rotation}")

    command = _build_command(*args)
    _send_command(command)

    return get_player(player.id)


def set_player_velocity(player: Player, direction: DirectionCollection, value: float) -> Player:
    """
    Change the movement speed of a player in different directions.
    All directions you can influence can be found in RichtungSammlung

    Args:
        player: Player object that should be influenced
        direction: Direction that should be changed, as an element of RichtungSammlung, e.g. RichtungSammlung.Vorwärts
        value: 1 is normal speed, 0 is freeze, the number can be arbitrarily large (and thus arbitrarily fast)
    Returns:
        You get an updated version of the player back (state after the speed was changed)

    """
    command = _build_command("setPlayerVelocity", direction.value, player.id, value)
    _send_command(command)
    return get_player(player.id)


def set_player_max_health(player: Player, value: float) -> Player:
    """Set the maximum health of a player"""
    _set_player_property("MAX_HEALTH", player, value)
    return get_player(player.id)


def set_player_health(player: Player, value: float) -> Player:
    """
    Set the current health of a player
    If the value is greater than the set maximum, all excess health is ignored
    Args:
        player: Player object that should be influenced
        value: Amount of health as a decimal number.
    Returns:
        You get an updated version of the player back (state after the health was changed)
    """
    _set_player_property("HEALTH", player, value)
    return get_player(player.id)


def set_player_hunger(player: Player, value: float, saturation: float | None = None) -> Player:
    """
    Set the hunger of a player.
    You can optionally also set the saturation.

    Args:
        player: Player object that should be influenced
        value: Amount of hunger as a decimal number.
        saturation: (optional) You can set the saturation. If you leave it empty, it won't be changed.
    Returns:
        You get an updated version of the player back (state after the hunger was changed)
    """
    _set_player_property("FOOD_LEVEL", player, value)
    if saturation is not None:
        _set_player_property("SATURATION", player, saturation)

    return get_player(player.id)


def set_player_xp_level(player: Player, value: float) -> Player:
    """
    Set the current level of a player

    Args:
        player: Player object that should be influenced
        value: Level as a decimal number
    Returns:
        You get an updated version of the player back (state after the level was changed)
    """
    _set_player_property("XP_LEVEL", player, value)
    return get_player(player.id)


def set_player_xp_progress(player: Player, value: float) -> Player:
    """
    Set the progress within a player's level
    Args:
        player: Player object that should be influenced
        value: Progress as a decimal number
    Returns:
        You get an updated version of the player back (state after the progress was changed)
    """
    _set_player_property("XP_PROGRESS", player, value)
    return get_player(player.id)


def _set_player_property(type: str, player: Player, value: float):
    """internal function for changing health, hunger and xp"""
    command = _build_command("setPlayerStat", type, player.id, value)
    _send_command(command)


def set_entity_name(entity: Entity, name: str) -> Entity:
    """
    Set the name of an entity
    Args:
        entity: The entity to be edited, not EntitySammlung!
        name: The new name of the entity
    Returns:
        An updated version of the entity (state after the change)
    """
    command = _build_command("editEntity", entity.id, f"name:{name}")
    _send_command(command)
    return get_entity(entity)


def set_entity_position(entity: Entity, x: float, y: float, z: float, dimension: Dimension = Dimension.World) -> Entity:
    """
    Set the position of an entity

    Args:
        entity: The entity to be edited, not EntitySammlung!
        x (int): new X coordinate
        y (int): new Y coordinate
        z (int): new Z coordinate
        dimension (Dimension): dimension to look for the block (default.: Dimension.World)
    Returns:
        An updated version of the entity (state after the change)
    """
    command = _build_command("editEntity", entity.id, f"position:{x};{y};{z};{dimension.value}")
    _send_command(command)
    return get_entity(entity)


def set_entity_ai(entity: Entity, status: bool) -> Entity:
    """
    Set the AI of an entity. If it has no AI (False), it doesn't move.

    Args:
        entity: The entity to be edited, not EntitySammlung!
        status: True (if it should move), otherwise False

    Returns:
        An updated version of the entity (state after the change)
    """
    command = _build_command("editEntity", entity.id, f"ai:{status}")
    _send_command(command)
    return get_entity(entity)


def set_entity_health(entity: Entity, health: float) -> Entity:
    """
    Set the health of an entity. If health is set to 0, it dies.

    Args:
        entity: The entity to be edited, not EntitySammlung!
        health: How many health points the entity should have (0=dead).
    """
    command = _build_command("editEntity", entity.id, f"health:{health}")
    _send_command(command)
    return get_entity(entity)


def _validate_id(id: str, type: Literal["MATERIAL", "ENTITY"]):
    """only for internal use"""
    command = _build_command("validate", type, id)
    _send_command(command)
    data = _receive()

    return _bytes_to_text(data)
