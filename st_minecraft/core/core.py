"""
Core of the library, here communication with the server happens
this file also provides some helper functions
"""

import os
import socket
from enum import Enum
from typing import Any
from typing import Literal
from typing import Optional
from typing import Type
from typing import TypeVar

# Global variable for the connection
connection: Optional[socket.socket] = None

ARG_SEPARATOR = "𝇉"

DEFAULT_PORT = 25595

_default_ip_options = ("0.0.0.0", "127.0.0.1", "localhost")
"""Options we try, to find a running server (with plugin) on the local device"""

_default_ip: Literal["0.0.0.0", "127.0.0.1", "localhost"] | None = None
"""
default IP the library tries to connect to
it is determined when connect() is called the first time without passing an IP
"""
# reason: we had issues on Windows to connect via 0.0.0.0
# 127.0.0.1 and localhost worked tho
# -> we try all  options stored in _default_ip_options (below) and see if one sticks before potentially raising
# the default_ip variable exists to save a successful find (so we don't try each time)


def connect(ip: str | None = None, port: int = DEFAULT_PORT) -> None:
    """
    Establishes a connection to the Minecraft server.

    Args:
        ip (str): IP address of the minecraft server, attempts to connect to localhost if left empty (or None is passed)
        port (int): The port the plugin is listening on
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
    # this should not happen. but pycharm said this was an issue, so we add this case.
    if connection is None:
        raise ConnectionError(
            f"Can't open a socket. Please find out why `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` failed"
        )

    # we got an explicit IP passed (or the env overwrite was set)
    if ip:
        connection.connect((ip, port))
        return

    # we previously found a successful connection in our defaults
    # -> this case can only happen when connect() was already called once
    global _default_ip
    if _default_ip is not None:
        connection.connect((ip, port))
        return

    # we're here for the first time.
    # we don't know where the server is so we try out a few options
    # if one sticks we save the result (globally)
    # if none sticks, we raise
    for option in _default_ip_options:

        # attempt connection
        try:
            connection.connect((option, port))

            # save globally
            _default_ip = option
            # we can exit the loop
            break

        # socket errors come in so many names and shapes, depending on OS and what exactly failed
        # so we deliberately use the broad 'catch all' here (:
        except Exception as e:
            pass  # silently eat it

    # break wasn't hit. we now fail. and give the user helpful information.
    else:
        ips = ", ".join(f"'{i}:{port}'" for i in _default_ip_options)
        msg = (
            f"Can't connect to server!\n"
            f"**Please check if the server is running and the plugin is located in the plugins folder**.\n"
            f"Tried to connect to {ips}.\n"
            f"If you're trying to connect to a server on another device, "
            f"please pass the IP of it to the connect() function (e.g. `connect(ip='192.168.1.10')`.\n"
            f"If the port the plugin listens to was changed, "
            f"you have to pass the port to the function (e.g. `connect(port='31415')`. "
            f"IP and port changes can be passed at the same time.\n"
            f"If you're unsure how to run a server with the (matching) plugin, please refer to our backend repository: "
            f"https://github.com/stjume/minecraft-python-backend"
        )
        raise ConnectionError(msg)


def _receive(timeout: float = 2.0) -> bytes | None:
    # needed internally

    # this allows us to develop more easily without having to adjust everything temporarily each time
    _timeout = os.getenv("SK_TIMEOUT_OVERWRITE")
    if _timeout is not None:
        if _timeout == "None":
            _timeout = None
        else:
            _timeout = float(_timeout)

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


class InventoryFieldEmptyError(KeyError):
    """Raised when trying to access an inventory field that is empty."""
