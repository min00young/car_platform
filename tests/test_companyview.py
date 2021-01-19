import pytest

from conftest import client, db

def test_get_company_success(client, db):
    
    response = client.get(
        '/company/2'
    )
    assert response.status_code == 200

def test_get_all_companies_success(client, db):
    
    response = client.get(
        '/company'
    )
    assert response.status_code == 200