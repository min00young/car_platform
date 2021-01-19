
### flask 실행방법
```bash
# in 가상환경
export FLASK_APP=app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=8000
```

### config.py 예시
```python
DB = {
	'host': 'localhost', # DB IP
	'user': 'root',      # DB사용자
	'pass': 'password',  # 비밀번호
	'db': 'ims'     # DB 이름
}

DB_URL = f'mysql+mysqlconnector://{DB["user"]}:{DB["pass"]}@{DB["host"]}/{DB["db"]}?charset=utf8'

TEST_DB = 'test_ims'

TEST_DB_URL = f'mysql+mysqlconnector://{DB["user"]}:{DB["pass"]}@{DB["host"]}/{TEST_DB}?charset=utf8'

SECRET_KEY = 'secret_key'
JWT_ALGORITHM = 'jwt_algorithm'
```
