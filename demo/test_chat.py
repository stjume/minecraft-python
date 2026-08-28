"""send "x" to chat and one more arbitrary message"""

import st_minecraft.de as st_minecraft

st_minecraft.verbinden()

st_minecraft.warte(2)
msgs = st_minecraft.hole_chat()
print(msgs)

assert msgs[0] == "x"
assert msgs[0] != "aaaa"

assert len(msgs) == 2
