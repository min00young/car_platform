import json
from flask      import request, jsonify
from flask.views    import MethodView

class CompanyListView(MethodView):
    def __init__(self, service):
        self.company_service = service

    def get(self):
        result = self.company_service.get_all_companies()
        return jsonify({'data':[dict(row) for row in result]})

class CompanyView(MethodView):
    def __init__(self, service):
        self.company_service = service

    def get(self, pk):
        result = self.company_service.get_company(pk)
        return jsonify({'data':dict(result)})
