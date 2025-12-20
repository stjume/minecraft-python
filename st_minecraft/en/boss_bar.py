"""Enables creating and configuring boss bars"""

from enum import Enum

from pydantic import BaseModel

from st_minecraft.core.core import ARG_SEPARATOR
from st_minecraft.core.core import WertFehler
from st_minecraft.core.core import _build_command
from st_minecraft.core.core import _send_command


class BossBarStyle(Enum):
    """Ways in which the style of a boss bar can be displayed"""

    SOLID = "solid"
    SEGMENTED_6 = "segmented_6"
    SEGMENTED_10 = "segmented_10"
    SEGMENTED_12 = "segmented_12"
    SEGMENTED_20 = "segmented_20"


class BossBarColor(Enum):
    """Colors in which a boss bar can be displayed"""

    BLUE = "blue"
    GREEN = "green"
    PINK = "pink"
    PURPLE = "purple"
    RED = "red"
    WHITE = "white"
    YELLOW = "yellow"


class BossBar(BaseModel):
    """Model of a boss bar"""

    name: str
    """ The name you set for the bar """
    display_text: str
    """ The text that is displayed on the bar """
    value: float  # between 0 and 1
    """ How much of the bar should be filled (between 0 and 1) """
    style: BossBarStyle
    """ Display style of the bar (see BossBarStyle) """
    color: BossBarColor
    """ Display color of the bar (see BossBarColor) """

    def __repr__(self):
        return (
            f"BossBar(name={self.name}, "
            f"display_text={self.display_text}, "
            f"value={self.value:.2f}, "
            f"style={self.style}, "
            f"color={self.color})"
        )


def _send_boss_bar_command(sub_command: str):
    # needed internally
    command = f"editBossBar{ARG_SEPARATOR}{sub_command}"
    _send_command(command)


def create_bar(name: str, display_text: str) -> BossBar:
    """
    Create a boss bar
    Args:
        name: A name you choose, what the boss bar should be called for you
        display_text: Text that should be displayed on the bar

    Returns:
        A BossBar object with which you can further configure the bar
    """
    command = _build_command("spawnBossBar", name, display_text)
    _send_command(command)

    # some of the values are set when creating.
    return BossBar(
        name=name,
        display_text=display_text,
        value=0.0,
        style=BossBarStyle.SOLID,
        color=BossBarColor.PURPLE,
    )


def set_text(boss_bar: BossBar, display_text: str) -> BossBar:
    """Set the text of the bar"""
    sub_command = _build_command("text", boss_bar.name, f"text:{display_text}")
    _send_boss_bar_command(sub_command)
    boss_bar.display_text = display_text
    return boss_bar


def set_color(boss_bar: BossBar, color: BossBarColor) -> BossBar:
    """Set the color of the bar"""
    sub_command = _build_command("color", boss_bar.name, f"color:{color.value}")
    _send_boss_bar_command(sub_command)
    boss_bar.color = color
    return boss_bar


def set_value(boss_bar: BossBar, value: float) -> BossBar:
    """Set to what proportion the bar should be filled (between 0 and 1)"""
    if not 0 <= value <= 1:
        raise WertFehler(f"The value of the boss bar must be between 0 and 1. You specified '{value}'.")

    sub_command = _build_command("value", boss_bar.name, f"value:{value}")
    _send_boss_bar_command(sub_command)
    boss_bar.value = value
    return boss_bar


def set_style(boss_bar: BossBar, style: BossBarStyle) -> BossBar:
    """Set the style of the bar"""
    sub_command = _build_command("style", boss_bar.name, f"style:{style.value}")
    _send_boss_bar_command(sub_command)
    boss_bar.style = style
    return boss_bar


def delete_bar(boss_bar: BossBar):
    """Delete a bar"""
    _delete_bar_str(boss_bar.name)


def _delete_bar_str(boss_bar_name: str):
    command = _build_command("deleteBossBar", boss_bar_name)
    _send_command(command)
