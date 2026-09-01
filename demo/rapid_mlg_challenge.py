"""
if a specified player looks at a certain block the ground below them will be erased
after that they will receive a water bucket and have to do a MLG to save themselves

if they're still alive they get boosted up again
"""

import st_minecraft.de as st

st.verbinden()

# hier spielernamen wenn gewünscht eingeben, sonst wird der erste Spieler
#  auf dem server benutzt
SPIELER_NAME = None  # "jumebonn0"

BLOCK = st.MaterialSammlung.Melone


def countdown(sekunden: int = 10, leise: bool = False):
    for i in range(sekunden, 0, -1):
        if not leise:
            st.sende_an_chat(f"{i}")
        st.warte(1)


def fangen(p_name: str):

    run = 1
    while True:

        s = st.hole_spieler(name=p_name)

        # spieler einfrieren
        st.spieler_geschwindigkeit_setzen(s, st.RichtungSammlung.Runter, 0)
        st.spieler_geschwindigkeit_setzen(s, st.RichtungSammlung.Vorwärts, 0)
        st.spieler_geschwindigkeit_setzen(s, st.RichtungSammlung.Zurück, 0)

        höhe = s.y + run

        # wenn alle Blöche bis auf letzte Bedrock ebene gelöscht wurden
        if höhe < -63:
            st.gebe_item(s, st.MaterialSammlung.Wassereimer, 1, inventar_feld=0)
            print("FERTIG!")
            countdown(8)
            try:
                s = st.hole_spieler(name=p_name)
                setze_ebene(s.x, s.y, s.z)
                st.gebe_item(s, st.MaterialSammlung.Wassereimer, 1, inventar_feld=0)
                st.spieler_geschwindigkeit_setzen(s, st.RichtungSammlung.Hoch, 30)
                st.warte(1)
                st.spieler_geschwindigkeit_setzen(s, st.RichtungSammlung.Hoch, 30)
                st.warte(1)
                st.spieler_geschwindigkeit_setzen(s, st.RichtungSammlung.Hoch, 30)
                st.warte(1)
                st.spieler_geschwindigkeit_setzen(s, st.RichtungSammlung.Hoch, 30)
            except Exception:
                print("Cant get player up")
            break

        # Ebene löschen und die höhe um eins reduzieren
        setze_ebene(s.x, höhe, s.z)

        run = run - 1
        print(höhe)


def setze_ebene(x: float, y: float, z: float, material: st.MaterialSammlung = st.MaterialSammlung.Luft):
    for i in range(-2, 3):
        for j in range(-2, 3):
            st.setze_block(x - i, y, z - j, material)


if __name__ == "__main__":
    while True:
        if SPIELER_NAME:
            s_0 = st.hole_spieler(name=SPIELER_NAME)
        else:
            s_0 = st.hole_spieler()
        if s_0.schaut_auf == BLOCK:
            fangen(s_0.name)
