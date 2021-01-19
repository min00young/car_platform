import re
from flask      import jsonify
from exceptions import ValidationError, LoginError
import json
class SuggestionService:
    def __init__(self, suggestion_dao, request_dao, database):
        self.suggestion_dao = suggestion_dao
        self.request_dao    = request_dao
        self.db             = database

    def modify_suggestion(self, args):
        try:
            connection = self.db.connect()
            trans = connection.begin()
            
            self.suggestion_dao.modify_suggestion(args, connection)

            trans.commit()
            return 'SUCCESS'
        
        except Exception as e:
            print(e)
            trans.rollback()
            return 'Database Rollback'

    def create_new_suggestion(self, request):
        try:
            connection = self.db.connect()
            trans = connection.begin()

            id = self.suggestion_dao.create(request, connection)
            
            trans.commit()
            return id

        except Exception as e:
            print(e)
            trans.rollback()
            return 'Database Rollback'

    def cancel_suggestion(self, pk):
        try:
            connection = self.db.connect()
            trans = connection.begin()

            request_id = self.suggestion_dao.cancel_suggestion(pk, connection)
            self.request_dao.cancel_request(request_id, connection)

            trans.commit()
            return 'SUCCESS'

        except Exception as e:
            print(e)
            trans.rollback()
            return 'Database Rollback'

    def get_my_suggestions_with_request(self, user_id, status):
        results = []
        # GET 내 제안
        suggestions = self.suggestion_dao.search({'user_id': user_id})
        # GET 요청ID IN 내 제안
        ids = [suggestion['request_id'] for suggestion in suggestions]
        # GET 요청 WITH 제안 수
        requests = self.request_dao.get_all_requests_with_suggestions_count()
        requests = [dict(request) for request in requests]
        # 요청 IN 내 제안
        my_requests = [request for request in requests if request['status'] == status and request['id'] in ids]
        # 요청의 제안 아이디 생성

        if not ids:
            raise ValidationError('제안한 요청이 없습니다')

        for i, request in enumerate(my_requests):
            request['suggestion_id'] = suggestions[i]['id']
            results.append(request)
        return results

    def get(self, pk):
        suggestion = self.suggestion_dao.get(pk)
        request = self.request_dao.get(suggestion['request_id'])
        suggestion['request'] = request
        del suggestion['request_id']
        return suggestion

