from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_request import MyRequest
import time


class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {"email": email,
                      "password": password}
        response2 = MyRequest.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        response3 = MyRequest.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"firstName": new_name})
        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequest.get(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of the user after edit")

    def test_edit_user_no_authorized_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Changed name"
        response2 = MyRequest.put(f"/user/{user_id}",
                                  data={"firstName": new_name})
        Assertions.assert_status_code(response2, 400)
        Assertions.assert_response_text(response2, "Auth token not supplied")

    def test_edit_user_another_user(self):
        # REGISTER FIRST USER
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        time.sleep(1)

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

        # EDIT firstName
        new_name = "Changed name"
        response4 = MyRequest.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"firstName": new_name})
        Assertions.assert_status_code(response4, 200)

        response5 = MyRequest.get(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid})
        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_has_not_key(response5, "firstName")

        # EDIT lastName
        new_name = "Changed name"
        response6 = MyRequest.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"lastName": new_name})
        Assertions.assert_status_code(response6, 200)

        response7 = MyRequest.get(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid})
        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_has_not_key(response7, "lastName")

    def test_edit_email(self):
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

        # EDIT
        new_email = "blablabla.ru"
        response3 = MyRequest.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"email": new_email})
        Assertions.assert_response_text(response3, "Invalid email format")
        Assertions.assert_status_code(response3, 400)

        # GET
        response4 = MyRequest.get(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid})
        new_email = self.get_json_value(response4, "email")
        Assertions.assert_status_code(response4, 200)
        Assertions.assert_json_value_by_name(response4, "email", email,
                                             f"email has been changed old email {email}, new email {new_email}")

    def test_edit_firstname_one_symbol(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequest.post("/user/", data=register_data)
        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {"email": email,
                      "password": password}
        response2 = MyRequest.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_first_name = "u"
        response3 = MyRequest.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"firstName": new_first_name})
        Assertions.assert_error_text(response3, "Too short value for field firstName")
        Assertions.assert_status_code(response3, 400)

