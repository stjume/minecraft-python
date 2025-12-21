import st_minecraft.de as st_minecraft

st_minecraft.verbinden("localhost")

spieler = st_minecraft.hole_spieler()

size = 10
for x in range(size):
    for y in range(size):
        for z in range(size):
            st_minecraft.hole_spieler()
            st_minecraft.setze_block(
                spieler.x + x,
                spieler.y + y,
                spieler.z - size * 2 + z,
                st_minecraft.MaterialSammlung.Stein,
            )
