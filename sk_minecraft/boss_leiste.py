""" Ermöglicht das erstellen und konfigurieren von Bossleisten """
from enum import Enum

from pydantic import BaseModel

from sk_minecraft.kern import _leerzeichen_behandel, WertFehler, _sende_befehl


class BossLeisteStil(Enum):
    """ Möglichkeiten in denen der Stil einer Bossleiste angezeigt werden kann """
    DURCHGEZOGEN = "solid"
    SEGMENTE_6 = "segmented_6"
    SEGMENTE_10 = "segmented_10"
    SEGMENTE_12 = "segmented_12"
    SEGMENTE_20 = "segmented_20"


class BossLeisteFarben(Enum):
    """ Farben in denen eine Bossleiste angezeigt werden kann """
    BLAU = "blue"
    GRÜN = "green"
    PINK = "pink"
    LILA = "purple"
    ROT = "red"
    WEIß = "white"
    GELB = "yellow"


class BossLeiste(BaseModel):
    """ Modell einer Bossleiste """
    name: str
    """ Der von dir für die Leiste gesetze Name """
    anzeige_text: str
    """ Der Text der auf der Leiste angezeigt wird """
    wert: float  # zwischen 0 und 1
    """ Wie viel von der Leiste gefüllt sein soll (zwischen 0 und 1) """
    stil: BossLeisteStil
    """ Anzeige Stil der Leiste (siehe BossLeisteStil) """
    farbe: BossLeisteFarben
    """ Anzeige Farbe der Leiste (siehe BossLeisteFarbe) """

    def __repr__(self):
        return (f"BossLeiste(name={self.name}, "
                f"anzeige_text={self.anzeige_text}, "
                f"wert={self.wert:.2f}, "
                f"stil={self.stil}, "
                f"farbe={self.farbe})")


def _sende_boss_leiste_befehl(unter_befehl: str):
    # brauchen wir intern
    befehl = f"editBossBar {unter_befehl}"
    _sende_befehl(befehl)


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
    _sende_befehl(befehl)

    # einige der werte sind beim erzeugen festgesetzt.
    return BossLeiste(
        name=name,
        anzeige_text=anzeige_text,
        wert=0.0,
        stil=BossLeisteStil.DURCHGEZOGEN,
        farbe=BossLeisteFarben.LILA
    )

def setze_text(boss_leiste: BossLeiste, anzeige_text: str) -> BossLeiste:
    """ Setze den Text der Leiste """
    unter_befehl = f"text {boss_leiste.name} text:{_leerzeichen_behandel(anzeige_text)}"
    _sende_boss_leiste_befehl(unter_befehl)
    boss_leiste.anzeige_text = anzeige_text
    return boss_leiste


def setze_farbe(boss_leiste: BossLeiste, farbe: BossLeisteFarben) -> BossLeiste:
    """ Setze die Farbe der Leiste """
    unter_befehl = f"color {boss_leiste.name} color:{farbe.value}"
    _sende_boss_leiste_befehl(unter_befehl)
    boss_leiste.farbe = farbe
    return boss_leiste


def setze_wert(boss_leiste: BossLeiste, wert: float) -> BossLeiste:
    """ Setze zu welchem Anteil die leiste gefüllt sein soll (zwischen 0 und 1) """
    if not 0 <= wert <= 1:
        raise WertFehler(f"Der Wert der Bossleiste muss zwischen 0 und 1 liegen. Du hast '{wert}' angegeben.")

    unter_befehl = f"value {boss_leiste.name} value:{wert}"
    _sende_boss_leiste_befehl(unter_befehl)
    boss_leiste.wert = wert
    return boss_leiste


def setze_stil(boss_leiste: BossLeiste, stil: BossLeisteStil) -> BossLeiste:
    """ Setze den Stil der Leiste """
    unter_befehl = f"style {boss_leiste.name} color:{stil.value}"
    _sende_boss_leiste_befehl(unter_befehl)
    boss_leiste.stil = stil
    return BossLeiste

    
