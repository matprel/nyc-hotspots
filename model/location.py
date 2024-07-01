from dataclasses import dataclass


@dataclass
class Location:
    Location: str
    mLat: float
    mLon: float

    def __hash__(self):
        return hash(self.Location)

    def __str__(self):
        return self.Location