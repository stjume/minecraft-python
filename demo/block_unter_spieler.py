import st_minecraft

st_minecraft.connect("localhost", 12345)

print("verbunden")

while True:
    spieler = st_minecraft.hole_spieler()

    st_minecraft.setze_block(spieler.x, spieler.y - 1, spieler.z, st_minecraft.MaterialSammlung.Stein)
    # time.sleep(0.1)
