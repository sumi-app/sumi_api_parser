# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json


# /html/body/section/div/div[3]/nav/div/a[3]
# /html/body/section/div/div[3]/nav/div/a[2]


def parse():
    chrome_options = Options()
    # Add for opening screen
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=2')
    driver = webdriver.Chrome(ChromeDriverManager().install(), 0, chrome_options)

    driver.get(f"https://telegrator.ru/channels/puteshestviya/")

    # Доставем элементы навигационного меню
    navs = driver.find_element_by_xpath('/html/body/section/div/div[3]/nav/div').find_elements_by_tag_name('a')
    pages_count = int(navs[len(navs) - 2].text)
    for i in range(pages_count):
        parse_page(driver, i + 1)

    # Открыть след страницу
    # navs[len(navs) - 1].click()


def parse_page(driver, page):
    driver.get(f"https://telegrator.ru/channels/puteshestviya/page/{page}")
    results_row = driver.find_element_by_xpath('/html/body/section/div/div[3]/div[3]')
    cards = results_row.find_elements_by_xpath('div')
    for card in cards:
        parse_blogger_card(card)


def parse_blogger_card(card):
    title = card.find_element_by_class_name('channel_title')
    name = title.find_element_by_tag_name("h3").text
    login = title.find_element_by_tag_name('p').text
    blogger_type = title.find_element_by_tag_name('small').text
    avatar = str(card.find_element_by_class_name("channel_avatar").get_attribute('style'))

    description = card.find_element_by_class_name("channel_info").text
    subs_count = card.find_element_by_class_name("channel_auditory").text

    avatar = avatar.replace('background-image: url("', '')
    avatar = avatar.replace('")', '')

    count_replaced = subs_count.replace(' ', '')
    # type(count_replaced)
    # print(count_replaced)
    json_data = json.dumps({
        "name": str(name),
        "login": str(login),
        "type": str(blogger_type),
        "description": str(description),
        "count": int(count_replaced),
        "avatar": str(avatar),
        "social_network": 0,
    }, ensure_ascii=False)
    json_data.encode('unicode_escape')
    print(json_data)
    headers = {'Content-Type': 'text/text; charset=utf-8'}
    r = requests.post("http://localhost:8080/api/blogger", data=json_data.encode("utf-8"), headers=headers)
    print(r.status_code, r.reason)


if __name__ == '__main__':
    parse()
