# sk_minecraft package 

import socket
from typing import Optional
from sk_minecraft.daten_modelle import Spieler

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


def _sende_befehl(befehl: str) -> None:
    """
    Sendet einen Befehl über die globale Verbindung.

    Args:
        befehl (str): Der zu sendende Befehl.
    """
    if verbindung is None:
        raise RuntimeError("Keine Verbindung zum Server. Bitte zuerst verbinden.")
    # TODO: Protokollformat für die Übertragung implementieren
    befehl = f"{befehl}\n"
    verbindung.sendall(befehl.encode("utf-8"))


def setze_block(x: int, y: int, z: int, block_typ: str) -> None:
    """
    Setzt einen Block im Minecraft-Spiel.

    Args:
        x (int): X-Koordinate
        y (int): Y-Koordinate
        z (int): Z-Koordinate
        block_typ (str): Typ des Blocks
    """
    # TODO: Das genaue Befehlsformat für das Protokoll festlegen
    befehl = f"setBlock {x} {y} {z} {block_typ}"
    _sende_befehl(befehl)


def hole_spieler_koordinaten(index: int = 0) -> Spieler:
    """
    Gibt die Koordinaten des Spielers zurück.
    """
    befehl = f"getPlayerLoc {index}"
    _sende_befehl(befehl)
    print("befehl gesendet")
    verbindung.settimeout(2.0)  # Timeout in Sekunden
    try:
        data = verbindung.recv(1024)
    except socket.timeout:
        print("Timeout: Keine Daten empfangen")
        return None
    spieler = Spieler.von_rohdaten(data)
    return spieler


