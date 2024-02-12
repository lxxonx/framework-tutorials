import enum


class CoordinateType(enum.Enum):
    LAT = "lat"
    LNG = "lng"


def print_dms(degree: float, type: CoordinateType = CoordinateType.LAT):
    if type == CoordinateType.LAT:
        hemisphere = "N" if degree >= 0 else "S"
    else:
        hemisphere = "E" if degree >= 0 else "W"
    mnt, sec = divmod(abs(degree) * 3600, 60)
    deg, mnt = divmod(mnt, 60)
    sec = round(sec, 3)
    return f"{int(deg)}°{int(mnt)}'{sec}''{hemisphere}"
