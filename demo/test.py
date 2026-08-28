"""
this file aims to call nearly all functions at least once
there are not many assertions. it's more a "do we pass all signatures correctly" test
"""

# TODO: read chat is untested

import time

import st_minecraft.de as st_minecraft
import st_minecraft.de.boss_leiste as boss_bar
from st_minecraft.en import Dimension

st_minecraft.verbinden()

""" test title"""

st_minecraft.zeige_titel("Hallo Welt!")

"""test player getters"""

spieler = st_minecraft.hole_spieler()

spieler_durch_name = st_minecraft.hole_spieler_durch_name(spieler.name)

spieler_durch_index = st_minecraft.hole_spieler_durch_index(spieler.id)

assert spieler == spieler_durch_name

assert spieler == spieler_durch_index

""" test player positioning"""


st_minecraft.spieler_position_setzen(spieler, spieler.x, spieler.y + 20, spieler.z, dimension=Dimension.Nether)
st_minecraft.spieler_position_setzen(spieler, spieler.x, spieler.y + 20, spieler.z, dimension=Dimension.World)

""" test player attributes"""

st_minecraft.spieler_leben_setzen(spieler, 20)

st_minecraft.spieler_max_leben_setzten(spieler, 40)

st_minecraft.spieler_hunger_setzen(spieler, 20)

st_minecraft.spieler_xp_level_setzen(spieler, 10)

st_minecraft.spieler_xp_fortschritt_setzen(spieler, 0.5)

st_minecraft.spieler_geschwindigkeit_setzen(spieler, st_minecraft.RichtungSammlung.Hoch, 10)

"""
entity tests
"""

entity = st_minecraft.erzeuge_entity(spieler.x, spieler.y, spieler.z, st_minecraft.EntitySammlung.Kuh)
entity = st_minecraft.entity_name_setzen(entity, "Test")
entity = st_minecraft.entity_position_setzen(entity, entity.x, entity.y, entity.z)
print(entity.name)
entity = st_minecraft.entity_ai_setzen(entity, False)
entity = st_minecraft.entity_leben_setzen(entity, 1)

e2 = st_minecraft.hole_entity(entity)

assert entity.id == e2.id

assert entity == entity

assert entity == st_minecraft.EntitySammlung.Kuh

entity2 = st_minecraft.erzeuge_entity(spieler.x, spieler.y, spieler.z, st_minecraft.EntitySammlung.Schaf)

assert entity != entity2

"""
block tests
"""

for i in range(1, 10, 2):
    p = st_minecraft.hole_spieler()
    offset = i * 0.01
    st_minecraft.spieler_position_setzen(p, p.x + offset, p.y + offset, p.z + offset)
    st_minecraft.entity_position_setzen(entity, entity.x, entity.y + offset, entity.z)
    time.sleep(0.2)
print(p.x)

"""
float test
"""

b = st_minecraft.hole_block(0, 100.34, 0)
# test compare against type
if b == st_minecraft.MaterialSammlung.Goldblock:
    zu_setzen = st_minecraft.MaterialSammlung.Diamantblock
    alt = st_minecraft.MaterialSammlung.Goldblock
else:
    alt = st_minecraft.MaterialSammlung.Diamantblock
    zu_setzen = st_minecraft.MaterialSammlung.Goldblock

st_minecraft.setze_block(0, 100.5, 0, zu_setzen)
b2 = st_minecraft.hole_block(0, 100.9, 0)
if b2.typ == zu_setzen:
    st_minecraft.setze_block(0, 100, 0, alt)

# test block against block comparison
if b2 != b2:
    raise AssertionError("Block compare with self is broken!")

if b == b2:
    raise AssertionError("Block compare between two blocks is broken!")

"""
command test
"""

st_minecraft.sende_befehl("time set day")

"""
chat test
"""
st_minecraft.sende_an_chat("Test!")

"""inventory tests"""

st_minecraft.gebe_item(spieler, st_minecraft.MaterialSammlung.Holzspitzhacke, 1, name="Test")
inv = st_minecraft.hole_inventar(spieler)

print(inv)

print(inv[0])

"""
boss bar tests
"""

bb = boss_bar.erzeuge_leiste("test", "test")

boss_bar.setze_farbe(bb, boss_bar.BossLeisteFarben.PINK)

boss_bar.loesche_leiste(bb)


print(f"SUCCESS")
