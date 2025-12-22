import datetime
import time

import st_minecraft.de as st_minecraft
import st_minecraft.de.boss_leiste as boss

st_minecraft.verbinden("localhost")

checkpoint = None
gestartet = False
unterster_punkt = 0

while True:
    spieler = st_minecraft.hole_spieler()

    block_unter_spieler = st_minecraft.hole_block(spieler.x, spieler.y - 1, spieler.z)
    # print(block_unter_spieler)

    if not gestartet and block_unter_spieler.typ == st_minecraft.MaterialSammlung.Smaragdblock:
        gestartet = True
        unterster_punkt = spieler.y - 1
        st_minecraft.sende_an_chat("Jump and run gestartet")
        checkpoint = spieler
        start = datetime.datetime.now()

    if checkpoint == None:
        continue

    if block_unter_spieler.typ == st_minecraft.MaterialSammlung.Goldblock and (
        checkpoint.x != spieler.x or checkpoint.y != spieler.y or checkpoint.z != spieler.z
    ):
        checkpoint = spieler
        st_minecraft.sende_an_chat("Checkpoint gespeichert")

    if block_unter_spieler.typ == st_minecraft.MaterialSammlung.Diamantblock:
        zeit = datetime.datetime.now() - start
        m, s = divmod(zeit.seconds, 60)
        st_minecraft.sende_an_chat(f"Fertig in {m} Minuten, {s} Sekunden")
        checkpoint = None
        gestartet = False

        b = boss.erzeuge_leiste("bar", "Krasse Leistung")

        boss.setze_farbe(b, boss.BossLeisteFarben.BLAU)

        for i in reversed(range(0, 100)):
            boss.setze_wert(b, i / 100)
            time.sleep(0.05)

        boss.loesche_leiste(b)

    if spieler.y < unterster_punkt:
        st_minecraft.spieler_position_setzen(spieler, checkpoint.x, checkpoint.y, checkpoint.z)
        if spieler.max_leben < 3:
            st_minecraft.sende_an_chat("Game Over")
            checkpoint = None
            gestartet = False
            st_minecraft.spieler_max_leben_setzten(spieler, 20)
            st_minecraft.spieler_leben_setzen(spieler, 20)
            continue

        st_minecraft.spieler_max_leben_setzten(spieler, spieler.max_leben - 2)
