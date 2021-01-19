import config

from flask      import Flask, render_template
from sqlalchemy import create_engine, text
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from model   import UserDao, CompanyDao, RequestDao, CarDao, SuggestionDao
from service import UserService, CompanyService, RequestService, SuggestionService
from view    import create_endpoints

from exceptions import ValidationError, LoginError
from error_handler import (
    handle_key_error,
    handle_validation_error,
    handle_login_error
)

def create_app(test_config=None):
    class Services:
        pass

    app = Flask(__name__)

    CORS(app)

    app.config.from_pyfile("config.py")
    
    # 테스트 데이터 베이스 업데이트
    if test_config:
        app.config.update(test_config)
    database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = database
    # 에러 처리
    app.register_error_handler(KeyError, handle_key_error)
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(LoginError, handle_login_error)

    ## Persistenace Layer
    user_dao       = UserDao(database)
    company_dao    = CompanyDao(database)
    request_dao    = RequestDao(database)
    car_dao        = CarDao(database)
    suggestion_dao = SuggestionDao(database)

    ## Business Layer
    services = Services
    services.user_service       = UserService(user_dao, company_dao, config, database)
    services.company_service    = CompanyService(company_dao)
    services.request_service    = RequestService(request_dao, database)
    services.suggestion_service = SuggestionService(suggestion_dao, request_dao, database)

    ## 엔드포인트들을 생성
    create_endpoints(app, services)

    ## 채팅을 위한 socket생성
    socketio = SocketIO(app, cors_allowed_origins='*')

    @socketio.on('connect')
    def connect():
        print('Client connected')
        messages = database.execute("""
        SELECT *
        FROM chats
        """).fetchall()

        messages = [dict(message) for message in messages]
    
        for message in messages:
            message['created_at'] = str(message['created_at'])

        socketio.emit('message', messages)

    @socketio.on('send_message')
    def handle_message(message):
        request_id = message['request_id']
        name = message['name']
        text = message['text']

        try:
            connection = database.connect()
            trans = connection.begin()

            connection.execute("""
            INSERT INTO chats (
                request_id,
                name,
                text
            ) VALUES (
                %s,
                %s,
                %s
                )
            """, (request_id, name, text))

            trans.commit()

        except:
            trans.rollback()

        chat_messages = database.execute("""
        SELECT *
        FROM chats
        """).fetchall()

        messages = [dict(chat_message) for chat_message in chat_messages]
    
        for msg in messages:
            msg['created_at'] = str(msg['created_at'])

        socketio.emit('message', messages)

    return app

if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host='0.0.0.0', port='8000', debug=True)
