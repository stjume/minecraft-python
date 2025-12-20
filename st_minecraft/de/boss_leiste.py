"""Ermöglicht das erstellen und konfigurieren von Bossleisten"""

from enum import Enum

from pydantic import BaseModel

import st_minecraft.en as __st_minecraft_en
import st_minecraft.en.boss_bar as _st_minecraft_en_boss_bar
from st_minecraft.core.core import WertFehler


class BossLeisteStil(Enum):
    """Möglichkeiten in denen der Stil einer Bossleiste angezeigt werden kann"""

    DURCHGEZOGEN = "solid"
    SEGMENTE_6 = "segmented_6"
    SEGMENTE_10 = "segmented_10"
    SEGMENTE_12 = "segmented_12"
    SEGMENTE_20 = "segmented_20"

    @staticmethod
    def von_englisch(boss_bar_stil: _st_minecraft_en_boss_bar.BossBarStyle) -> "BossLeisteStil":
        return BossLeisteStil._value2member_map_[boss_bar_stil.value]

    def zu_englisch(self) -> _st_minecraft_en_boss_bar.BossBarStyle:
        return _st_minecraft_en_boss_bar.BossBarStyle._value2member_map_[self.value]


class BossLeisteFarben(Enum):
    """Farben in denen eine Bossleiste angezeigt werden kann"""

    BLAU = "blue"
    GRÜN = "green"
    PINK = "pink"
    LILA = "purple"
    ROT = "red"
    WEIß = "white"
    GELB = "yellow"

    @staticmethod
    def von_englisch(boss_bar_farbe: _st_minecraft_en_boss_bar.BossBarColor) -> "BossLeisteFarben":
        return BossLeisteFarben._value2member_map_[boss_bar_farbe.value]

    def zu_englisch(self) -> _st_minecraft_en_boss_bar.BossBarColor:
        return _st_minecraft_en_boss_bar.BossBarColor._value2member_map_[self.value]


class BossLeiste(BaseModel):
    """Modell einer Bossleiste"""

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
        return (
            f"BossLeiste(name={self.name}, "
            f"anzeige_text={self.anzeige_text}, "
            f"wert={self.wert:.2f}, "
            f"stil={self.stil}, "
            f"farbe={self.farbe})"
        )

    @staticmethod
    def von_englisch(boss_bar: _st_minecraft_en_boss_bar.BossBar) -> "BossLeiste":
        return BossLeiste(
            name=boss_bar.name,
            anzeige_text=boss_bar.display_text,
            wert=boss_bar.value,
            stil=BossLeisteStil.von_englisch(boss_bar.style),
            farbe=BossLeisteFarben.von_englisch(boss_bar.color),
        )

    def zu_englisch(self) -> _st_minecraft_en_boss_bar.BossBar:
        return _st_minecraft_en_boss_bar.BossBar(
            name=self.name,
            display_text=self.anzeige_text,
            value=self.wert,
            style=self.stil.zu_englisch(),
            color=self.farbe.zu_englisch(),
        )


def erzeuge_leiste(name: str, anzeige_text: str) -> BossLeiste:
    """
    Erstelle eine Bossleiste
    Args:
        name: Ein von dir gewählter Name, wie die Bossleiste für dich heißen soll
        anzeige_text: Text der an der Leiste angezeigt werden soll

    Returns:
        Ein BossLeisten Objekt mit dessen Hilfe du die Leiste weiter konfigurieren kannst
    """
    b = __st_minecraft_en.create_bar(name, anzeige_text)
    return BossLeiste.von_englisch(b)


def setze_text(boss_leiste: BossLeiste, anzeige_text: str) -> BossLeiste:
    """Setze den Text der Leiste"""
    b = __st_minecraft_en.set_text(boss_leiste.zu_englisch(), anzeige_text)
    return BossLeiste.von_englisch(b)


def setze_farbe(boss_leiste: BossLeiste, farbe: BossLeisteFarben) -> BossLeiste:
    """Setze die Farbe der Leiste"""
    b = __st_minecraft_en.set_color(boss_leiste.zu_englisch(), farbe.zu_englisch())
    return BossLeiste.von_englisch(b)


def setze_wert(boss_leiste: BossLeiste, wert: float) -> BossLeiste:
    """Setze zu welchem Anteil die leiste gefüllt sein soll (zwischen 0 und 1)"""
    if not 0 <= wert <= 1:
        raise WertFehler(f"Der Wert der Bossleiste muss zwischen 0 und 1 liegen. Du hast '{wert}' angegeben.")

    b = __st_minecraft_en.set_value(boss_leiste.zu_englisch(), wert)
    return BossLeiste.von_englisch(b)


def setze_stil(boss_leiste: BossLeiste, stil: BossLeisteStil) -> BossLeiste:
    """Setze den Stil der Leiste"""
    b = __st_minecraft_en.set_style(boss_leiste.zu_englisch(), stil.zu_englisch())
    return BossLeiste.von_englisch(b)


def loesche_leiste(boss_leiste: BossLeiste):
    """Lösche eine Leiste"""
    __st_minecraft_en.delete_bar(boss_leiste.zu_englisch())
