
from CarChooser.RestApi import app
from sqlalchemy_utils import drop_database, database_exists
from CarChooser.RestApi.extensions import db
import pytest
class TestAPI:
    def setup_method(self):
        self.app = app.create_app("testing")
        self.client = self.app.test_client()
        self.user_data = dict(
            email="asdqwe@test.com",
            password='12345'
        )

    def test_registrate(self):
        resp = self.client.post('/auth/register', json=self.user_data).get_json()
        assert resp['status'] == 'success', f"Response obj: {resp}"
        assert resp['message'] == 'Successfully registered.'
        assert type(resp["auth_token"]) == str
        assert len(resp['auth_token']) > 0

    def test_login(self):
        resp = self.client.post('/auth/login', json=self.user_data).get_json()
        assert resp['status'] == 'success'
        assert resp['message'] == 'Successfully logged in.'
        assert type(resp["auth_token"]) == str
        assert len(resp['auth_token']) > 0

    def test_status(self):
        token = self.client.post('/auth/login', json=self.user_data).get_json()['auth_token']
        header = dict(Authorization = f'Bearer {token}')
        resp = self.client.get('/auth/status', headers=header).get_json()
        assert resp['status'] == "success"
        assert type(resp['data']["user_id"]) == int
        assert resp['data']['email'] == self.user_data['email']
        assert resp['data']['admin'] == False
        assert type(resp['data']['registered_on']) == str

    def test_logout(self):
        token = self.client.post('/auth/login', json=self.user_data).get_json()['auth_token']
        header = dict(Authorization = f'Bearer {token}')
        resp = self.client.post('/auth/logout', headers=header).get_json()
        assert resp['status'] == 'success'
        assert resp['message'] == 'Successfully logged out.'
    
    @pytest.mark.parametrize(
            argnames="user_data, expected_resp", 
            argvalues=[
                    [{"email": "asd121asd.asd", "password": "asd123"}, 'value is not a valid email address: email'],
                    [{"email": "asd1@asd.asd", "password": "asd1#23"}, "Incorrect symbols in password: {'#'}"],
                    [{"email": "asd1@asd.asd"}, 'field required: password'],
                    [{"password": "asd123"}, 'field required: email'],
                ]
        )
    def test_negative_registration(self, user_data, expected_resp):
        resp = self.client.post('/auth/register', json=user_data).get_json()
        assert resp['status'] == 'fail'
        assert resp['message'] == expected_resp

    def test_negative_login_inc_password(self):
        self.user_data['password'] = '01010111'
        resp = self.client.post('/auth/login', json=self.user_data).get_json()
        assert resp['message'] == 'Incorrect password'
    
    def test_negative_login_unexisting_email(self):
        self.user_data['email'] = 'asdyrt010101@llal.asdwwq'
        resp = self.client.post('/auth/login', json=self.user_data).get_json()
        assert resp['message'] == 'User does not exist.'

    def test_negative_status(self):
        header = dict(Authorization = f'Bearer lala')
        resp = self.client.get('/auth/status', headers=header).get_json()
        assert resp['message'] == "Invalid token. Please log in again."
    
    def test_negative_status_wihout_token(self):
        resp = self.client.get('/auth/status').get_json()
        assert resp['message'] == "Provide a valid auth token."
    
    def test_negative_logout(self):
        header = dict(Authorization = f'Bearer lala')
        resp = self.client.post('/auth/logout', headers=header).get_json()
        assert resp['message'] == "Invalid token. Please log in again."
    
    def test_negative_logout_wihout_token(self):
        resp = self.client.post('/auth/logout').get_json()
        assert resp['message'] == "Provide a valid auth token."