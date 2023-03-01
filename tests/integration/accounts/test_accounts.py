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
    os.environ['APP_NAME'] = 'Now Transact Test'
    connex_app = create_app()
    connex_app.add_api('../api_spec.yml', resolver=RestyResolver('app.controllers'))
    app = connex_app.app
    # app.logger.disabled = True # remember to comment in pipeline

    with app.app_context() as context:
        context.push()
        db.create_all()
        yield app

    db.drop_all()

@pytest.fixture(scope='module')
def payload():
    return {
        'account_name': 'John Doe'
    }

@pytest.fixture(scope='module')
def user():
    return {
        "firstname": "John",
        "lastname": "Doe",
        "email": "johndoe@gmail.com",
        "phonenumber": "09012348765",
        "password": "$Password1"
    }

@pytest.fixture(scope='module')
def user_2():
    return {
        "firstname": "Jane",
        "lastname": "Doe",
        "email": "janedoe@gmail.com",
        "phonenumber": "09087651234",
        "password": "$Password1"
    }

@pytest.fixture(scope='module')
def auth_token(app, user):
    user_res = app.test_client().post('/api/v1/users', json=user)
    auth_payload = {
        'user_id': user_res.json['data']['id'],
        'password': user['password']
    }
    auth_res = app.test_client().post('/api/v1/auth', json=auth_payload)
    return auth_res.json['data']['token']

@pytest.fixture(scope='module')
def auth_token_2(app, user_2):
    user_res = app.test_client().post('/api/v1/users', json=user_2)
    auth_payload = {
        'user_id': user_res.json['data']['id'],
        'password': user_2['password']
    }
    auth_res = app.test_client().post('/api/v1/auth', json=auth_payload)
    return auth_res.json['data']['token']
###################### SETUP ######################


###################### TESTS ######################

def test_create_account__no_auth_header(app, payload):
    '''
    GIVEN no auth header
    WHEN an HTTP POST call is made to /api/v1/accounts
    THEN check that a 500 is returned
    '''
    res = app.test_client().post('/api/v1/accounts', json=payload, headers={})

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'x-auth-token is required in header'

def test_create_account__empty_auth_header(app, payload):
    '''
    GIVEN an auth header is available but empty
    WHEN an HTTP POST call is made to /api/v1/accounts
    THEN check that a 403 is returned
    '''
    res = app.test_client().post('/api/v1/accounts', json=payload, headers={'x-auth-token': ''})

    assert res.status_code == 403
    assert res.json['success'] == False
    assert res.json['error'] == 'Invalid x-auth-token'

def test_create_account__throws(app, mocker, payload, auth_token):
    '''
    GIVEN a valid payload and valid auth header, and AccountDao.create_account throws
    WHEN an HTTP POST call is made to /api/v1/accounts
    THEN check that a 500 is returned
    '''
    mocker.patch('app.dao.account_dao.AccountDao.create_account', side_effect=Exception)
    res = app.test_client().post('/api/v1/accounts', json=payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'Could not create account'

def test_create_account__success(app, payload, auth_token):
    '''
    GIVEN a valid payload and valid auth header
    WHEN an HTTP POST call is made to /api/v1/accounts
    THEN check that a 201 is returned, and balance is initially 0.00
    '''
    res = app.test_client().post('/api/v1/accounts', json=payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 201
    assert res.json['success'] == True
    assert res.json['data']['account_name'] == payload['account_name']
    assert res.json['data']['account_balance'] == '0.00'

def test_create_account__fail_multiple_account_per_user(app, payload, auth_token):
    '''
    GIVEN a valid payload and valid auth header for a user with an account already
    WHEN an HTTP POST call is made to /api/v1/accounts
    THEN check that a 400 is returned
    '''
    res = app.test_client().post('/api/v1/accounts', json=payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 400
    assert res.json['success'] == False
    assert res.json['error'] == 'Cannot create more than one account per user at this time'

def test_get_account__invalid_account_id(app, auth_token):
    '''
    GIVEN an invalid account_id and auth header
    WHEN an HTTP GET call is made to /api/v1/accounts/{id}
    THEN check that a 404 is returned
    '''
    res = app.test_client().get('/api/v1/accounts/2', headers={'x-auth-token': auth_token})

    assert res.status_code == 404
    assert res.json['success'] == False
    assert res.json['error'] == 'Cannot retrieve non-existent account, kindly create one'

def test_get_account__valid_account_id(app, auth_token):
    '''
    GIVEN a valid account_id and auth header
    WHEN an HTTP GET call is made to /api/v1/accounts/{id}
    THEN check that a 200 is returned
    '''
    res = app.test_client().get('/api/v1/accounts/1', headers={'x-auth-token': auth_token})

    assert res.status_code == 200
    assert res.json['success'] == True
    assert res.json['data']['transaction_count'] == 0

def test_update_account__non_existing_account(app, payload, auth_token_2, user_2):
    '''
    GIVEN a non-existing account_id and auth header
    WHEN an HTTP PUT call is made to /api/v1/accounts/{id}
    THEN check that a 400 is returned
    '''
    user_res = app.test_client().post('/api/v1/users', json=user_2)
    payload['account_name'] = 'John Oneal'
    res = app.test_client().put('/api/v1/accounts/2', json=payload, headers={'x-auth-token': auth_token_2})

    assert res.status_code == 400
    assert res.json['success'] == False
    assert res.json['error'] == 'Cannot update non-existent account, kindly create one'

# This method simulates a throw in 'app.dao.account_dao.AccountDao.create_account'
def test_update_account__existing_account_of_another_user(app, payload, auth_token_2):
    '''
    GIVEN an existing account_id of another user and auth header
    WHEN an HTTP PUT call is made to /api/v1/accounts/{id}
    THEN check that a 400 is returned
    '''
    account_res = app.test_client().post('/api/v1/accounts', json=payload, headers={'x-auth-token': auth_token_2})
    payload['account_name'] = 'Jane Oneal'
    res = app.test_client().put('/api/v1/accounts/1', json=payload, headers={'x-auth-token': auth_token_2})

    assert res.status_code == 500
    assert res.json['success'] == False
    assert account_res.json['data']['id'] == 2 # user account_id is 2, but account_id in update request is 1
    assert res.json['error'] == 'Could not update account'

def test_update_account__success(app, payload, auth_token_2):
    '''
    GIVEN a valid account_id and auth header
    WHEN an HTTP PUT call is made to /api/v1/accounts/{id}
    THEN check that a 200 is returned
    '''
    payload['account_name'] = 'Jane Oneal'
    res = app.test_client().put('/api/v1/accounts/2', json=payload, headers={'x-auth-token': auth_token_2})

    assert res.status_code == 200
    assert res.json['success'] == True
    assert res.json['data']['account_name'] == 'Jane Oneal'

def test_delete_account__non_existing_account(app, auth_token):
    '''
    GIVEN an invalid account_id and auth header
    WHEN an HTTP DELETE call is made to /api/v1/accounts/{id}
    THEN check that a 404 is returned
    '''
    res = app.test_client().delete('/api/v1/accounts/3', headers={'x-auth-token': auth_token})

    assert res.status_code == 404
    assert res.json['success'] == False
    assert res.json['error'] == 'Cannot delete non-existent account, kindly create one'

def test_delete_account__throws(app, mocker, auth_token):
    '''
    GIVEN an invalid account_id and auth header, and AccountDao.delete_user throws
    WHEN an HTTP DELETE call is made to /api/v1/accounts/{id}
    THEN check that a 500 is returned
    '''
    mocker.patch('app.dao.account_dao.AccountDao.delete_account', side_effect=Exception)
    res = app.test_client().delete('/api/v1/accounts/1', headers={'x-auth-token': auth_token})

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'Could not delete account'

def test_delete_account__success(app, auth_token_2):
    '''
    GIVEN a valid account_id and auth header
    WHEN an HTTP DELETE call is made to /api/v1/accounts/{id}
    THEN check that a 200 is returned
    '''
    res = app.test_client().delete('/api/v1/accounts/2', headers={'x-auth-token': auth_token_2})

    assert res.status_code == 200
    assert res.json['success'] == True
    assert res.json['data']['account_name'] == 'Jane Oneal'
