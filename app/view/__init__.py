from .company_view import (
    CompanyView,
    CompanyListView
)
from .user_view import (
    SignupCompanyView,
    SignupEmployeeView,
    CheckIdView,
    LoginView
)
from .request_view import (
    RequestListView,
    RequestView,
    CarListView,
)

from .suggestion_view import (
    SuggestionListView,
    SuggestionView
)

def create_endpoints(app, services):
    user_service       = services.user_service
    company_service    = services.company_service
    request_service    = services.request_service
    suggestion_service = services.suggestion_service

    # 회사검색
    app.add_url_rule('/company', view_func = CompanyListView.as_view('company_list_view', company_service), methods=['GET'])

    # 특정회사검색
    app.add_url_rule('/company/<int:pk>', view_func = CompanyView.as_view('company_view', company_service), methods=['GET'])

    # 회원가입(company)
    app.add_url_rule('/user/signup/company', view_func = SignupCompanyView.as_view('signupcompany_view', user_service), methods=['POST'])

    # 회원가입(employee)
    app.add_url_rule('/user/signup/employee', view_func = SignupEmployeeView.as_view('signupemployee_view', user_service), methods=['POST'])

    # 로그인
    app.add_url_rule('/user/login', view_func = LoginView.as_view('login_view', user_service), methods=['POST'])

    # 아이디체크
    app.add_url_rule('/user/check/id/<path:login_id>', view_func = CheckIdView.as_view('checkid_view', user_service), methods=['GET'])

    # 요청작성
    app.add_url_rule('/request', view_func = RequestListView.as_view('request_list_view', request_service), methods=['GET','POST'])

    # 차량검색
    app.add_url_rule('/car', view_func = CarListView.as_view('car_list_view', request_service), methods=['GET'])

    # 단일 요청 R,U,D
    app.add_url_rule('/request/<int:pk>', view_func = RequestView.as_view('request_view', request_service), methods=['GET', 'PUT', 'PATCH', 'DELETE'])

    # 제안 리스트 C, R
    app.add_url_rule('/suggestion', view_func = SuggestionListView.as_view('suggestion_list_view', suggestion_service), methods=['GET', 'POST'])

    # 제안 R, U, D
    app.add_url_rule('/suggestion/<int:pk>', view_func = SuggestionView.as_view('suggestion_view', suggestion_service), methods=['GET', 'PUT', 'PATCH', 'DELETE'])

