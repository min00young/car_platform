from sqlalchemy import text

class CarDao:
    def __init__(self, database):
        self.db = database

    def all(self):
        rows = self.db.execute(text("""
        SELECT *
        FROM cars
        """)).fetchall()
        return [dict(row) for row in rows]

    def get(self, pk):
        row = self.db.execute(text("""
        SELECT *
        FROM cars
        WHERE id = :id
        """), {'id' : pk}).fetchone()
        return dict(row)
