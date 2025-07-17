import datetime
import sk_minecraft

sk_minecraft.verbinden("localhost", 12345)

checkpoint = None
gestartet = False
unterster_punkt = 0

while True:
    spieler = sk_minecraft.hole_spieler()

    block_unter_spieler = sk_minecraft.hole_block(spieler.x, spieler.y-1, spieler.z)
    # print(block_unter_spieler)

    if not gestartet and block_unter_spieler.typ == sk_minecraft.MaterialSammlung.Eichenstamm:
        gestartet = True
        unterster_punkt = spieler.y-1
        sk_minecraft.sende_an_chat("Jump and run gestartet")
        checkpoint = spieler
        start = datetime.datetime.now()

    if checkpoint == None:
        continue
    
    if block_unter_spieler.typ == sk_minecraft.MaterialSammlung.Stein and (checkpoint.x != spieler.x or checkpoint.y != spieler.y or checkpoint.z != spieler.z):
        checkpoint = spieler
        sk_minecraft.sende_an_chat("Checkpoint gespeichert")

    if block_unter_spieler.typ == sk_minecraft.MaterialSammlung.Goldblock:
        zeit = datetime.datetime.now() - start
        m, s = divmod(zeit.seconds, 60)
        sk_minecraft.sende_an_chat(f"Fertig in {m} Minuten, {s} Sekunden")
        checkpoint = None
        gestartet = False

    if spieler.y < unterster_punkt:
        sk_minecraft.spieler_position_setzen(spieler, checkpoint.x, checkpoint.y, checkpoint.z)
    