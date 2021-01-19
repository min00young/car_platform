import pytest
import jwt

from app        import create_app
from sqlalchemy import create_engine, text

import config

TEST_CONFIG = {
    'TESTING': True,
    'DB_URL': config.TEST_DB_URL
}

def generate_token(id):
    token = jwt.encode({'id': id}, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM).decode('utf-8')
    return {'Authorization': token}

def db_file(db, filename):
    sql_lines = []
    with open(filename, 'r') as file_data:
        sql_lines = [line.strip('\n') for line in file_data if not line.startswith('--') and line.strip('\n')]

    with db.connect() as conn:
        with conn.begin() as tran:
            sql_command = ''

            for line in sql_lines:
                sql_command += line
                if sql_command.endswith(';'):
                    try:
                        conn.execute(text(sql_command))
                    except Exception as e:
                        tran.rollback()
                        print('Fail DB Reset!!')
                        print(e)
                        return False
                    finally:
                        sql_command = ''
    return True

@pytest.fixture(scope='session')
def app():
    return create_app(TEST_CONFIG)

@pytest.fixture(scope='session')
def db():
    db = create_engine(TEST_CONFIG['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    return db

@pytest.fixture
def client(app, db):
    client = app.test_client()

    # db init
    if not db_file(db, 'tests/schema.sql'):
        raise ValueError('테이블 생성 실패!')
    if not db_file(db, 'tests/insertion.sql'):
        raise ValueError('초기데이터 넣기 실패!')

    return client

