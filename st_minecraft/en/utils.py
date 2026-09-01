"""
Extension that contains shortcuts, that go beyond the core functionality.
Some signature complexities exceed beginner level and are meant for more advanced use cases.
This extension is not held to the same rigorous standards as the core library.
It may introduce breaking changes even in minor updates.
"""

import time
from typing import Callable
from typing import Literal

from st_minecraft.core import connect
from st_minecraft.de import Material
from st_minecraft.en import MaterialCollection
from st_minecraft.en import Player
from st_minecraft.en import boss_bar
from st_minecraft.en import get_block
from st_minecraft.en import send_to_chat
from st_minecraft.en import set_block
from st_minecraft.en import wait


def get_block_below_player(player: Player, y_level: int = -1) -> Material:
    """
    Get the block below the player by simply passing the player

    Args:
        player: the player to use
        y_level: y-level offset of player (-1 -> block directly under player, -10 -> 10 block below)
    """
    return get_block(player.x, player.y + y_level, player.z)


def set_block_below_player(player: Player, material: MaterialCollection, at: int = -1) -> None:
    """
    Set a block below a player

    Args:
        player: the player to use
        material: the material to use
        at: y-level offset of player (-1 -> block directly under player, -10 -> 10 block below)
    """
    set_block(player.x, player.y + at, player.z, material)


def plattform_below_player(player: Player, radius: int, material: MaterialCollection, y_level: int = -1):
    """
    Set an N x N platform below a player

    Args:
        player: the player to use
        radius: radius around player with player in center (1 -> 3x3, 2 -> 5x5)
        material: the material to use
        y_level: y-level offset of player (-1 -> block directly under player, -10 -> 10 block below)
    """
    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            set_block(player.x + x, y_level, player.z + z, material)


def countdown(seconds: int = 10, send_in_chat: bool = True):
    """
    Do a countdown. This function returns when countdown has finished

    Args:
        seconds: seconds to wait
        send_in_chat: if True (default) the countdown will be sent to chat

    Returns:

    """
    for i in range(seconds, 0, -1):
        if send_in_chat:
            send_to_chat(f"{i}")
        wait(1)


def countdown_boss_bar(
    seconds: float,
    bar: boss_bar.BossBar,
    run_down: Literal["down", "up"] = "down",
    delete_on_end: bool = True,
    do_in_each_step: Callable = lambda: None,
    time_step_size: float = 0.1,
) -> boss_bar.BossBar:
    """
    Display time progress via boss-bar and optionally execute a task each time step.
    Args:
        seconds: seconds to countdown (allows for float, e.g. 1.5)
        bar: the boss-bar to do the countdown with
        run_down: decide if bar shall run down or fill (default is "down")
        delete_on_end: whether the boss-bar shall be deleted when countdown reached 0 (default: True)
        do_in_each_step: a function to be called each time step
        time_step_size: step size of the countdown (default: 0.1)

    Returns: remaining state of the boss-bar passed to the function (remember: if delete_on_end the bar is deleted)
    """

    # run down case
    if run_down:
        bar = boss_bar.set_value(bar, 1)
    # run up case
    else:
        bar = boss_bar.set_value(bar, 0)

    remaining_time = seconds
    step_size = 1 / (seconds * 10)
    while remaining_time > 0:
        do_in_each_step()

        if run_down:
            wert = bar.value - step_size
        else:
            wert = bar.value + step_size

        # run down case
        if wert < 0:
            wert = 0
        # run up case
        elif wert > 1:
            wert = 1

        bar = boss_bar.set_value(bar, wert)
        wait(0.1)
        remaining_time = remaining_time - time_step_size

    if delete_on_end:
        boss_bar.delete_bar(bar)

    return bar


if __name__ == "__main__":
    connect()

    b = boss_bar.create_bar("test", "test")
    countdown_boss_bar(2.33, b, run_down="down", delete_on_end=False)
    countdown_boss_bar(1.33, b, run_down="up", do_in_each_step=lambda: print(time.time()))
