import json
from flask           import request, jsonify, current_app, g
from flask.views     import MethodView
from model           import UserDao
from utils.decorator import login_required

class SuggestionListView(MethodView):
    def __init__(self, service):
        self.suggestion_service = service

    @login_required
    def post(self):
        params = request.get_json()
        print(params)
        args = {}

        args['first_car_id']    = params['first_car_id']
        args['second_car_id']   = params['second_car_id']
        args['request_id']      = params['request_id']
        args['additional_info'] = params['additional_info']
        args['user_id']         = g.user_id

        id = self.suggestion_service.create_new_suggestion(args)
        return jsonify({'id': id}), 200

    @login_required
    def get(self):
        status = int(request.args.get('status',0))
        result = self.suggestion_service.get_my_suggestions_with_request(g.user_id, status)
        return jsonify({'data': result})

class SuggestionView(MethodView):
    def __init__(self, service):
        self.suggestion_service = service

    def get(self, pk):
        result = self.suggestion_service.get(pk)
        return jsonify({'suggestion': result})

    def patch(self, pk):
        params = request.get_json()

        args = {}

        args['first_car_id']    = params['first_car_id']
        args['second_car_id']   = params['second_car_id']
        args['additional_info'] = params['additional_info']
        args['suggestion_id']   = pk

        result = self.suggestion_service.modify_suggestion(args)
        return jsonify({'message': result}), 200

    def delete(self, pk):
        result = self.suggestion_service.cancel_suggestion(pk)
        return jsonify({'message' : result}), 200
