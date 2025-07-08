""" Ermöglicht das erstellen und konfigurieren von Bossleisten """

from sk_minecraft.kern import _leerzeichen_behandel, _sende_befehl
from sk_minecraft.daten_modelle import BossLeiste, WertFehler, BossLeisteFarben, BossLeisteStil


def _sende_boss_leiste_befehl(unter_befehl: str):
    # brauchen wir intern
    befehl = f"editBossBar {unter_befehl}"
    _sende_boss_leiste_befehl(befehl)


def erzeuge_leiste(name: str, anzeige_text: str) -> BossLeiste:
    """
    Erstelle eine Bossleiste
    Args:
        name: Ein von dir gewählter Name, wie die Bossleiste für dich heißen soll
        anzeige_text: Text der an der Leiste angezeigt werden soll

    Returns:
        Ein BossLeisten Objekt mit dessen Hilfe du die Leiste weiter konfigurieren kannst
    """
    befehl = f"spawnBossBar {name} {anzeige_text}"
    _sende_boss_leiste_befehl(befehl)

    # einige der werte sind beim erzeugen festgesetzt.
    return BossLeiste(
        name=name,
        anzeige_text=anzeige_text,
        wert=0.0,
        stil=BossLeisteStil.DURCHGEZOGEN,
        color=BossLeisteFarben.LILA
    )

def setze_text(boss_leiste: BossLeiste, anzeige_text: str):
    """ Setze den Text der Leiste """
    unter_befehl = f"text {boss_leiste.name} text:{_leerzeichen_behandel(anzeige_text)}"
    _sende_boss_leiste_befehl(unter_befehl)


def setze_farbe(boss_leiste: BossLeiste, farbe: BossLeisteFarben):
    """ Setze die Farbe der Leiste """
    unter_befehl = f"color {boss_leiste.name} color:{farbe.value}"
    _sende_boss_leiste_befehl(unter_befehl)


def setze_wert(boss_leiste: BossLeiste, wert: float):
    """ Setze zu welchem Anteil die leiste gefüllt sein soll (zwischen 0 und 1) """
    if not 0 < wert <= 1:
        raise WertFehler(f"Der Wert der Bossleiste muss zwischen 0 und 1 liegen. Du hast '{wert}' angegeben.")

    unter_befehl = f"value {boss_leiste.name} value:{wert}"
    _sende_boss_leiste_befehl(unter_befehl)


def setze_stil(boss_leiste: BossLeiste, stil: BossLeisteStil):
    """ Setze den Stil der Leiste """
    unter_befehl = f"style {boss_leiste.name} color:{stil.value}"
    _sende_boss_leiste_befehl(unter_befehl)
    
