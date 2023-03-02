import os
import pytest
import logging
from dotenv import load_dotenv
from connexion import RestyResolver
from requests.exceptions import Timeout

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
def user(app):
    user = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'johndoe@gmail.com',
        'phonenumber': '09012348765',
        'password': '$Password1'
    }
    res = app.test_client().post('/api/v1/users', json=user)
    return res.json['data']

@pytest.fixture(scope='module')
def auth_token(app, user):
    auth_payload = {
        'user_id': user['id'],
        'password': '$Password1'
    }
    auth_res = app.test_client().post('/api/v1/auth', json=auth_payload)
    return auth_res.json['data']['token']

@pytest.fixture(scope='module')
def account(app, payload, auth_token):
    res = app.test_client().post('/api/v1/accounts', json=payload, headers={'x-auth-token': auth_token})
    return res.json['data']

@pytest.fixture(scope='module')
def credit_payload():
    return {
        'transaction_amount': '500.00',
        'transaction_description': 'Initial Deposit',
        'transaction_type': 'DEPOSIT'
    }

@pytest.fixture(scope='module')
def debit_payload():
    return {
        'transaction_amount': '300.00',
        'transaction_description': 'Udemy course payment',
        'transaction_type': 'WITHDRAWAL'
    }

trans_fields = ['transaction_amount', 'transaction_description', 'transaction_type']
###################### SETUP ######################


###################### TESTS ######################

def test_execute_transaction__fail__non_existing_account(app, credit_payload, auth_token):
    '''
    GIVEN a credit transaction on a non-existing account
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 404 is returned
    '''
    res = app.test_client().post('/api/v1/accounts/2/transactions', json=credit_payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 404
    assert res.json['success'] == False
    assert res.json['error'] == 'Account not found'

def test_execute_transaction__fail__debit_zero_balance(app, debit_payload, account, auth_token):
    '''
    GIVEN a debit transaction on a zero-balance account
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 400 is returned
    '''
    res = app.test_client().post(f'/api/v1/accounts/{account["id"]}/transactions', json=debit_payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 400
    assert res.json['success'] == False
    assert res.json['error'] == 'Terminal account balance can not be negative'

def test_execute_transaction__fail__ip_timeout(app, mocker, credit_payload, account, auth_token):
    '''
    GIVEN a valid credit transaction and ip timeout
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 500 is returned
    '''
    mocker.patch('app.services.http_service.HttpService.get', side_effect=Timeout)
    res = app.test_client().post(f'/api/v1/accounts/{account["id"]}/transactions', json=credit_payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'Internal Server Error'

def test_execute_transaction__fail__ip_exception(app, mocker, credit_payload, account, auth_token):
    '''
    GIVEN a valid credit transaction and ip exception
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 500 is returned
    '''
    mocker.patch('app.services.http_service.HttpService.get', side_effect=Exception)
    res = app.test_client().post(f'/api/v1/accounts/{account["id"]}/transactions', json=credit_payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'Failed to fetch origin ip'

def test_execute_transaction__fail__throws(app, mocker, credit_payload, account, auth_token):
    '''
    GIVEN a valid credit transaction and AccountDao.save_transaction throws
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 500 is returned
    '''
    mocker.patch('app.services.http_service.HttpService.get', return_value={'ip': '196.43.0.1'})
    mocker.patch('app.dao.account_dao.AccountDao.save_transaction', side_effect=Exception)
    res = app.test_client().post(f'/api/v1/accounts/{account["id"]}/transactions', json=credit_payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 500
    assert res.json['success'] == False
    assert res.json['error'] == 'Error executing transaction'

def test_execute_transaction__credit__success(app, mocker, credit_payload, account, auth_token):
    '''
    GIVEN a valid credit transaction
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 201 is returned
    '''
    mocker.patch('app.services.http_service.HttpService.get', return_value={'ip': '196.43.0.1'})
    res = app.test_client().post(f'/api/v1/accounts/{account["id"]}/transactions', json=credit_payload, headers={'x-auth-token': auth_token})
    check_status = check_fields_same(res.json['data'], credit_payload, trans_fields)

    assert res.status_code == 201
    assert res.json['success'] == True
    assert check_status == True

    # verify
    account_res = app.test_client().get(f'/api/v1/accounts/{account["id"]}', headers={'x-auth-token': auth_token})
    assert account_res.json['data']['account_balance'] == '500.00'
    assert account_res.json['data']['transaction_count'] == 1

def test_execute_transaction__debit__success(app, mocker, debit_payload, account, auth_token):
    '''
    GIVEN a valid credit transaction
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 201 is returned
    '''
    mocker.patch('app.services.http_service.HttpService.get', return_value={'ip': '196.43.0.1'})
    res = app.test_client().post(f'/api/v1/accounts/{account["id"]}/transactions', json=debit_payload, headers={'x-auth-token': auth_token})
    check_status = check_fields_same(res.json['data'], debit_payload, trans_fields)

    assert res.status_code == 201
    assert res.json['success'] == True
    assert check_status == True

    # verify
    account_res = app.test_client().get(f'/api/v1/accounts/{account["id"]}', headers={'x-auth-token': auth_token})
    assert account_res.json['data']['account_balance'] == '200.00'
    assert account_res.json['data']['transaction_count'] == 2

def test_execute_transaction__debit__amount_more_than_balance(app, mocker, debit_payload, account, auth_token):
    '''
    GIVEN an invalid debit transaction
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 400 is returned
    '''
    mocker.patch('app.services.http_service.HttpService.get', return_value={'ip': '196.43.0.1'})
    res = app.test_client().post(f'/api/v1/accounts/{account["id"]}/transactions', json=debit_payload, headers={'x-auth-token': auth_token})

    assert res.status_code == 400
    assert res.json['success'] == False
    assert res.json['error'] == 'Terminal account balance can not be negative'

    # verify
    account_res = app.test_client().get(f'/api/v1/accounts/{account["id"]}', headers={'x-auth-token': auth_token})
    assert account_res.json['data']['account_balance'] == '200.00'
    assert account_res.json['data']['transaction_count'] == 2

def test_search_transaction__without_description(app, account, auth_token):
    '''
    GIVEN no search param
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 200 is returned
    '''
    res = app.test_client().get(f'/api/v1/accounts/{account["id"]}/transactions', headers={'x-auth-token': auth_token})

    assert res.status_code == 200
    assert res.json['success'] == True
    assert isinstance(res.json['data'], list)
    assert len(res.json['data']) == 2
    assert res.json['data'][0]['transaction_amount'] == '300.00'
    assert res.json['data'][0]['transaction_type'] == 'WITHDRAWAL'
    assert res.json['data'][1]['transaction_amount'] == '500.00'
    assert res.json['data'][1]['transaction_type'] == 'DEPOSIT'

def test_search_transaction__with_description(app, account, auth_token):
    '''
    GIVEN transaction_description search param
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 200 is returned
    '''
    query = {'description': 'IniTial dEpOsiT'}
    res = app.test_client().get(f'/api/v1/accounts/{account["id"]}/transactions', query_string=query, headers={'x-auth-token': auth_token})

    assert res.status_code == 200
    assert res.json['success'] == True
    assert isinstance(res.json['data'], list)
    assert len(res.json['data']) == 1
    assert res.json['data'][0]['transaction_amount'] == '500.00'
    assert res.json['data'][0]['transaction_type'] == 'DEPOSIT'

def test_search_transaction__with_explicit_pagination(app, account, auth_token):
    '''
    GIVEN transaction_description search param
    WHEN an HTTP POST request is made to /api/v1/accounts/{id}/transactions
    THEN check that a 200 is returned
    '''
    query = {'offset': 0, 'limit': 1}
    res = app.test_client().get(f'/api/v1/accounts/{account["id"]}/transactions', query_string=query, headers={'x-auth-token': auth_token})

    assert res.status_code == 200
    assert res.json['success'] == True
    assert isinstance(res.json['data'], list)
    assert len(res.json['data']) == 1
    assert res.json['data'][0]['transaction_amount'] == '300.00'
    assert res.json['data'][0]['transaction_type'] == 'WITHDRAWAL'
