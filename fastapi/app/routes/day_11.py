from fastapi import APIRouter, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image


static_router = StaticFiles(directory="app/assets")
day_11_router = APIRouter(prefix="/11")


def _calculate_formula(rgb_image: Image.Image):
    # red > blue + green
    count = 0
    for x in range(rgb_image.width):
        for y in range(rgb_image.height):
            r, g, b = rgb_image.getpixel((x, y))

            if r > b + g:
                count += 1

    return count


@day_11_router.post("/red_pixels")
async def red_pixels(
    image: UploadFile,
):
    image = Image.open(image.file)
    image = image.convert("RGB")

    count = _calculate_formula(image)
    return count
