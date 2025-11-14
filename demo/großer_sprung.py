import sk_minecraft

sk_minecraft.verbinden("localhost", 12345)

sneaked = False
jetpack = False
while True:
    spieler = sk_minecraft.hole_spieler()

    if not spieler.sneaked and sneaked:
        block_unter_spieler = sk_minecraft.hole_block(spieler.x, spieler.y - 1, spieler.z)
        if jetpack or block_unter_spieler.typ != sk_minecraft.MaterialSammlung.Luft:
            sk_minecraft.spieler_geschwindigkeit_setzen(spieler, sk_minecraft.RichtungSammlung.Vorwärts, 3)

    sneaked = spieler.sneaked
