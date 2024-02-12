from fastapi import APIRouter, Response
import s2sphere

from app.routes.day21.utils.dms import CoordinateType, print_dms

day_21_router = APIRouter(prefix="/21")


@day_21_router.get("/coords/{cell_id_str}")
async def get_coords(cell_id_str: str):
    cell_id = int(cell_id_str, 2)
    s2 = s2sphere.CellId(cell_id)

    latlng = s2.to_lat_lng()
    lat = print_dms(latlng.lat().degrees, CoordinateType.LAT)
    lng = print_dms(latlng.lng().degrees, CoordinateType.LNG)

    print(lat, lng)
    result = f"{lat} {lng}"

    return Response(status_code=200, content=result)
