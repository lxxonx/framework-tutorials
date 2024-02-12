from pydantic import BaseModel


class Star(BaseModel):
    x: int
    y: int
    z: int

    def get_distance(self, other_star: "Star") -> float:
        return (
            (self.x - other_star.x) ** 2
            + (self.y - other_star.y) ** 2
            + (self.z - other_star.z) ** 2
        ) ** 0.5
