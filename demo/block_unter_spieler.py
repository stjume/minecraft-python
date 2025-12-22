import st_minecraft.de as mc

mc.verbinden("localhost")

while True:
    spieler = mc.hole_spieler()
    mc.setze_block(spieler.x, spieler.y - 1, spieler.z, mc.MaterialSammlung.Stein)
