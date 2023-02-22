import datetime
import json
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def crawl(url, path):
    outfile = open('result2.json', 'w')
    data = {}
    options = Options()
    options.add_argument("start-maximized")
    created_on = datetime.datetime.now()

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        time.sleep(3)
        driver.get(url)
        time.sleep(3)
        div = driver.find_element(By.XPATH, path)
        time.sleep(3)
        data = {
            "url": url,
            'created_on': created_on,
            "content": div.text
        }
        print(div)
        print(div.text)
    except TimeoutException:
        print("Timeout")
    except NoSuchElementException:
        print("Element not found")
    json.dump(data, outfile)


url_list = []
paths = []
with open('urls.txt') as f:
    lines = f.readlines()
    for line in lines:
        url_list.append(line.split(";")[0])
        paths.append(line.split(";")[1])
for url, path in zip(url_list, paths):
    crawl(url, path)
crawl(url_list[3], paths[3])
