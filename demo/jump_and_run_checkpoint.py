import time
import sk_minecraft

sk_minecraft.verbinden("localhost", 12345)

checkpoint = None
gestartet = False
unterster_punkt = 0

while True:
    spieler = sk_minecraft.hole_spieler_koordinaten()

    block_unter_spieler = sk_minecraft.hole_block(spieler.x, spieler.y-1, spieler.z)
    # print(block_unter_spieler)

    if not gestartet and block_unter_spieler.typ == "OAK_LOG\n":
        gestartet = True
        unterster_punkt = spieler.y-1
        sk_minecraft.send_an_chat("Jump and run gestartet")
        checkpoint = spieler

    if checkpoint == None:
        continue
    
    if block_unter_spieler.typ == "STONE\n" and (checkpoint.x != spieler.x or checkpoint.y != spieler.y or checkpoint.z != spieler.z):
        checkpoint = spieler
        sk_minecraft.send_an_chat("Checkpoint gespeichert")


    if spieler.y < unterster_punkt:
        sk_minecraft.spieler_position_setzen(spieler, checkpoint.x, checkpoint.y, checkpoint.z)
    