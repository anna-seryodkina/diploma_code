from flask import json
import requests


def test_1():
    response = requests.get("http://127.0.0.1:5000")
    assert response.status_code == 200
    

def test_login_with_valid_data():
    payload = {
        'email': 'testing@gmail.com',
        "password": '0987654321'
    }
    response = requests.post("http://127.0.0.1:5000/login", data=payload)
    assert response.status_code == 200


"""
def test_login_with_invalid_data():
    payload = {
        'email': 'ffff@gmail.com',
        "password": '1111111111'
    }
    response = requests.post("http://127.0.0.1:5000/login", data=payload)
    # assert response.status_code == 401

"""
