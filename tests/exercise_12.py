import requests

class TestCookies:

    def setup_method(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        assert response.status_code==200, f"Response status code not 200"
        assert "x-secret-homework-header" in response.headers, f"no key HomeWork in cookies"
        self.header = response.headers["x-secret-homework-header"]

    def test_check_cookie_value(self):
        expected_value = "Some secret value"
        assert self.header == expected_value, "Value from cookie key hw_value unexpected"