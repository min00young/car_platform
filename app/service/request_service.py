import re
from flask      import jsonify
from exceptions import ValidationError, LoginError
import json
class RequestService:
    def __init__(self, request_dao, database):       
        self.request_dao = request_dao
        self.db          = database
        
    def create_new_request(self, new_request):
        #핸드폰번호 유효성검사(2,3자리 - 3,4자리 - 4자리)
        phone_validation = re.compile(r'\d{2,3}-\d{3,4}-\d{4}')
        if not re.match(phone_validation, new_request['phone_number']):
            raise ValidationError('PHONE_NUMBER')
        try:
            connection = self.db.connect()
            trans = connection.begin()

            id = self.request_dao.create_request(new_request, connection)

            trans.commit()
            return id

        except Exception as e:
            print(e)
            trans.rollback()
            return 'Database Rollback'

    def get_request(self, pk):
        request = self.request_dao.get(pk)
        return request

    def get_all_requests(self):
        requests = self.request_dao.get_all_requests()
        return requests
 
    def get_all_cars(self):
        cars = self.request_dao.get_all_cars()
        return cars

    def get_all_car_models(self, brand):
        car_models = self.request_dao.get_all_car_models(brand)
        return car_models

    def get_all_requests_with_suggestions_count(self):
        requests = self.request_dao.get_all_requests_with_suggestions_count()
        return [dict(request) for request in requests]

    def request_completion(self, args):

        # 배차완료 (request drived_at)
        if args['status'] == 2:
            try:
                connection = self.db.connect()
                trans = connection.begin()

                result = self.request_dao.request_driveout(args, connection)

                trans.commit()
                return result

            except Exception as e:
                print(e)
                trans.rollback()
                return 'Database Rollback'

        # 반납완료 (request checkout_date)
        elif args['status'] == 3:
            try:
                connection = self.db.connect()
                trans = connection.begin()

                result = self.request_dao.request_checkout(args, connection)

                trans.commit()
                return result

            except Exception as e:
                print(e)
                trans.rollback()
                return 'Database Rollback'
