import json
import requests
import pytest


def cook_data():
    request_headers = [
        'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
        'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1']
    response_text = [{'platform': 'Mobile', 'browser': 'No', 'device': 'Android'},
                     {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'},
                     {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'},
                     {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'},
                     {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'}]

    return list(zip(request_headers, response_text))


class TestUserAgent:
    @pytest.mark.parametrize("header_value, expected", cook_data())
    def test_fields_value(self, header_value, expected):
        header = {"User-Agent": header_value}
        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers=header)
        assert response.status_code == 200, f"Response status code not 200"
        try:
            response_in_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in Json format. Response text is {response.text}"
        assert expected["platform"] == response_in_dict["platform"], f"Value in field platform not equal by User-Agent {header_value}"
        assert expected["browser"] == response_in_dict["browser"], f"Value in field browser not equal by User-Agent {header_value}"
        assert expected["device"] == response_in_dict["device"], f"Value in field device not equal by User-Agent {header_value}"
