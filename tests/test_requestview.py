# tests/test_main.py
import pytest
from datetime import datetime
import json
from sqlalchemy import text

from conftest import client, db

def test_request_completion_success(client, db):

    request = {
        "status" : 3
        }

    response = client.patch(
        '/request/1',
        data=json.dumps(request),
        content_type='application/json'
    )

    assert response.status_code == 200

def test_request_completion_success(client, db):

    request = {
        "status" : 2
        }

    response = client.patch(
        '/request/1',
        data=json.dumps(request),
        content_type='application/json'
    )

    assert response.status_code == 200

def test_create_request_success(client, db):
    request = {
    "phone_number" : "010-5717-6080",
    "state"        : "California",
    "city"         : "LA",
    "car_number"   : "testcarnumber",
    "car_id"       : 1,
    "additional_info" : "additional_info"
    }
    response = client.post(
        '/request',
        data=json.dumps(request),
        content_type='application/json'
    )

    assert response.status_code == 200

def test_get_all_cars_success(client, db):
    response = client.get(
        '/car'
    )
    assert response.status_code == 200

def test_get_all_car_models_success(client, db):
    response = client.get(
        '/car?brand=현대'
    )
    assert response.status_code == 200

def test_request_list_success(client):
    response = client.get(
        '/request',
        content_type='application/json'
    )
    assert response.status_code == 200
    assert len(response.get_json()['requests']) > 1

def test_get_request_success(client, db):
    response = client.get(
        '/request/1',
        content_type='application/json'
    )
    assert response.status_code == 200
