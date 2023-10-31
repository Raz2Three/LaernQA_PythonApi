import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_request import MyRequest


class TestUserAuth(BaseCase):
    exclude_params = [("no_cookie"), ("no_token")]
    payload = ["password", "email"]
    username_len = [1, 251, 320]

    def setup_method(self):
        data = {"email": "vinkotov@example.com",
                "password": "1234"}

        response1 = MyRequest.post("/user/login", data=data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_auth_method(self):
        response2 = MyRequest.get("/user/auth", headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(response2,
                                             "user_id",
                                             self.user_id_from_auth_method,
                                             "User id from auth method is not equal to user id from check method")

    @pytest.mark.parametrize("condition", exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            response2 = MyRequest.get("/user/auth", headers={"x-csrf-token": self.token})
        else:
            response2 = MyRequest.get("/user/auth", cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(response2, "user_id", 0, f"User is authorized with condition {condition}")

    def test_create_without_ligature(self):
        data = {"email": "testexample.com",
                "password": "1234"}

        response = MyRequest.post("/user/login", data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, "Invalid username/password supplied")

    @pytest.mark.parametrize("field", payload)
    def test_create_without_required_field(self, field):
        if field == "email":
            data = {"email": "test@mail.ru"}
        else:
            data = {"password": "1234"}

        response = MyRequest.post("/user/login", data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, "Invalid email/password supplied")

    @pytest.mark.parametrize("len_username", username_len)
    def test_create_username_with_random_len(self, len_username):
        data = {"email": ''.join(chr(ord('a')+i) for i in range(len_username))+"@mail.ru",
                "password": "1234"}
        response = MyRequest.post("/user/login", data=data)
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response, "Invalid username/password supplied")


