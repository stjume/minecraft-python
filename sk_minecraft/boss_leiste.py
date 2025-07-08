from sk_minecraft.kern import _leerzeichen_behandel, _sende_befehl
from sk_minecraft.daten_modelle import BossLeiste, WertFehler, BossLeisteFarben, BossLeisteStil


def _sende_befehl(unter_befehl: str):
    befehl = f"editBossBar {unter_befehl}"
    _sende_befehl(befehl)


def erzeuge_leiste(name: str, anzeige_text: str):
    befehl = f"spawnBossBar {name} {anzeige_text}"
    _sende_befehl(befehl)

    # einige der werte sind beim erzeugen festgesetzt.
    return BossLeiste(
        name=name,
        anzeige_text=anzeige_text,
        wert=0.0,
        stil=BossLeisteStil.DURCHGEZOGEN,
        color=BossLeisteFarben.LILA
    )

def setze_text(boss_leiste: BossLeiste, anzeige_text: str):
    unter_befehl = f"text {boss_leiste.name} text:{_leerzeichen_behandel(anzeige_text)}"
    _sende_befehl(unter_befehl)


def setze_farbe(boss_leiste: BossLeiste, farbe: BossLeisteFarben):
    unter_befehl = f"color {boss_leiste.name} color:{farbe.value}"
    _sende_befehl(unter_befehl)


def setze_wert(boss_leiste: BossLeiste, wert: float):
    """ setze zu welchem anteil die leiste gefüllt sein soll (zwischen 0 und 1) """
    if not 0 < wert <= 1:
        raise WertFehler(f"Der Wert der Bossleiste muss zwischen 0 und 1 liegen. Du hast '{wert}' angegeben.")

    unter_befehl = f"value {boss_leiste.name} value:{wert}"
    _sende_befehl(unter_befehl)


def setze_stil(boss_leiste: BossLeiste, stil: BossLeisteStil):
    unter_befehl = f"style {boss_leiste.name} color:{stil.value}"
    _sende_befehl(unter_befehl)
    
