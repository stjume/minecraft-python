"""
kern der bibliothek, hier wird mit dem server kommuniziert
diese datei stell auch einige hilfsfunktionen zur Verfügung
"""

import os
import socket
from enum import Enum
from typing import Any
from typing import Optional
from typing import Type
from typing import TypeVar

# Globale Variable für die Verbindung
verbindung: Optional[socket.socket] = None

ARG_SEPARATOR = "𝇉"


def verbinden(ip: str, port: int) -> None:
    """
    Stellt eine Verbindung zum Minecraft-Server her.

    Args:
        ip (str): Die IP-Adresse des Servers.
        port (int): Der Port des Servers.
    """
    # brauchen wir intern
    global verbindung
    if verbindung is not None:
        verbindung.close()

    # hierdurch können wir leichter entwickeln, ohne jedes Mal alle temporär anpassen zu müssen
    _ip = os.getenv("SK_SERVER_OVERWRITE")
    if _ip is not None:
        spacer = "#" * 100
        print(
            f"{spacer}\n"
            f"IP wurde von von Environment Variable von '{ip}' auf '{_ip}', "
            f"(env var name: 'SK_SERVER_OVERWRITE') überschrieben\n"
            f"{spacer}"
        )
        ip = _ip

    verbindung = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    verbindung.connect((ip, port))


def _empfangen(timeout: float = 2.0) -> bytes | None:
    # brauchen wir intern

    # hierdurch können wir leichter entwickeln, ohne jedes Mal alle temporär anpassen zu müssen
    _timeout = os.getenv("SK_TIMEOUT_OVERWRITE")
    if _timeout is not None:
        if _timeout == "None":
            _timeout = None

        spacer = "#" * 100
        print(
            f"{spacer}\n"
            f"Timeout wurde von von Environment Variable von '{timeout}' auf '{_timeout}', "
            f"(env var name: 'SK_TIMEOUT_OVERWRITE') überschrieben\n"
            f"{spacer}"
        )
        timeout = _timeout

    if timeout:
        verbindung.settimeout(timeout)  # Timeout in Sekunden

    try:
        data = verbindung.recv(1024)
    except socket.timeout:
        raise KeineDatenFehler(f"Timeout: Nach {timeout} sekunden wurde keine Antwort vom Server emofangen.")

    return data


def _baue_command(*args: Any) -> str:
    """
    Nimmt alle argumente entgegen, konvertiert sie in strings und baut daraus den fertigen command
    """
    return ARG_SEPARATOR.join(map(str, args))


def _bytes_zu_text(b: bytes) -> str:
    # brauchen wir intern
    # häppchen zu text :)
    return b.decode("utf-8").strip()


def _sende_befehl(befehl: str) -> None:
    """
    Sendet einen Befehl über die globale Verbindung.

    Args:
        befehl (str): Der zu sendende Befehl.
    """
    # brauchen wir intern
    if verbindung is None:
        raise RuntimeError("Keine Verbindung zum Server. Bitte zuerst verbinden.")

    befehl = f"{befehl}\n"
    verbindung.sendall(befehl.encode("utf-8"))


E = TypeVar("E", bound=Enum)


def _zu_enum_umwandeln(enum: Type[E], wert: Any) -> Optional[E]:
    return enum._value2member_map_.get(wert)


class KeineDatenFehler(ValueError):
    """Wird geworfen, wenn wir von der API nix empfangen"""


class WertFehler(ValueError):
    """ValueError aber deutsch :clown face:"""


class InventarFeldLeerFehler(KeyError):
    """Wird geworfen, wenn versucht wird auf ein Inventar-Feld zuzugreifen, dass leer ist."""
