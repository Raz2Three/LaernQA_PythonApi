from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_request import MyRequest
import random


class TestUserGet(BaseCase):

    def setup_method(self):
        data = {"email": "vinkotov@example.com",
                "password": "1234"}
        response = MyRequest.post("/user/login", data=data)
        self.auth_sid = self.get_cookie(response, "auth_sid")
        self.token = self.get_header(response, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response, "user_id")

    def test_get_user_details_not_auth(self):
        response = MyRequest.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_same_user(self):
        response2 = MyRequest.get(f"/user/{self.user_id_from_auth_method}",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_has_keys(response2, ["username", "email", "firstName", "lastName"])

    def test_get_user_details_another_user(self):
        response2 = MyRequest.get(f"/user/1",
                                 headers={"x-csrf-token": self.token},
                                 cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")


