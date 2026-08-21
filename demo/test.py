import time

import st_minecraft.de as st_minecraft
from st_minecraft.en import Dimension

st_minecraft.verbinden()

st_minecraft.zeige_titel("Hallo Welt!")

spieler = st_minecraft.hole_spieler()

spieler_durch_name = st_minecraft.hole_spieler_durch_name(spieler.name)

spieler_durch_index = st_minecraft.hole_spieler_durch_index(spieler.id)

assert spieler == spieler_durch_name

assert spieler == spieler_durch_index

cmd = f"op {spieler.name}"
st_minecraft.sende_befehl(cmd)
print(cmd)


st_minecraft.spieler_position_setzen(spieler, spieler.x, spieler.y - 20, spieler.z, dimension=Dimension.Nether)
st_minecraft.spieler_position_setzen(spieler, spieler.x, spieler.y + 20, spieler.z, dimension=Dimension.World)

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


for i in range(1, 10, 2):
    p = st_minecraft.hole_spieler()
    offset = i * 0.01
    st_minecraft.spieler_position_setzen(p, p.x + offset, p.y + offset, p.z + offset)
    st_minecraft.entity_position_setzen(entity, entity.x, entity.y + offset, entity.z)
    time.sleep(0.2)
print(p.x)


b = st_minecraft.hole_block(0, 100.34, 0)
if b.typ == st_minecraft.MaterialSammlung.Goldblock:
    zu_setzen = st_minecraft.MaterialSammlung.Diamantblock
    alt = st_minecraft.MaterialSammlung.Goldblock
else:
    alt = st_minecraft.MaterialSammlung.Diamantblock
    zu_setzen = st_minecraft.MaterialSammlung.Goldblock

st_minecraft.setze_block(0, 100.5, 0, zu_setzen)
b = st_minecraft.hole_block(0, 100.9, 0)
if b.typ == zu_setzen:
    st_minecraft.setze_block(0, 100, 0, alt)

else:
    raise AssertionError("Set block doesnt match")

print(f"SUCCESS")
