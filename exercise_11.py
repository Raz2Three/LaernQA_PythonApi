import requests


class TestCookies:

    def setup_method(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        assert "HomeWork" in response.cookies, f"no key HomeWork in cookies"
        self.cookie = response.cookies["HomeWork"]

    def test_check_cookie_value(self):
        expected_value = "hw_value"
        assert self.cookie == expected_value, "Value from cookie key hw_value unexpected"
