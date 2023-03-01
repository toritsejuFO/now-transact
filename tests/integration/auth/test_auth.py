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
def user_payload():
    return {
        "firstname": "John",
        "lastname": "Doe",
        "email": "johndoe@gmail.com",
        "phonenumber": "09012348765",
        "password": "$Password1"
    }

@pytest.fixture(scope='module')
def user(app, user_payload):
    user_res = app.test_client().post('/api/v1/users', json=user_payload)
    return user_res.json['data']
###################### SETUP ######################


###################### SETUP ######################

def test_get_auth_token__invalid_user(app):
    auth_payload = {
        'user_id': 2,
        'password': '$Password1'
    }
    res = app.test_client().post('/api/v1/auth', json=auth_payload)

    assert res.status_code == 401
    assert res.json['error'] == 'Invalid auth details'

def test_get_auth_token__invalid_password(app):
    auth_payload = {
        'user_id': 1,
        'password': 'password'
    }
    res = app.test_client().post('/api/v1/auth', json=auth_payload)

    assert res.status_code == 401
    assert res.json['error'] == 'Invalid auth details'

def test_get_auth_token__valid_credentials(app, user):
    auth_payload = {
        'user_id': user['id'],
        'password': '$Password1'
    }
    res = app.test_client().post('/api/v1/auth', json=auth_payload)

    assert res.status_code == 200
    assert res.json['data']['token'] != ''
