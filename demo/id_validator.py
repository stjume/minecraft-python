import sk_minecraft
import csv

sk_minecraft.verbinden("localhost", 12345)

# with open("blocks_items.csv") as f:
#     names = csv.reader(f)
#     for row in names:
#         result = sk_minecraft.validiere_id(row[1], "MATERIAL")
#         if result == "Yes":
#             print(",".join(row))
        
with open("entities.csv") as f:
    names = csv.reader(f)
    for row in names:
        result = sk_minecraft.validiere_id(row[1], "ENTITY")
        if result == "Yes":
            print(",".join(row))