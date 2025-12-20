import st_minecraft

st_minecraft.verbinden("localhost", 12345)

sneaked = False
jetpack = False
while True:
    spieler = st_minecraft.hole_spieler()

    if not spieler.sneaked and sneaked:
        block_unter_spieler = st_minecraft.hole_block(spieler.x, spieler.y - 1, spieler.z)
        if jetpack or block_unter_spieler.typ != st_minecraft.MaterialSammlung.Luft:
            st_minecraft.spieler_geschwindigkeit_setzen(spieler, st_minecraft.RichtungSammlung.Vorwärts, 3)

    sneaked = spieler.sneaked
