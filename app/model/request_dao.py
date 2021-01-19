from sqlalchemy import text
import datetime

class RequestDao:
    def __init__(self, database):
        self.db = database

    def create_request(self, request, connection):
        id = connection.execute(text("""
        INSERT INTO requests (
            phone_number,
            state,
            city,
            car_number,
            car_id,
            additional_info
        ) VALUES (
            :phone_number,
            :state,
            :city,
            :car_number,
            :car_id,
            :additional_info
        )
        """), request).lastrowid
        return id

    def get_all_requests(self):
        rows = self.db.execute(text("""
        SELECT
        id,
        car_id,
        car_number,
        created_at,
        drive_date,
        checkout_date,
        status
        FROM requests
        """)).fetchall()
        return rows

    def get_all_cars(self):
        rows = self.db.execute(text("""
        SELECT DISTINCT
        brand
        FROM cars
        """)).fetchall()
        return rows

    def get_all_car_models(self, brand):
        rows = self.db.execute(text("""
        SELECT
        id,
        model
        FROM cars
        WHERE brand = :brand
        """), {'brand' : brand}).fetchall()
        return rows

    def get_all_requests_with_suggestions_count(self):
        rows = self.db.execute(text(f"""
            SELECT
                requests.id,
                requests.car_number,
                requests.status,
                DATE_FORMAT(requests.drive_date,'%Y-%m-%d') as drive_date,
                DATE_FORMAT(requests.checkout_date,'%Y-%m-%d') as checkout_date,
                DATE_FORMAT(requests.created_at,'%Y-%m-%d') as created_at,
                cars.brand as cars_brand,
                cars.model as cars_model,
                count(suggestions.id) as suggestions_count
            FROM requests 
            LEFT JOIN suggestions ON requests.id=suggestions.request_id
            LEFT JOIN cars ON requests.car_id=cars.id
            GROUP BY requests.id;
        """)).fetchall()
        return rows

    def request_checkout(self, args, connection):
        now = datetime.datetime.now()
        now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

        connection.execute(text("""
        UPDATE requests
        SET status = 3, checkout_date =:datetime
        WHERE id=:id
        """),{'id': args['request_id'], 'datetime' : now_datetime})

        return 'SUCCESS'

    def request_driveout(self, args, connection):
        now = datetime.datetime.now()
        now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

        connection.execute(text("""
        UPDATE requests
        SET status = 2, drive_date =:datetime
        WHERE id=:id
        """),{'id': args['request_id'], 'datetime' : now_datetime})

        return 'SUCCESS'

    def cancel_request(self, request_id, connection):
        connection.execute(text("""
        UPDATE requests
        SET status = 0
        WHERE id=:id
        """),{'id': request_id})

        return 'SUCCESS'

    def get(self, pk):
        row = self.db.execute(text("""
        SELECT
            id,
            car_id,
            car_number,
            phone_number,
            state,
            city,
            additional_info,
            DATE_FORMAT(drive_date,'%Y-%m-%d') as drive_date,
            DATE_FORMAT(checkout_date,'%Y-%m-%d') as checkout_date, 
            status,
            DATE_FORMAT(created_at,'%Y-%m-%d') as created_at,
            DATE_FORMAT(removed_at,'%Y-%m-%d') as removed_at
        FROM requests
        WHERE id=:id
        """),{'id': pk}).fetchone()
        request = dict(row)

        # 차량 정보 받아오기
        row = self.db.execute(text("""
        SELECT 
            id,
            brand,
            model
        FROM cars WHERE id=:id
        """),{'id': request['car_id']}).fetchone()

        request['car'] = dict(row)
        del request['car_id']

        return request

