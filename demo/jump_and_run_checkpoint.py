import datetime

import st_minecraft

st_minecraft.verbinden("localhost", 12345)

checkpoint = None
gestartet = False
unterster_punkt = 0

while True:
    spieler = st_minecraft.hole_spieler()

    block_unter_spieler = st_minecraft.hole_block(spieler.x, spieler.y - 1, spieler.z)
    # print(block_unter_spieler)

    if not gestartet and block_unter_spieler.typ == st_minecraft.MaterialSammlung.Eichenstamm:
        gestartet = True
        unterster_punkt = spieler.y - 1
        st_minecraft.sende_an_chat("Jump and run gestartet")
        checkpoint = spieler
        start = datetime.datetime.now()

    if checkpoint == None:
        continue

    if block_unter_spieler.typ == st_minecraft.MaterialSammlung.Stein and (
        checkpoint.x != spieler.x or checkpoint.y != spieler.y or checkpoint.z != spieler.z
    ):
        checkpoint = spieler
        st_minecraft.sende_an_chat("Checkpoint gespeichert")

    if block_unter_spieler.typ == st_minecraft.MaterialSammlung.Goldblock:
        zeit = datetime.datetime.now() - start
        m, s = divmod(zeit.seconds, 60)
        st_minecraft.sende_an_chat(f"Fertig in {m} Minuten, {s} Sekunden")
        checkpoint = None
        gestartet = False

    if spieler.y < unterster_punkt:
        st_minecraft.spieler_position_setzen(spieler, checkpoint.x, checkpoint.y, checkpoint.z)
