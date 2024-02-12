from collections import deque
from fastapi import APIRouter, Request, Response

from app.routes.day22.models import Star

day_22_router = APIRouter(prefix="/22")

PRESENT = "🎁"


@day_22_router.post("/integers")
async def day_22_integers(
    request: Request,
):
    body = await request.body()

    numbers = body.decode().split("\n")
    temp_array = []
    for number in numbers:
        if number in temp_array:
            temp_array.remove(number)
        else:
            temp_array.append(number)

    number_left = int("".join(temp_array))

    result = PRESENT * number_left

    return Response(content=result)


def bfs(graph, start, end):
    queue = []
    queue = deque([start])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == end:
            return path
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


@day_22_router.post("/rocket")
async def day_22_rocket(
    request: Request,
):
    body = await request.body()

    numbers = body.decode().split("\n")
    n = int(numbers[0])

    stars: list[Star] = []

    for star in numbers[1 : n + 1]:
        x, y, z = star.split(" ")

        x = int(x)
        y = int(y)
        z = int(z)
        s = Star(x=x, y=y, z=z)
        stars.append(s)

    k = int(numbers[n + 1])

    portals = {}
    for portal in numbers[n + 2 : n + 2 + k]:
        a, b = portal.split(" ")

        if a in portals:
            portals[a].add(b)
        else:
            portals[a] = set(b)
    print(portals)

    path = bfs(portals, "0", str(n - 1))
    print(path)
    total_distance = 0
    for i in range(len(path) - 1):
        dist = stars[int(path[i])].get_distance(stars[int(path[i + 1])])
        total_distance += dist

    result = f"{len(path)-1} {total_distance:.3f}"

    return Response(content=result)
