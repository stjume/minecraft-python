import csv

import st_minecraft.de as st_minecraft

st_minecraft.verbinden("localhost")

# with open("blocks_items.csv") as f:
#     names = csv.reader(f)
#     for row in names:
#         result = st_minecraft.validiere_id(row[1], "MATERIAL")
#         if result == "Yes":
#             print(",".join(row))

with open("entities.csv") as f:
    names = csv.reader(f)
    for row in names:
        result = st_minecraft._validiere_id(row[1], "ENTITY")
        if result == "Yes":
            print(",".join(row))
