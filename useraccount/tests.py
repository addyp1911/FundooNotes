import json
from fundoonote.settings import login_url, register_url, password_forgot_url
from rest_framework.test import APITestCase

with open('/home/admin1/Desktop/documents/myproject/fundoonote/templates/testing.json', 'r') as f:
    DATA = json.load(f)


class UserRegistration(APITestCase):
    def test_register_view1(self):
        response = self.client.post(path=register_url, data=DATA[0]['test_user1'])
        print(response.content)
        self.assertEqual(response.status_code, 400)

    def test_register_view2(self):
        response = self.client.post(path=register_url, data=DATA[0]['test_user2'])
        print(response.content)
        self.assertEqual(response.status_code, 400)

    def test_register_view3(self):
        response = self.client.post(path=register_url, data=DATA[0]['test_user3'])
        print(response.content)
        self.assertEqual(response.status_code, 200)


class UserLogin(APITestCase):
    def test_login_view1(self):
        response = self.client.post(path=login_url, data=DATA[1]['test_user1'])
        print(response.content)
        self.assertEqual(response.status_code, 400)

    def test_login_view2(self):
        response = self.client.post(path=login_url, data=DATA[1]['test_user2'])
        print(response.content)
        self.assertEqual(response.status_code, 400)

    def test_login_view3(self):
        response = self.client.post(path=login_url, data=DATA[1]['test_user3'])
        print(response.content)
        self.assertEqual(response.status_code, 400)


class ForgotPassword(APITestCase):
    def test_forgot_password_view1(self):
        response = self.client.post(path=password_forgot_url, data=DATA[2]['test_user1'])
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_view2(self):
        response = self.client.post(path=password_forgot_url, data=DATA[2]['test_user2'])
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_view3(self):
        response = self.client.post(path=password_forgot_url, data=DATA[2]['test_user3'])
        print(response.content)
        self.assertEqual(response.status_code, 200)



