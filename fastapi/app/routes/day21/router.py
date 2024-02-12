from fastapi import APIRouter, Response
import s2sphere
from geopy.geocoders import Nominatim
from app.routes.day21.utils.country import get_country_from_country_code

from app.routes.day21.utils.dms import CoordinateType, print_dms

day_21_router = APIRouter(prefix="/21")


@day_21_router.get("/coords/{cell_id_str}")
async def get_coords(cell_id_str: str):
    cell_id = int(cell_id_str, 2)
    s2 = s2sphere.CellId(cell_id)

    latlng = s2.to_lat_lng()
    lat = print_dms(latlng.lat().degrees, CoordinateType.LAT)
    lng = print_dms(latlng.lng().degrees, CoordinateType.LNG)

    result = f"{lat} {lng}"

    return Response(status_code=200, content=result)


@day_21_router.get("/country/{cell_id_str}")
async def get_country_from_coords(cell_id_str: str):
    cell_id = int(cell_id_str, 2)
    s2 = s2sphere.CellId(cell_id)

    latlng = s2.to_lat_lng()
    lat = latlng.lat().degrees
    lng = latlng.lng().degrees

    geolocator = Nominatim(user_agent="geoapi")

    location = geolocator.reverse(str(lat) + "," + str(lng))

    address = location.raw["address"]

    country_code = address.get("country_code", "")
    country = get_country_from_country_code(country_code)

    return Response(status_code=200, content=country)
