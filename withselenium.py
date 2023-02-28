import datetime
import json
import time
from json import JSONEncoder

import requests
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from requests.exceptions import ConnectionError

from threading import Thread
from queue import Queue


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


# producer task
def producer(queue):
    print('Producer: Running')
    # generate items
    with open('urls.txt') as f:
        lines = f.readlines()
        for line in lines:
            item = {
                "url": line.split(";")[0],
                "path": line.split(";")[1]
            }
            # add to the queue
            queue.put(item)
            # report progress
            print(f'>producer added {item}')
            # signal that there are no further items
        queue.put(None)
        print('Producer: Done')


def consumer(queue):
    print('Consumer: Running')
    # consume items
    # get a unit of work
    for i in range(0, 5):
        item = queue.get()
        # check for stop
        if item is None:
            break
        crawl(item['url'], item['path'])
        # report
        print(f'>consumer got {item}')
    # all done
    print('Consumer: Done')


def get_status(logs):
    for log in logs:
        if log['message']:
            d = json.loads(log['message'])
            try:
                content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                response_received = d['message']['method'] == 'Network.responseReceived'
                if content_type and response_received:
                    return d['message']['params']['response']['status']
            except:
                pass


def crawl(url, path):
    startCTime = datetime.datetime.now()
    data = {}
    try:
        r = requests.get(url)

        driver.get(url)
        div = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, path)))
        # div = driver.find_element(By.XPATH, path)
        # time.sleep(3)
        print(r.status_code)
        data = {
            "url": url,
            'created_on': created_on,
            "content": div.text,
            "status": r.status_code
        }
        # print(div)
        print(div.text)
    except (TimeoutException, NoSuchElementException, InvalidArgumentException):
        print("Timeout or Invalid Argument")
        data = {
            "url": url,
            'created_on': created_on,
            "content": "",
            "status": -2
        }
    except ConnectionError as ex:
        print("Connection error", ex)
        data = {
            "url": url,
            'created_on': created_on,
            "content": "",
            "status": -1
        }
    except Exception as ex:
        print("other exception", type(ex).__name__)
        data = {
            "url": url,
            'created_on': created_on,
            "content": "",
            "status": -1
        }
    result_list.append(data)
    # driver.quit()
    endCTime = datetime.datetime.now()
    timeCDelta = endCTime - startCTime
    print(timeCDelta.seconds, "sn crawl süresi.")


result_list = []
url_list = []
paths = []
d = {}
data = []
fileName = 'crawlUrl' + '.json'
outfile1 = open(fileName, 'w')
with open('urls.txt') as f:
    lines = f.readlines()
    for line in lines:
        url_list.append(line.split(";")[0])
        paths.append(line.split(";")[1])
        d = {
            "url": line.split(";")[0],
            "path": line.split(";")[1]
        }
        data.append(d)
json.dump(data, outfile1, cls=DateTimeEncoder)

startTime = datetime.datetime.now()
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
# options.headless = True
options.add_argument("--window-size=1024,800")
created_on = datetime.datetime.now()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

queue = Queue()

producer = Thread(target=producer, args=(queue,))
producer.start()
consumer = Thread(target=consumer, args=(queue,))
consumer.start()

# wait for all threads to finish
consumer.join()

producer.join()

# for url, path in zip(url_list, paths):
#  crawl(url, path)
# crawl("https://www.batmancagdas.com/kunye", "/html/body/div[1]/div[2]/div[4]")
driver.quit()
fileName = 'result' + '.json'
outfile2 = open(fileName, 'w')
json.dump(result_list, outfile2, cls=DateTimeEncoder)
endTime = datetime.datetime.now()
timeDelta = endTime - startTime

print(timeDelta.seconds, "saniye sürdü.")
#crawl(url_list[7], paths[7])
