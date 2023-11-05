import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_request import MyRequest


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):

    @allure.title("Delete User")
    def test_user_delete(self):
        allure.dynamic.description("Positive removal test")
        # REGISTER
        with allure.step("Register User"):
            register_data = self.prepare_registration_data()
            response1 = MyRequest.post("/user/", data=register_data)
            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data["email"]
            password = register_data["password"]
            user_id = self.get_json_value(response1, "id")

        # LOGIN
        with allure.step("Login User"):
            login_data = {"email": email,
                          "password": password}
            response2 = MyRequest.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # DELETE
        with allure.step("Delete User"):
            response3 = MyRequest.delete(f"/user/{user_id}",
                                         headers={"x-csrf-token": token},
                                         cookies={"auth_sid": auth_sid})
            Assertions.assert_status_code(response3, 200)

        # GET
        with allure.step("Get deleted User"):
            response4 = MyRequest.get(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})
            Assertions.assert_response_text(response4, "User not found")

    @pytest.mark.parametrize("user_id", ["1", "2", "3", "4", "5"])
    @allure.title("Delete static user (user_id: {user_id})")
    def test_user_delete_static_user(self, user_id):
        allure.dynamic.description("Test for removing static users")
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        with allure.step("Login User"):
            response1 = MyRequest.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")

        # DELETE
        with allure.step("Delete User"):
            response2 = MyRequest.delete(f"/user/{user_id}",
                                         headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
            Assertions.assert_response_text(response2, "Please, do not delete test users with ID 1, 2, 3, 4 or 5.")
            Assertions.assert_status_code(response2, 400)

    # @pytest.mark.xfail(reason="in this case, we expect a bug fix")
    @allure.title("Delete user another user")
    def test_delete_user_another_user(self):
        # REGISTER FIRST USER
        allure.dynamic.description("The test is to delete a user while being logged in by another user")
        with allure.step("Register first User"):
            register_data = self.prepare_registration_data()
            response1 = MyRequest.post("/user/", data=register_data)
            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data["email"]
            password = register_data["password"]

        # REGISTER SECOND USER
        with allure.step("Register Second User"):
            register_data = self.prepare_registration_data()
            response2 = MyRequest.post("/user/", data=register_data)
            Assertions.assert_status_code(response2, 200)
            Assertions.assert_json_has_key(response2, "id")
            user_id = self.get_json_value(response2, "id")

        # LOGIN
        with allure.step("Login first User"):
            login_data = {"email": email,
                          "password": password}
            response3 = MyRequest.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response3, "auth_sid")
            token = self.get_header(response3, "x-csrf-token")

        # DELETE
        with allure.step("Delete Second User by First User"):
            response4 = MyRequest.delete(f"/user/{user_id}",
                                         headers={"x-csrf-token": token},
                                         cookies={"auth_sid": auth_sid})
            Assertions.assert_status_code(response4, 400)
