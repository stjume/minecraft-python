import sk_minecraft

sk_minecraft.verbinden("localhost", 12345)

spieler = sk_minecraft.hole_spieler()

size = 10
for x in range(size):
    for y in range(size):
        for z in range(size):
            sk_minecraft.hole_spieler()
            sk_minecraft.setze_block(
                spieler.x + x,
                spieler.y + y,
                spieler.z - size * 2 + z,
                sk_minecraft.MaterialSammlung.Stein,
            )
