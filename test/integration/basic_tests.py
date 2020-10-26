from base import ApiGatewayTestBase
import requests
import json
import bcrypt


class BasicTests(ApiGatewayTestBase):
    def tearDown(self):
        super().tearDown()
        self.db_conn.close()

    def test_login_endpoint(self):
        cursor = self.get_db_cursor()
        hashed_passwd = bcrypt.hashpw("valid_passwd".encode(), bcrypt.gensalt())
        cursor.execute(f"INSERT INTO users (name, passwd) VALUES ('valid_username', '{hashed_passwd.decode()}')")
        self.db_conn.commit()
        payload = {
            "username": "valid_username",
            "passwd": "valid_passwd"
        }
        code, res = self.wrapped_request(requests.post, f'{self.url}/login', json=payload)
        self.assertEqual(code, 200)
        self.assertIn("access_token", res)

    def test_invalid_route(self):
        code, res = self.wrapped_request(requests.get, f'{self.url}/invalid_route')
        self.assertEqual(code, 404)

    def test_login_with_invalid_method(self):
        code, res = self.wrapped_request(requests.get, f'{self.url}/login')
        self.assertEqual(code, 405)

    def test_login_without_body(self):
        code, res = self.wrapped_request(requests.post, f'{self.url}/login')
        self.assertEqual(code, 401)
        self.assertIn("Body is required", res.get("reasons"))

    def test_login_if_invalid_body_format(self):
        payload = "invalid_body"
        headers = {'content-type': 'application/json'}
        res = requests.post(f'{self.url}/login', headers = headers, data = payload)
        self.assertEqual(res.status_code, 400)
        self.assertIn("Invalid body format", json.loads(res.text).get("msg"))

    def test_login_without_username(self):
        payload = {
            "passwd": "passwd"
        }
        code, res = self.wrapped_request(requests.post, f'{self.url}/login', json=payload)
        self.assertEqual(code, 401)
        self.assertIn("Username is required", res.get("reasons"))

    def test_login_without_passwd(self):
        payload = {
            "username": "username"
        }
        code, res = self.wrapped_request(requests.post, f'{self.url}/login', json=payload)
        self.assertEqual(code, 401)
        self.assertIn("Passwd is required", res.get("reasons"))

    def test_login_with_invalid_username(self):
        cursor = self.get_db_cursor()
        cursor.execute("INSERT INTO users (name, passwd) VALUES ('valid_username', 'valid_passwd')")
        self.db_conn.commit()
        payload = {
            "username": "invalid_username",
            "passwd": "valid_passwd"
        }
        code, res = self.wrapped_request(requests.post, f'{self.url}/login', json=payload)
        self.assertEqual(code, 401)
        self.assertIn("Invalid username", res.get("reasons"))

    def test_login_with_invalid_passwd(self):
        cursor = self.get_db_cursor()
        hashed_passwd = bcrypt.hashpw("valid_passwd".encode(), bcrypt.gensalt())
        cursor.execute(f"INSERT INTO users (name, passwd) VALUES ('valid_username', '{hashed_passwd.decode()}')")
        self.db_conn.commit()
        payload = {
            "username": "valid_username",
            "passwd": "invalid_passwd"
        }
        code, res = self.wrapped_request(requests.post, f'{self.url}/login', json=payload)
        self.assertEqual(code, 401)
        self.assertIn("Invalid password", res.get("reasons"))

    def test_root_endpoint(self):
        cursor = self.get_db_cursor()
        hashed_passwd = bcrypt.hashpw("valid_passwd".encode(), bcrypt.gensalt())
        cursor.execute(f"INSERT INTO users (name, passwd) VALUES ('valid_username', '{hashed_passwd.decode()}')")
        self.db_conn.commit()
        payload = {
            "username": "valid_username",
            "passwd": "valid_passwd"
        }
        _, res = self.wrapped_request(requests.post, f'{self.url}/login', json = payload)
        headers = { 'Authorization': f'Bearer {res.get("access_token")}'}
        code, res = self.wrapped_request(requests.get, f'{self.url}/', headers = headers)
        self.assertEqual(code, 200)
        self.assertEqual(res.get("name"), "sparkle-api-gateway")

        version = res.get("version")
        self.assertIsNotNone(version)
        self.assertIn("major", version)
        self.assertIn("minor", version)
        self.assertIn("build", version)

    
