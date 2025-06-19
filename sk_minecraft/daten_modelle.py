from pydantic import BaseModel

class Spieler(BaseModel):
    index: int
    name: str
    x: int
    y: int
    z: int

    @staticmethod
    def von_rohdaten(data: bytes) -> "Spieler":
        """ rohdaten sind index, name, x, y, z """
        index, name, x, y, z = data.decode("utf-8").split(" ")
        return Spieler(index=int(index), name=name, x=int(x), y=int(y), z=int(z))

    def __repr__(self):
        return f"Spieler(index={self.index}, name={self.name}, x={self.x}, y={self.y}, z={self.z})"