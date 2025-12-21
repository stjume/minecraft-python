import st_minecraft.de as st_minecraft

st_minecraft.verbinden("localhost", 12345)

spieler = st_minecraft.hole_spieler()

st_minecraft.spieler_leben_setzen(spieler, 20)

st_minecraft.spieler_max_leben_setzten(spieler, 40)

st_minecraft.spieler_hunger_setzen(spieler, 20)

st_minecraft.spieler_xp_level_setzen(spieler, 10)

st_minecraft.spieler_xp_fortschritt_setzen(spieler, 0.5)

entity = st_minecraft.erzeuge_entity(spieler.x, spieler.y, spieler.z, st_minecraft.EntitySammlung.Kuh)
entity = st_minecraft.entity_name_setzen(entity, "Test")
print(entity.name)
entity = st_minecraft.entity_ai_setzen(entity, False)

st_minecraft.gebe_item(spieler, st_minecraft.MaterialSammlung.Holzspitzhacke, 1, name="Test")
print(st_minecraft.hole_inventar(spieler))
