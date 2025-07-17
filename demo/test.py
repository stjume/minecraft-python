import datetime
import sk_minecraft

sk_minecraft.verbinden("localhost", 12345)

spieler = sk_minecraft.hole_spieler()

sk_minecraft.spieler_leben_setzen(spieler, 5)

sk_minecraft.spieler_max_leben_setzten(spieler, 10)

sk_minecraft.spieler_hunger_setzen(spieler, 20)

sk_minecraft.spieler_xp_level_setzen(spieler, 10);

sk_minecraft.spieler_xp_fortschritt_setzen(spieler, 0.5)

entity = sk_minecraft.erzeuge_entity(spieler.x, spieler.y, spieler.z, sk_minecraft.EntitySammlung.Kuh)
entity = sk_minecraft.entity_name_setzen(entity, "Test")
print(entity.name)
entity = sk_minecraft.entity_ai_setzen(entity, False)

sk_minecraft.gebe_item(spieler, sk_minecraft.MaterialSammlung.Holzspitzhacke, 1, name="Test")
print(sk_minecraft.hole_inventar(spieler))