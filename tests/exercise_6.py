import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

print(f"Количество редиректов: {len(response.history)}")
print(f"Итоговый url: {response.history[-1].url}")