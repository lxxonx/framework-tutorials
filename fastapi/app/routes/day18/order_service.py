from sqlite3 import Connection
from app.routes.day18.db.models import Order


class OrderService:
    def __init__(self, db: Connection):
        self.db = db

    def reset(self):
        self.db.execute("DROP TABLE IF EXISTS orders;")
        self.db.executescript(
            """
            CREATE TABLE orders (
                id INT PRIMARY KEY,
                region_id INT,
                gift_name VARCHAR(50),
                quantity INT
            );
            """
        )

    def create_many(self, orders: list[Order]):
        for order in orders:
            self.db.execute(
                "INSERT INTO orders (id, region_id, gift_name, quantity) VALUES (?, ?, ?, ?);",
                (order.id, order.region_id, order.gift_name, order.quantity),
            )

    def find_all(self) -> int | None:

        orders = self.db.execute(
            "SELECT * FROM orders;",
        )
        result = orders.fetchall()
        return result

    def get_total(self) -> int | None:

        orders_sum = self.db.execute(
            "SELECT SUM(orders.quantity) FROM orders;",
        )
        result = orders_sum.fetchone()
        if result:
            return result[0]
        return 0

    def get_popular_order(self) -> str | None:
        orders_sum = self.db.execute(
            "SELECT orders.gift_name FROM orders GROUP BY orders.gift_name ORDER BY SUM(orders.quantity) DESC LIMIT 1;",
        )
        result = orders_sum.fetchone()
        if result:
            return result[0]
        return None
