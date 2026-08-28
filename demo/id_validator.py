import st_minecraft.de as mc
from st_minecraft.de.material import MaterialSammlung

mc.verbinden("192.168.3.102")

# with open("blocks_items.csv") as f:
#     names = csv.reader(f)
#     for row in names:
#         result = st_minecraft.validiere_id(row[1], "MATERIAL")
#         if result == "Yes":
#             print(",".join(row))

ms = MaterialSammlung._value2member_map_

print(ms)

p = mc.hole_spieler()

for e, v in ms.items():
    mc.setze_block(p.x, p.y, p.z, v)
    print(v)

print("Done")

mc.gebe_item(p, MaterialSammlung.Totem_der_Unsterblichkeit, 4, None, 2)

i = mc.hole_inventar(p)

print(i[1])
