from sqlite3 import Connection
from app.routes.day18.db.models import Region
from app.routes.day18.order_service import OrderService


class RegionService:
    def __init__(self, db: Connection):
        self.db = db

    def reset(self):
        self.db.execute("DROP TABLE IF EXISTS regions;")
        self.db.executescript(
            """
            CREATE TABLE regions (
                id INT PRIMARY KEY,
                name VARCHAR(50)
            );
            """
        )

    def create_many(self, regions: list[Region]):
        for region in regions:
            self.db.execute(
                "INSERT INTO regions (id, name) VALUES (?, ?);",
                (region.id, region.name),
            )

    def find_all(self):
        regions = self.db.execute(
            "SELECT * FROM regions r ORDER BY r.name;",
        )
        result = regions.fetchall()
        return result

    def get_total(self):
        orders_sum = self.db.execute(
            "SELECT r.name as region, SUM(o.quantity) as total FROM orders o JOIN regions r ON o.region_id = r.id GROUP BY o.region_id ORDER BY r.name;",
        )
        result = orders_sum.fetchall()
        return result

    def get_top_list(self, limit: int):
        regions = self.find_all()
        result = []
        for region in regions:
            region_id = region[0]
            orders = self.db.execute(
                "SELECT orders.gift_name FROM orders WHERE orders.region_id = ? GROUP BY orders.gift_name ORDER BY SUM(orders.quantity) DESC, orders.gift_name ASC LIMIT ?;",
                (region_id, limit),
            )
            order_list = orders.fetchall()
            order_list = [order[0] for order in order_list]
            result.append((region[1], order_list))

        return result
