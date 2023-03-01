import os
import pytest
from dotenv import load_dotenv
from connexion import RestyResolver

load_dotenv()

from app import db, create_app

###################### SETUP ######################
@pytest.fixture(scope='module')
def app():
    os.environ['ENV'] = 'test'
    connex_app = create_app()
    connex_app.add_api('../api_spec.yml', resolver=RestyResolver('app.controllers'))
    app = connex_app.app

    with app.app_context() as context:
        context.push()
        db.create_all()
        yield app

    db.drop_all()

@pytest.fixture(scope='function')
def empty_payload():
    return {
        "firstname": "",
        "lastname": "",
        "email": "",
        "phonenumber": "",
        "password": ""
    }

@pytest.fixture(scope='function')
def valid_payload():
    return {
        "firstname": "John",
        "lastname": "Doe",
        "email": "johndoe@gmail.com",
        "phonenumber": "09012348765",
        "password": "$Password1"
    }

user_fields = ['firstname', 'lastname', 'email', 'phonenumber']
###################### SETUP ######################

###################### TESTS ######################
def test_create_user__no_payload(app):
    '''
    GIVEN no user payload
    WHEN an HTTP POST call is made to /api/v1/users
    THEN check that a 400 is returned
    '''
    res = app.test_client().post('/api/v1/users', json={})

    assert res.status_code == 400
    assert res.json['success'] == False
    assert res.json['error']['firstname'][0] == 'firstname is required'
    assert res.json['error']['lastname'][0] == 'lastname is required'
    assert res.json['error']['email'][0] == 'email is required'
    assert res.json['error']['phonenumber'][0] == 'phonenumber is required'
    assert res.json['error']['password'][0] == 'password is required'

def test_create_user__empty_payload(app, empty_payload):
    '''
    GIVEN an empty user payload
    WHEN an HTTP POST call is made to /api/v1/users
    THEN check that a 400 is returned
    '''
    res = app.test_client().post('/api/v1/users', json=empty_payload)

    assert res.status_code == 400
    assert res.json['success'] == False
    assert res.json['error']['firstname'][0] == 'firstname cannot be empty'
    assert res.json['error']['lastname'][0] == 'lastname cannot be empty'
    assert res.json['error']['phonenumber'][0] == 'phonenumber cannot be empty'
    assert res.json['error']['password'][0] == 'password cannot be empty'
    assert 'Not a valid email address' in res.json['error']['email'][0]

def test_create_user__invalid_email(app, valid_payload):
    '''
    GIVEN a valid user payload with invalid email
    WHEN an HTTP POST call is made to /api/v1/users
    THEN check that a 400 is returned
    '''
    valid_payload['email'] = 'invalid@gmail'
    res = app.test_client().post('/api/v1/users', json=valid_payload)

    assert res.status_code == 400
    assert res.json['success'] == False
    assert 'Not a valid email address' in res.json['error']['email'][0]

def test_create_user__invalid_password_length(app, valid_payload):
    '''
    GIVEN a valid user payload with invalid password length
    WHEN an HTTP POST call is made to /api/v1/users
    THEN check that a 400 is returned
    '''
    valid_payload['password'] = '123$Abc'
    res = app.test_client().post('/api/v1/users', json=valid_payload)

    assert res.status_code == 400
    assert res.json['success'] == False
    assert res.json['error']['password'][0] == 'password must be at least 8 characters long'

def test_create_user__invalid_password_pattern(app, valid_payload):
    '''
    GIVEN a valid user payload with invalid password pattern
    WHEN an HTTP POST call is made to /api/v1/users
    THEN check that a 400 is returned
    '''
    valid_payload['password'] = '12345abcdE'
    res = app.test_client().post('/api/v1/users', json=valid_payload)

    assert res.status_code == 400
    assert res.json['success'] == False
    assert res.json['error']['password'][0] == 'password must have at least a lowercase letter, an uppercase letter, a number, and a special character'
###################### TESTS ######################
