import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_request import MyRequest


class TestUserDelete(BaseCase):

    def test_user_delete(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {"email": email,
                      "password": password}
        response2 = MyRequest.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequest.delete(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})
        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequest.get(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid})
        Assertions.assert_response_text(response4, "User not found")

    @pytest.mark.parametrize("user_id", ["1", "2", "3", "4", "5"])
    def test_user_delete_static_user(self, user_id):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response2 = MyRequest.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequest.delete(f"/user/{user_id}",
                                     headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_response_text(response3, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")
        Assertions.assert_status_code(response3, 400)

    @pytest.mark.xfail(reason="in this case, we expect a bug fix")
    def test_delete_user_another_user(self):
        # REGISTER FIRST USER
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]

        # REGISTER SECOND USER
        register_data = self.prepare_registration_data()
        response2 = MyRequest.post("/user/", data=register_data)
        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")
        user_id = self.get_json_value(response2, "id")

        # LOGIN
        login_data = {"email": email,
                      "password": password}
        response3 = MyRequest.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # DELETE
        response4 = MyRequest.delete(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})
        Assertions.assert_status_code(response4, 400)

