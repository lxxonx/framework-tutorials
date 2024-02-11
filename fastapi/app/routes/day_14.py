import html
from fastapi import APIRouter, Body, Response


day_14_router = APIRouter(prefix="/14")


@day_14_router.post("/unsafe")
async def unsafe_serve(content: str = Body(..., embed=True)):
    template = f"""<html>
  <head>
    <title>CCH23 Day 14</title>
  </head>
  <body>
    {content}
  </body>
</html>"""
    return Response(content=template, media_type="text/html")


@day_14_router.post("/safe")
async def safe_serve(content: str = Body(..., embed=True)):
    content = html.escape(content)
    template = f"""<html>
  <head>
    <title>CCH23 Day 14</title>
  </head>
  <body>
    {content}
  </body>
</html>"""
    return Response(content=template, media_type="text/html")
