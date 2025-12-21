import st_minecraft.de as st_minecraft

st_minecraft.verbinden("localhost")

print("verbunden")

while True:
    spieler = st_minecraft.hole_spieler()

    st_minecraft.setze_block(spieler.x, spieler.y - 1, spieler.z, st_minecraft.MaterialSammlung.Stein)
    # time.sleep(0.1)
