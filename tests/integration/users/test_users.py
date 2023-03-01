import os
import pytest
import logging
from dotenv import load_dotenv
from connexion import RestyResolver

load_dotenv()

from app import db, create_app
from tests.utils import check_fields_same

###################### SETUP ######################
@pytest.fixture(scope='module')
def app():
    os.environ['ENV'] = 'test'
    os.environ['APP_NAME'] = 'Now Transact Test'
    connex_app = create_app()
    connex_app.add_api('../api_spec.yml', resolver=RestyResolver('app.controllers'))
    app = connex_app.app
    app.logger.disabled = True # remember to comment in pipeline

    with app.app_context() as context:
        context.push()
        db.create_all()
        yield app

    db.drop_all()

@pytest.fixture(scope='function')
def payload_1():
    return {
        "firstname": "John",
        "lastname": "Doe",
        "email": "johndoe@gmail.com",
        "phonenumber": "09012348765",
        "password": "$Password1"
    }

@pytest.fixture(scope='function')
def payload_2():
    return {
        "firstname": "Jane",
        "lastname": "Doe",
        "email": "janedoe@gmail.com",
        "phonenumber": "09087651234",
        "password": "$Password1"
    }

user_fields = ['firstname', 'lastname', 'email', 'phonenumber']
###################### SETUP ######################


###################### TESTS ######################
def test_create_user__valid_payload(app, payload_1):
    '''
    GIVEN a valid user payload
    WHEN an HTTP POST call is made to /api/v1/users
    THEN check that a 201 is returned
    '''
    res = app.test_client().post('/api/v1/users', json=payload_1)
    check_status = check_fields_same(res.json['data'], payload_1, user_fields)

    assert res.status_code == 201
    assert res.json['success'] == True
    assert check_status == True

def test_create_user__existing_user_payload(app, payload_1):
    '''
    GIVEN a user payload of an existing user
    WHEN an HTTP POST call is made to /api/v1/users
    THEN check that a 409 is returned
    '''
    res = app.test_client().post('/api/v1/users', json=payload_1)

    assert res.status_code == 409
    assert res.json['success'] == False

def test_create_user__throws(app, mocker, payload_2):
    '''
    GIVEN a valid user payload and UserDao.create_user throws
    WHEN an HTTP POST call is made to /api/v1/users
    THEN check that a 500 is returned
    '''
    mocker.patch('app.dao.user_dao.UserDao.create_user', side_effect=Exception)
    res = app.test_client().post('/api/v1/users', json=payload_2)

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'Failed to create user'

def test_get_user_by_id__valid_id(app, payload_1):
    '''
    GIVEN a valid user id of an existing user
    WHEN an HTTP GET call is made to /api/v1/users/{id}
    THEN check that a 200 is returned
    '''
    res = app.test_client().get(f'/api/v1/users/1', json=payload_1)
    check_status = check_fields_same(res.json['data'], payload_1, user_fields)

    assert res.status_code == 200
    assert res.json['success'] == True
    assert check_status == True

def test_get_user_by_id__invalid_id(app, payload_1):
    '''
    GIVEN an invalid user id of a non-existing user
    WHEN an HTTP GET call is made to /api/v1/users/{id}
    THEN check that a 404 is returned
    '''
    res = app.test_client().get(f'/api/v1/users/2', json=payload_1)

    assert res.status_code == 404
    assert res.json['success'] == False
    assert res.json['error'] == 'User not found'

def test_update_user_by_id__valid_id__valid_payload(app, payload_1):
    '''
    GIVEN a valid user id and valid update payload
    WHEN an HTTP PUT call is made to /api/v1/users/{id}
    THEN check that a 404 is returned
    '''
    res = app.test_client().put(f'/api/v1/users/1', json=payload_1)
    check_status = check_fields_same(res.json['data'], payload_1, user_fields)

    assert res.status_code == 200
    assert res.json['success'] == True
    assert check_status == True

def test_update_user_by_id__throws(app, mocker, payload_1):
    '''
    GIVEN a valid user id, a valid update payload, and UserDao.update_user throws
    WHEN an HTTP PUT call is made to /api/v1/users/{id}
    THEN check that a 500 is returned
    '''
    mocker.patch('app.dao.user_dao.UserDao.update_user', side_effect=Exception)
    res = app.test_client().put(f'/api/v1/users/1', json=payload_1)

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'Failed to update user'

def test_update_user_by_id__invalid_id__valid_payload(app, payload_1):
    '''
    GIVEN an invalid user id and valid update payload
    WHEN an HTTP PUT call is made to /api/v1/users/{id}
    THEN check that a 404 is returned
    '''
    res = app.test_client().put(f'/api/v1/users/2', json=payload_1)

    assert res.status_code == 404
    assert res.json['success'] == False
    assert res.json['error'] == 'User not found'

def test_update_user_by_id__valid_id__invalid_payload(app, payload_1, payload_2):
    '''
    GIVEN a valid user id and invalid update payload [email or phonenumber of another user]
    WHEN an HTTP PUT call is made to /api/v1/users/{id}
    THEN check that a 409 is returned
    '''
    # Create another user
    res_2 = app.test_client().post(f'/api/v1/users', json=payload_2)

    payload_1['id'] = res_2.json['data']['id']
    payload_1['email'] = res_2.json['data']['email']
    payload_1['phonenumber'] = res_2.json['data']['phonenumber']
    res_1 = app.test_client().put(f'/api/v1/users/1', json=payload_1)

    assert res_1.status_code == 409
    assert res_1.json['success'] == False
    assert res_1.json['error'] == 'Try again with another email or phonenumber'

def test_delete_user_by_id__valid_id(app, payload_1):
    '''
    GIVEN a valid user id
    WHEN an HTTP DELETE call is made to /api/v1/users/{id}
    THEN check that a 200 is returned
    '''
    res = app.test_client().delete(f'/api/v1/users/1')
    check_status = check_fields_same(res.json['data'], payload_1, user_fields)

    assert res.status_code == 200
    assert res.json['success'] == True
    assert check_status == True

def test_delete_user_by_id__throws(app, mocker):
    '''
    GIVEN a valid user id, and UserDao.delete_user throws
    WHEN an HTTP DELETE call is made to /api/v1/users/{id}
    THEN check that a 500 is returned
    '''
    mocker.patch('app.dao.user_dao.UserDao.delete_user', side_effect=Exception)
    res = app.test_client().delete(f'/api/v1/users/2')

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'Failed to delete user'

def test_delete_user_by_id__invalid_id(app):
    '''
    GIVEN an invalid user id
    WHEN an HTTP DELETE call is made to /api/v1/users/{id}
    THEN check that a 404 is returned
    '''
    res = app.test_client().delete(f'/api/v1/users/3')

    assert res.status_code == 404
    assert res.json['success'] == False
###################### TESTS ######################
