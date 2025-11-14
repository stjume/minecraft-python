import sk_minecraft

sk_minecraft.verbinden("localhost", 12345)

print("verbunden")

while True:
    spieler = sk_minecraft.hole_spieler()

    sk_minecraft.setze_block(spieler.x, spieler.y - 1, spieler.z, sk_minecraft.MaterialSammlung.Stein)
    # time.sleep(0.1)
