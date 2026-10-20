"""
this file aims to call nearly all functions at least once
there are not many assertions. it's more a "do we pass all signatures correctly" test
"""

# TODO: read chat is untested
#  can be tested via test_chat.py

import time

import st_minecraft.de as st_minecraft
import st_minecraft.de as mc
import st_minecraft.de.boss_leiste as boss_bar
from st_minecraft.de import hole_alle_spieler
from st_minecraft.de import hole_alle_spieler_namen
from st_minecraft.de.material import MaterialSammlung
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

spieler_liste = hole_alle_spieler()

assert spieler_liste[0] == spieler

spieler_liste_namen = hole_alle_spieler_namen()

assert spieler_liste_namen[0] == spieler.name

spieler_liste = hole_alle_spieler()

assert spieler_liste[0] == spieler

spieler_liste_namen = hole_alle_spieler_namen()

assert spieler_liste_namen[0] == spieler.name

""" test player positioning"""


st_minecraft.spieler_position_setzen(spieler, spieler.x, spieler.y + 20, spieler.z, dimension=Dimension.Nether)
st_minecraft.spieler_position_setzen(spieler, spieler.x, spieler.y + 20, spieler.z, dimension=Dimension.World)

""" test player attributes"""

st_minecraft.spieler_max_leben_setzten(spieler, 60)

st_minecraft.spieler_leben_setzen(spieler, 65)


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
# test placing via entity as entity.type
entity3 = st_minecraft.erzeuge_entity(spieler.x, spieler.y, spieler.z, entity2)

assert entity != entity2

assert entity2.typ == entity3.typ

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
else:
    zu_setzen = st_minecraft.MaterialSammlung.Goldblock


st_minecraft.setze_block(0, 100.5, 0, zu_setzen)
b2 = st_minecraft.hole_block(0, 100.9, 0)
if b2.typ == zu_setzen:
    # reset by using type from old block, also tests if blocks can be used as block type
    st_minecraft.setze_block(0, 100, 0, b)

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
feld = spieler.hält_item.index
st_minecraft.gebe_item(
    spieler,
    st_minecraft.MaterialSammlung.Diamantaxt,
    2,
    name="test2",
    inventar_feld=feld,
)

spieler_neu = st_minecraft.hole_spieler_durch_name(spieler.name)

assert spieler_neu.hält_item == st_minecraft.MaterialSammlung.Diamantaxt

assert spieler.hält_item.index == feld

assert spieler_neu.hält_item.anzeige_name == "test2"

assert spieler_neu.hält_item.anzahl == 2

st_minecraft.gebe_item(spieler_neu, st_minecraft.MaterialSammlung.Luft, 1, inventar_feld=feld)


print(inv)

print(inv[0])

spieler = mc.hole_spieler()
gold_y = spieler.y - 10
mc.setze_block(spieler.x, gold_y, spieler.z, MaterialSammlung.Goldblock)

mc.warte(3)

spieler = mc.hole_spieler()
mc.spieler_position_setzen(spieler, *spieler.coords, rotation=0)

e = mc.erzeuge_entity(spieler.x, spieler.y + 1 - 0.5, spieler.z + 1, mc.EntitySammlung.Schaf)
entity = st_minecraft.entity_ai_setzen(e, False)

schaut_auf_block = MaterialSammlung.Redstone_Block
mc.setze_block(spieler.x, spieler.y + 1, spieler.z + 3, schaut_auf_block)


spieler_looks_at = mc.hole_spieler()

assert spieler_looks_at.schaut_auf_entity == e

assert spieler_looks_at.schaut_auf_block == schaut_auf_block

mc.entity_leben_setzen(e, 0)
mc.setze_block(spieler.x, spieler.y + 1, spieler.z + 3, MaterialSammlung.Luft)
mc.setze_block(spieler.x, gold_y, spieler.z, MaterialSammlung.Luft)

"""
boss bar tests
"""

bb = boss_bar.erzeuge_leiste("test", "test")

boss_bar.setze_farbe(bb, boss_bar.BossLeisteFarben.PINK)

boss_bar.lösche_leiste(bb)


print(f"SUCCESS")
