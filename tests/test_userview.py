# tests/test_main.py
import pytest
import bcrypt
import json
from sqlalchemy import text

from conftest import client, db

def test_signup_company_success(client, db):
    
    user = {
    "userid"          : "testmin",
    "userpassword"    : "test123!",
    "username"        : "testmin",
    "usernumber"      : "010-5717-6080",
    "userposition"    : "director",
    "useremail"       : "test@gmail.com",
    "companyname"     : "rencar",
    "companyaddress1" : "Pennsylvania Avenue",
    "companyaddress2" : "1600",
    "companycity"     : "NW",
    "companystate"    : "Washington",  
    "companyzipcode"  : "01456",  
    "companyintro"    : "hello world!"
}
    response = client.post(
        '/user/signup/company',
        data=json.dumps(user),
        content_type='application/json'
    )
    assert response.status_code == 200

def test_signup_employee_success(client, db):
    
    user = {
    "userid"       : "mintest",
    "userpassword" : "test124!",
    "username"     : "testemployee",
    "usernumber"   : "010-5717-6080",
    "userposition" : "designer",
    "useremail"    : "test@gmail.com",
    "company_id"   : 1
}
    response = client.post(
        '/user/signup/employee',
        data=json.dumps(user),
        content_type='application/json'
    )
    assert response.status_code == 200

def test_checkid_success(client, db):
    
    response = client.get(
        '/user/check/id/leetest'
    )
    assert response.status_code == 200

def test_checkid_fail(client, db):
    
    response = client.get(
        '/user/check/id/lee'
    )
    assert response.status_code == 400

def test_login_success(client, db):
    # 토큰 생성

    user = {
        'login_id': 'test_user',
        'password': '1q2w3e4r!',
        'user_type_id': 1,
        'activation': True
    }

    user['hashed_password'] = bcrypt.hashpw(user['password'].encode('utf-8'),bcrypt.gensalt())
    # db에 유저 넣기 
    sql = text("""
                    INSERT INTO users (
                        login_id,
                        password,
                        user_type_id,
                        activation
                    ) VALUES (
                        :login_id,
                        :hashed_password,
                        :user_type_id,
                        :activation
                    )
               """)

    with db.connect() as conn:
        conn.execute(sql,user)

    request = {
        'login_id': user['login_id'],
        'password': user['password']
    }
    response = client.post(
        '/user/login',
        data=json.dumps(request),
        content_type='application/json'
    )
    assert response.status_code == 200
