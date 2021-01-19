# tests/test_main.py
import pytest
from datetime import datetime
import json
from sqlalchemy import text

from conftest import client, db

def test_cancel_suggestion_success(client, db):

    response = client.delete(
        '/suggestion/1'
    )

    assert response.status_code == 200

def test_modify_suggestion_success(client, db):
    request = {
        "first_car_id"  : 2,
        "second_car_id"  : 1,
        "additional_info": "hello world"
        }
    response = client.patch(
        '/suggestion/1',
        data=json.dumps(request),
        content_type='application/json'
    )
    assert response.status_code == 200
