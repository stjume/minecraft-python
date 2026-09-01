"""
Erweiterung mit Abkürzungen, die über die Kern-Funktionalität hinausgehen.
Einige Signaturen sind komplexer als das Anfänger-Niveau und für fortgeschrittene Anwendungsfälle gedacht.
Diese Erweiterung wird nicht an die gleichen strengen Standards wie die Kern-Bibliothek gehalten.
Sie kann auch in kleineren Updates zu Änderungen führen, die bestehenden Code brechen.
"""

import time
from typing import Callable
from typing import Literal

import st_minecraft.en.utils as __st_minecraft_en_utils
from st_minecraft.core import connect as verbinden
from st_minecraft.de import Material
from st_minecraft.de import MaterialSammlung
from st_minecraft.de import Spieler
from st_minecraft.de import boss_leiste
from st_minecraft.de import hole_block
from st_minecraft.de import sende_an_chat
from st_minecraft.de import setze_block
from st_minecraft.de import warte


def hole_block_unter_spieler(spieler: Spieler, y_level: int = -1) -> Material:
    """
    Hole den Block unter dem Spieler, indem du einfach den Spieler übergibst.

    Args:
        spieler: Der zu verwendende Spieler
        y_level: Y-Versatz zum Spieler (-1 -> Block direkt unter dem Spieler, -10 -> 10 Blöcke darunter)
    """
    return hole_block(spieler.x, spieler.y + y_level, spieler.z)


def setze_block_unter_spieler(spieler: Spieler, block_typ: MaterialSammlung, y_level: int = -1) -> None:
    """
    Setze einen Block unter einem Spieler.

    Args:
        spieler: Der zu verwendende Spieler
        block_typ: Das zu verwendende Material
        y_level: Y-Versatz zum Spieler (-1 -> Block direkt unter dem Spieler, -10 -> 10 Blöcke darunter)
    """
    setze_block(spieler.x, spieler.y + y_level, spieler.z, block_typ)


def plattform_unter_spieler(spieler: Spieler, radius: int, block_typ: MaterialSammlung, y_level: int = -1):
    """
    Setze eine N x N Plattform unter einem Spieler.

    Args:
        spieler: Der zu verwendende Spieler
        radius: Radius um den Spieler mit dem Spieler im Zentrum (1 -> 3x3, 2 -> 5x5)
        block_typ: Das zu verwendende Material
        y_level: Y-Versatz zum Spieler (-1 -> Block direkt unter dem Spieler, -10 -> 10 Blöcke darunter)
    """
    for x in range(-radius, radius + 1):
        for z in range(-radius, radius + 1):
            setze_block(spieler.x + x, y_level, spieler.z + z, block_typ)


def countdown(sekunden: int = 10, sende_in_chat: bool = True) -> None:
    """
    Führe einen Countdown aus. Diese Funktion kehrt zurück, wenn der Countdown beendet ist.

    Args:
        sekunden: Sekunden, die gewartet werden soll
        sende_in_chat: Wenn True (Standard) wird der Countdown in den Chat gesendet
    """
    for i in range(sekunden, 0, -1):
        if sende_in_chat:
            sende_an_chat(f"{i}")
        warte(1)


def countdown_boss_leiste(
    sekunden: float,
    leiste: boss_leiste.BossLeiste,
    runterzählen: Literal["down", "up"] = "down",
    löschen_am_ende: bool = True,
    mache_in_jedem_schritt: Callable = lambda: None,
    zeit_schritt_größe: float = 0.1,
) -> boss_leiste.BossLeiste:
    """
    Zeige den Zeit-Fortschritt über eine Boss-Leiste an und führe optional in jedem Zeitschritt eine Aufgabe aus.

    Args:
        sekunden: Sekunden, die heruntergezählt werden (erlaubt Kommazahlen, z.B. 1.5)
        leiste: Die Boss-Leiste, mit der der Countdown ausgeführt wird
        runterzählen: Ob die Leiste leer laufen ("down") oder sich füllen ("up") soll (Standard: "down")
        löschen_am_ende: Ob die Boss-Leiste bei 0 gelöscht werden soll (Standard: True)
        mache_in_jedem_schritt: Eine Funktion, die in jedem Zeitschritt aufgerufen wird
        zeit_schritt_größe: Schrittweite des Countdowns (Standard: 0.1)

    Returns:
        Verbleibender Zustand der übergebenen Boss-Leiste (Achtung: bei loeschen_am_ende ist die Leiste gelöscht)
    """
    b = __st_minecraft_en_utils.countdown_boss_bar(
        sekunden,
        leiste.zu_englisch(),
        run_down=runterzählen,
        delete_on_end=löschen_am_ende,
        do_in_each_step=mache_in_jedem_schritt,
        time_step_size=zeit_schritt_größe,
    )
    return boss_leiste.BossLeiste.von_englisch(b)


if __name__ == "__main__":
    verbinden()

    b = boss_leiste.erzeuge_leiste("test", "test")
    countdown_boss_leiste(2.33, b, runterzählen="down", löschen_am_ende=False)
    countdown_boss_leiste(1.33, b, runterzählen="up", mache_in_jedem_schritt=lambda: print(time.time()))
