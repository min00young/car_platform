import json
from flask       import request, jsonify, session
from flask.views import MethodView

class SignupCompanyView(MethodView):
    def __init__(self, service):
        self.user_service = service

    def post(self):
        params = request.get_json()

        args = {}
        args['userid']          = params['userid']
        args['userpassword']    = params['userpassword']
        args['username']        = params['username']
        args['usernumber']      = params['usernumber']
        args['userposition']    = params['userposition']
        args['useremail']       = params['useremail']
        args['companyname']     = params['companyname']
        args['companyaddress1'] = params['companyaddress1']
        args['companyaddress2'] = params['companyaddress2']
        args['companycity']     = params['companycity']
        args['companystate']    = params['companystate']
        args['companyzipcode']  = params['companyzipcode']
        args['companyintro']    = params['companyintro']
        args['user_type_id']    = int(1)
        args['activation']      = True

        result = self.user_service.create_new_company(args)

        return jsonify({'message':result}), 200

class SignupEmployeeView(MethodView):
    def __init__(self, service):
        self.user_service = service

    def post(self):
        params = request.get_json()

        args = {}
        args['userid']       = params['userid']
        args['userpassword'] = params['userpassword']
        args['username']     = params['username']
        args['usernumber']   = params['usernumber']
        args['userposition'] = params['userposition']
        args['useremail']    = params['useremail']
        args['company_id']   = params['company_id']
        args['user_type_id'] = int(2)
        args['activation']   = True

        result = self.user_service.create_new_employee(args)

        return jsonify({'message':result}), 200

class CheckIdView(MethodView):
    def __init__(self, service):
        self.user_service = service

    def get(self,login_id):
        result = self.user_service.check_id(login_id)

        if result == True:
            return jsonify({'message':'SUCCESS'}), 200
        return jsonify({'message':'DUPLICATED_ID'}), 400

class LoginView(MethodView):
    def __init__(self, service):
        self.user_service = service

    def post(self):
        params = request.get_json()
        session['user'] = 1
        result = self.user_service.login(params['login_id'],params['password'])
        return jsonify(result), 200

