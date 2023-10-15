import requests
import time

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
resp_json = response.json()
token = resp_json.get("token", "failed")
time_sleep = resp_json.get("seconds", "failed")

check_status = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
status = check_status.json().get("status", "")
if status == "Job is NOT ready":
    time.sleep(time_sleep)
    response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token})
    print(response.json())
else:
    print("Field status Failed")
