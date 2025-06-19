import sk_minecraft

sk_minecraft.verbinden("131.220.6.219", 12345)

print("verbunden")

spieler = sk_minecraft.hole_spieler_koordinaten()
print(spieler)


sk_minecraft.setze_block(spieler.x, spieler.y-1, spieler.z, "stone")