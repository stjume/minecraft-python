import time
import sk_minecraft

sk_minecraft.verbinden("10.151.9.209", 12345)

print("verbunden")

while True:
    spieler = sk_minecraft.hole_spieler_koordinaten()
    print(spieler)


    sk_minecraft.setze_block(spieler.x, spieler.y-1, spieler.z, "stone")
    # time.sleep(0.1)