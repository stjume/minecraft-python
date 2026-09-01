import st_minecraft.de as st
from st_minecraft.de import MaterialSammlung
from st_minecraft.de import RichtungSammlung
from st_minecraft.de import boss_leiste as boss

st.verbinden()


def block_unter_spieler(s):
    return st.hole_block(s.x, s.y - 1, s.z)


def countdown_boss_bar(sekunden: float, leise: bool = False):
    t = round(sekunden, 1)

    b = boss.erzeuge_leiste(COUNTDOWN_LEISTE, "Vorwärts Boost in...")
    b = boss.setze_wert(b, 1)
    b = boss.setze_farbe(b, boss.BossLeisteFarben.GELB)

    t_count = t
    schritt_größe = 1 / (t * 10)
    while t_count > 0:
        wert = b.wert - schritt_größe
        if wert < 0:
            wert = 0
        b = boss.setze_wert(b, wert)
        st.warte(0.1)
        t_count = t_count - 0.1

    boss.loesche_leiste(b)


COUNTDOWN_LEISTE = "countdown"

boss.loesche_leiste(
    boss.BossLeiste(
        name=COUNTDOWN_LEISTE,
        anzeige_text="",
        wert=0,
        farbe=boss.BossLeisteFarben.GELB,
        stil=boss.BossLeisteStil.DURCHGEZOGEN,
    )
)

spiel = 1

gewonnen = False  # wird auf True gesetzt, wenn Sieg kriterium erfüllt
while True:

    s = st.hole_spieler()
    # setze_ebene2(s.x, s.y-1, s.z, MaterialSammlung.Obsidian)
    # continue

    if s.schaut_auf == MaterialSammlung.Redstone_Block:
        print("REDSTONE")
        spiel = 1
        st.spieler_geschwindigkeit_setzen(s, RichtungSammlung.Hoch, 20)
        st.warte(0.1)

    if s.schaut_auf == MaterialSammlung.Diamantblock:
        print("DIAMANT")
        st.spieler_geschwindigkeit_setzen(s, RichtungSammlung.Hoch, 6)
        countdown_boss_bar(1.2)
        st.spieler_geschwindigkeit_setzen(s, RichtungSammlung.Vorwärts, 4)
        st.warte(0.1)

    if s.schaut_auf == MaterialSammlung.Goldblock:
        st.spieler_geschwindigkeit_setzen(s, RichtungSammlung.Vorwärts, 5)
        st.warte(0.1)

    # SPIEL 2

    if s.schaut_auf == MaterialSammlung.Orange_Wolle:
        spiel = 2
        print("ORANGE WOLLE")
        st.spieler_geschwindigkeit_setzen(s, RichtungSammlung.Hoch, 0.5)
        st.warte(0.1)

    # SPIEL 3

    if s.schaut_auf == MaterialSammlung.Hellblaue_Wolle:
        spiel = 3
        print("HELLBLAU")
        countdown_boss_bar(0.6)
        st.spieler_geschwindigkeit_setzen(s, RichtungSammlung.Vorwärts, 3)

    # SPIEL 4
    if s.schaut_auf == MaterialSammlung.Packeis:
        spiel = 4

    block = st.hole_block(s.x, s.y - 1, s.z)
    # schauen ob spieler:in auf zielhöhe ist
    if s.y > 80:
        # schauen ob spieler:in auf obsidian steht
        if block == MaterialSammlung.Obsidian:
            # wenn noch nicht gewonnen, text zeigen und gewonnen setzen
            if gewonnen == False:
                st.zeige_titel("GEWONNEN!", anzeige_zeit=1, ausblende_zeit=0.5)
                gewonnen = True

            # continue sorgt dafür, dass gewonnen = False hier drunter
            #  erst wieder auf false geht, wenn die sieg bedingungen nicht mehr gelten
            #  so wird der sieg text nur einmal angezeigt.
            continue

    gewonnen = False

    if block == MaterialSammlung.Grasblock:
        st.sende_befehl(f"kill {s.name}")
        while True:
            try:
                s = st.hole_spieler()
                b = block_unter_spieler(s)
                if b == MaterialSammlung.Grasblock:
                    st.warte(0.1)
                    continue
                break
            except Exception:
                continue
        st.warte(1)
        if spiel == 2:
            st.spieler_position_setzen(s, 54, -60, -53, rotation=-180)
        if spiel == 3:
            st.spieler_position_setzen(s, 28, -60, -53, rotation=-180)
        if spiel == 4:
            st.spieler_position_setzen(s, -42, -60, -17, rotation=-90)
        st.zeige_titel("Start!", einblende_zeit=0.1, anzeige_zeit=2, ausblende_zeit=0.5)
        print("START")
    st.warte(0.03)
