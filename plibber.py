# -*- coding: utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json

from mapper import get_social_type

query = "https://plibber.ru/?f%5Branges%5D%5Bprice_from%5D=0&f%5Branges%5D%5Bprice_to%5D=1000000&f%5Bsubscribers_from" \
        "%5D=0&f%5Bsubscribers_to%5D=1000000&f%5Bproperties%5D%5Bsubject%5D=putesestviya "


def parse():
    chrome_options = Options()
    # Add for opening screen
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument('log-level=2')
    driver = webdriver.Chrome(ChromeDriverManager().install(), 0, chrome_options)

    driver.get(
        f"{query}&page=1")

    bottom_nav = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/div[1]/div/div[4]/nav/ul")
    bottom_nav_items = bottom_nav.find_elements_by_tag_name('li')
    count_pages = int(bottom_nav_items[len(bottom_nav_items) - 2].text)
    print(f"Pages count: {count_pages}")

    for i in range(count_pages):
        parse_cards(driver, i + 1)


def parse_cards(driver, i):
    driver.get(f"{query}&page={i}")
    results_row = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div[1]/div/div[3]')
    cards = results_row.find_elements_by_xpath('div')
    print(len(cards))

    more_links = []

    for card in cards:
        title = card.find_element_by_class_name("block-top__name")
        more_link = title.find_element_by_class_name("block-title").get_attribute("href")
        more_links.append(more_link)

    for link in more_links:
        driver.get(link)
        name = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/h1").text
        blogger_type = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/p").text
        login = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div[1]/a").text
        avatar = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/img[1]").get_attribute("src")

        tab_bar = driver.find_element_by_xpath("/html/body/div[1]/div/nav/ol")
        tab_items = tab_bar.find_elements_by_tag_name("li")
        social_network = tab_items[len(tab_items) - 2].text

        cost = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/div[1]/div").text
        coverage = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/div[2]/div").text
        subs_count = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div/div[2]/div[1]/div[3]/div[2]/div[1]/div[3]/div").text
        description = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]").text

        count_replaced = subs_count.replace(' ', '')
        cost_replaced = cost.replace(' ', '')
        coverage_replaced = coverage.replace(' ', '')
        print('------------------------------------')
        print(social_network)

        json_data = json.dumps({
            "name": str(name),
            "login": str(login),
            "type": str(blogger_type),
            "description": str(description),
            "count": int(count_replaced),
            "avatar": str(avatar),
            "social_network": int(get_social_type(social_network)),
            "cost": int(cost_replaced),
            "coverage": int(coverage_replaced),
        }, ensure_ascii=False)
        json_data.encode('unicode_escape')
        print(json_data)

        headers = {'Content-Type': 'text/text; charset=utf-8'}
        r = requests.post("http://localhost:8080/api/blogger", data=json_data.encode("utf-8"), headers=headers)
        print(r.status_code, r.reason)

        print('------------------------------------')

        #  name = title.find_element_by_tag_name("a")
        #  channelType = title.find_element_by_class_name("block-network__text")
        # title.click()

        # driver.execute_script("window.history.go(-1)")
        # print(login)


if __name__ == '__main__':
    parse()
