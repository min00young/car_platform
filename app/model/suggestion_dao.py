from sqlalchemy import text
import datetime

class SuggestionDao:
    def __init__(self, database):
        self.db = database

    def modify_suggestion(self, args, connection):

        connection.execute(text("""
        UPDATE suggestions
        SET first_car_id =:first_car_id, second_car_id =:second_car_id, additional_info =:additional_info
        WHERE id=:suggestion_id
        """), args)

        return 'SUCCESS'

    def cancel_suggestion(self, pk, connection):
        now = datetime.datetime.now()
        now_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

        connection.execute(text("""
        UPDATE suggestions
        SET removed_at =:datetime
        WHERE id=:id
        """),{'id': pk, 'datetime' : now_datetime})

        result = connection.execute(text("""
        SELECT request_id 
        FROM suggestions
        WHERE id=:id
        """), {'id': pk}).fetchone()[0]

        return result
    def create(self, request, connection):

        field_string = ','.join(request.keys())
        value_string = ','.join([f':{i}' for i in request.keys()])

        id = connection.execute(text(f"""
        INSERT INTO suggestions (
            {field_string}
        ) VALUES (
            {value_string}
        )
        """), request).lastrowid
        return id

    def search(self, condition=None):
        condition_sql = ''
        if not condition == None:
            condition_sql = 'WHERE ' + ' AND '.join([f'{k}={v}' for k, v in condition.items()])

        suggestions = self.db.execute(text(f"""
        SELECT * FROM suggestions
        {condition_sql}
        """))
        print(suggestions)
        return [dict(row) for row in suggestions]

    def get(self, condition=None):
        condition_sql = ''
        if not condition == None:
            condition_sql = 'WHERE ' + ' AND '.join([f'{k}={v}' for k, v in condition.items()])

        suggestions = self.db.execute(text(f"""
        SELECT * FROM suggestions
        {condition_sql}
        """))

        return [dict(row) for row in suggestions]

    def get(self, pk):
        row = self.db.execute(text("""
        SELECT
            id,
            request_id,
            first_car_id,
            second_car_id,
            additional_info,
            DATE_FORMAT(created_at,'%Y-%m-%d') as created_at
        FROM suggestions
        WHERE id=:id
        """),{'id': pk}).fetchone()
        suggestion = dict(row)

        # 차량 정보 받아오기
        rows = self.db.execute(text("""
        SELECT 
            id,
            brand,
            model
            FROM cars WHERE id IN (:id1, :id2)
        """),{'id1': suggestion['first_car_id'],
              'id2': suggestion['second_car_id']
             }).fetchall()

        car = [dict(row) for row in rows]
        print(f'\n\n\n{car}\n\n\n')
        suggestion['first_car'] = car[0]

        if len(car) > 1:
            suggestion['second_car'] = car[1]
        else:
            suggestion['second_car'] = None

        del suggestion['first_car_id']
        del suggestion['second_car_id']

        return suggestion
