import datetime
import json
import time
from json import JSONEncoder

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def crawl(url, path):
    startCTime = datetime.datetime.now()
    outfile = open('result2.json', 'w')
    data = {}
    #options = Options()
    #options.add_argument("start-maximized")
    #time.sleep(3)
    try:
        driver.get(url)
        div = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, path)))
        #div = driver.find_element(By.XPATH, path)
        #time.sleep(3)
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
    except InvalidArgumentException:
        print("Invalid Argument")
    json.dump(data, outfile, cls=DateTimeEncoder)
    #driver.quit()
    endCTime = datetime.datetime.now()
    timeCDelta = endCTime - startCTime
    print(timeCDelta.seconds, "sn crawl süresi.")


url_list = []
paths = []
with open('urls.txt') as f:
    lines = f.readlines()
    for line in lines:
        url_list.append(line.split(";")[0])
        paths.append(line.split(";")[1])
startTime = datetime.datetime.now()
options = Options()
options.headless = True
options.add_argument("--window-size=1024,800")
created_on = datetime.datetime.now()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
for url, path in zip(url_list, paths):
   crawl(url, path)
driver.quit()
endTime = datetime.datetime.now()
timeDelta = endTime-startTime
print(timeDelta.seconds , "saniye sürdü.")
#crawl(url_list[1], paths[1])
