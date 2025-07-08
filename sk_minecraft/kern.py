"""
kern der bibliothek, hier wird mit dem server kommuniziert
diese datei stell auch einige hilfsfunktionen zur Verfügung
"""

import socket
from typing import Optional

from sk_minecraft.daten_modelle import KeineDatenFehler

# Globale Variable für die Verbindung
verbindung: Optional[socket.socket] = None


def verbinden(ip: str, port: int) -> None:
    """
    Stellt eine Verbindung zum Minecraft-Server her.

    Args:
        ip (str): Die IP-Adresse des Servers.
        port (int): Der Port des Servers.
    """
    global verbindung
    if verbindung is not None:
        verbindung.close()
    verbindung = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    verbindung.connect((ip, port))


def _empfangen(timeout: float = 2.0) -> bytes | None:
    verbindung.settimeout(timeout)  # Timeout in Sekunden
    try:
        data = verbindung.recv(1024)
    except socket.timeout:
        raise KeineDatenFehler(f"Timeout: Nach {timeout} sekunden wurde keine Antwort vom Server emofangen.")


    return data


def _bytes_zu_text(b: bytes) -> str:
    # häppchen zu text :)
    return b.decode("utf-8")


def _leerzeichen_behandel(s: str) -> str:
    return s.replace(" ", "|&s&|")


def _sende_befehl(befehl: str) -> None:
    """
    Sendet einen Befehl über die globale Verbindung.

    Args:
        befehl (str): Der zu sendende Befehl.
    """
    if verbindung is None:
        raise RuntimeError("Keine Verbindung zum Server. Bitte zuerst verbinden.")

    befehl = f"{befehl}\n"
    verbindung.sendall(befehl.encode("utf-8"))
