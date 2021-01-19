import json
from flask       import request, jsonify
from flask.views import MethodView

class RequestListView(MethodView):
    def __init__(self, service):
        self.request_service = service
    
    def post(self):
        params = request.get_json()

        args = {}

        args['phone_number']    = params['phone_number']
        args['state']           = params['state']
        args['city']            = params['city']
        args['car_number']      = params['car_number']
        args['car_id']          = params['car_id']
        args['additional_info'] = params['additional_info']

        request_id = self.request_service.create_new_request(args)

        return jsonify({'id':request_id}), 200

    def get(self):
        result = self.request_service.get_all_requests_with_suggestions_count()
        return jsonify({'requests':result})

class RequestView(MethodView):
    def __init__(self, service):
        self.request_service = service

    def patch(self, pk):
        params = request.get_json()

        args = {}

        args['status'] = params['status']
        args['request_id'] = pk

        result = self.request_service.request_completion(args)
        return jsonify({'message' : result})
    def get(self, pk):
        result = self.request_service.get_request(pk)
        return jsonify({'request' : result})

class CarListView(MethodView):
    def __init__(self, service):
        self.request_service = service

    def get(self):
        brand = request.args.get('brand')
        if brand:
            result = self.request_service.get_all_car_models(brand)
            return jsonify({'data':[dict(row) for row in result]})
            
        result = self.request_service.get_all_cars()
        return jsonify({'data':[dict(row) for row in result]})