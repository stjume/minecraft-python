"""
Core of the library, here communication with the server happens
this file also provides some helper functions
"""

import os
import socket
from enum import Enum
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar

# Global variable for the connection
connection: Optional[socket.socket] = None

ARG_SEPARATOR = "𝇉"

DEFAULT_PORT = 25595


def connect(ip: str, port: int = DEFAULT_PORT) -> None:
    """
    Establishes a connection to the Minecraft server.

    Args:
        ip (str): The IP address of the server.
        port (int): The port of the server.
    """
    # needed internally
    global connection
    if connection is not None:
        connection.close()

    # this allows us to develop more easily without having to adjust everything temporarily each time
    _ip = os.getenv("SK_SERVER_OVERWRITE")
    if _ip is not None:
        spacer = "#" * 100
        print(
            f"{spacer}\n"
            f"IP was overwritten by environment variable from '{ip}' to '{_ip}', "
            f"(env var name: 'SK_SERVER_OVERWRITE')\n"
            f"{spacer}"
        )
        ip = _ip

    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((ip, port))


def _receive(timeout: float = 2.0) -> bytes | None:
    # needed internally

    # this allows us to develop more easily without having to adjust everything temporarily each time
    _timeout = os.getenv("SK_TIMEOUT_OVERWRITE")
    if _timeout is not None:
        if _timeout == "None":
            _timeout = None

        spacer = "#" * 100
        print(
            f"{spacer}\n"
            f"Timeout was overwritten by environment variable from '{timeout}' to '{_timeout}', "
            f"(env var name: 'SK_TIMEOUT_OVERWRITE')\n"
            f"{spacer}"
        )
        timeout = _timeout

    if timeout:
        connection.settimeout(timeout)  # Timeout in seconds

    try:
        data = connection.recv(1024)
    except socket.timeout:
        raise NoDataError(f"Timeout: After {timeout} seconds no response was received from the server.")

    return data


def _build_command(*args: Any) -> str:
    """
    Takes all arguments, converts them to strings and builds the finished command from them
    """
    return ARG_SEPARATOR.join(map(str, args))


def _bytes_to_text(b: bytes) -> str:
    # needed internally
    # bytes to text :)
    return b.decode("utf-8").strip()


def _send_command(command: str) -> None:
    """
    Sends a command over the global connection.

    Args:
        command (str): The command to send.
    """
    # needed internally
    if connection is None:
        raise RuntimeError("No connection to server. Please connect first.")

    command = f"{command}\n"
    connection.sendall(command.encode("utf-8"))


E = TypeVar("E", bound=Enum)


def _to_enum(enum: Type[E], value: Any) -> Optional[E]:
    return enum._value2member_map_.get(value)


class NoDataError(ValueError):
    """Raised when we receive nothing from the API"""


class WertFehler(ValueError):
    """ValueError aber deutsch :clown face:"""


class InventoryFieldEmptyError(KeyError):
    """Raised when trying to access an inventory field that is empty."""
