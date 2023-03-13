import datetime
import json
import time
from json import JSONEncoder
import sys

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

result_list = []
urlCount = 0
created_on = datetime.datetime.now()
outFolder = sys.argv[1]
threadCount = sys.argv[2]


def producer(queue):
    print('Producer: Running')
    # generate items
    with open(outFolder + 'url.txt') as f:
        print()
        x = f.read()
        url_list = json.loads(x)
        for url in url_list:
            item = {
                "strKunyeAdresiParm": url['strKunyeAdresiParm'],
                "strYayinKoduParm": url['strYayinKoduParm']
            }
            # add to the queue
            queue.put(item)
            # report progress
            print(f'>producer added {item}')
            # signal that there are no further items
        queue.put(None)
        print('Producer: Done')


def consumer(queue, Driver, x):
    # driver =
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.headless = False
    options.add_argument("--window-size=1024,800")
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = Driver(service=Service(ChromeDriverManager().install()), options=options)

    print(x, 'Consumer: Running')
    # consume items
    # get a unit of work

    a = 0
    while queue.empty() == False:
        # print( "before queue get")
        item = queue.get()
        # print( "after queue get")
        # check for stop
        # print( "will crawl")
        if item is None:
            break
        crawl(item['strKunyeAdresiParm'], item['strYayinKoduParm'], driver)
        # print("crawled")
        # report
        # print(f'>consumer got {item}')
        a += 1
        print(a)
        # time.sleep(1)
    # all done

    print(x, 'Consumer: Done ', a, 'items processed.')
    driver.quit()


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def crawl(url, yayinKodu, driver):
    # print(url, yayinKodu)
    strYayinKoduParm = yayinKodu
    startCTime = datetime.datetime.now()
    data = {}
    yayinAdi = ""
    tuzelKisi = ""
    yayinci = ""
    sorumlu = ""
    adres = ""
    tel = ""
    email = ""
    uets = ""
    yersaglayici = ""
    yersaglayiciAdres = ""
    strRawDataXMLParm = ""
    strHttpStatusParm = "0"
    boolKunyeBilgisiTarandiParm = False
    if url:

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bik-kunye-main")))
            try:
                if driver.find_element(By.ID, "bik-kunye-ticaret-unvani"): yayinAdi = driver.find_element(By.ID,
                                                                                                          "bik-kunye-ticaret-unvani").text
                if driver.find_element(By.ID, "bik-kunye-tuzel-kisi-temsilcisi"): tuzelKisi = driver.find_element(By.ID,
                                                                                                                  "bik-kunye-tuzel-kisi-temsilcisi").text
                if driver.find_element(By.ID, "bik-kunye-yayinci"): yayinci = driver.find_element(By.ID,
                                                                                                  "bik-kunye-yayinci").text
                if driver.find_element(By.ID, "bik-kunye-sorumlu-yim"): sorumlu = driver.find_element(By.ID,
                                                                                                      "bik-kunye-sorumlu-yim").text
                if driver.find_element(By.ID, "bik-kunye-yonetim-yeri"): adres = driver.find_element(By.ID,
                                                                                                     "bik-kunye-yonetim-yeri").text
                if driver.find_element(By.ID, "bik-kunye-telefon"): tel = driver.find_element(By.ID,
                                                                                              "bik-kunye-telefon").text
                if driver.find_element(By.ID, "bik-kunye-eposta"): email = driver.find_element(By.ID,
                                                                                               "bik-kunye-eposta").text
                if driver.find_element(By.ID, "bik-kunye-uets"): uets = driver.find_element(By.ID,
                                                                                            "bik-kunye-uets").text
                if driver.find_element(By.ID, "bik-kunye-yer-saglayıcı-unvan"): yersaglayici = driver.find_element(
                    By.ID,
                    "bik-kunye-yer-saglayıcı-unvan").text
                if driver.find_element(By.ID, "bik-kunye-yer-saglayici-adres"): yersaglayiciAdres = driver.find_element(
                    By.ID, "bik-kunye-yer-saglayici-adres").text
                if driver.find_element(By.ID, "bik-kunye-main"): strRawDataXMLParm = driver.find_element(By.ID,
                                                                                                         "bik-kunye-main")
                global urlCount
                urlCount += 1

            except Exception as ex:
                print(ex)
            # time.sleep(3)x
            # print(r.status_code)
            data = {
                "strYayinKoduParm": strYayinKoduParm,
                'dateKunyeTarihiParm': created_on,
                "strYayinSahibiTicareUnvaniParm": yayinAdi,
                "strTuzelKisiTemsilcisiParm": tuzelKisi,
                "strYayinciParm": yayinci,
                "strSorumluMudurYaziIsleriMuduruParm": sorumlu,
                "strYonetimYeriParm": adres,
                "strIletisimTelefonuParm": tel,
                "strKurumsalePostaParm": email,
                "strUETSAdresiParm": uets,
                "strYerSaglayiciTicaretUnvaniParm": yersaglayici,
                "strYerSaglayiciAdresiParm": yersaglayiciAdres,
                "strRawDataXMLParm": strRawDataXMLParm.get_attribute('innerHTML'),
                "strHttpStatusParm": "1",  # r.status_code
                "boolKunyeBilgisiTarandiParm": True
            }
            # print(div)
        except (TimeoutException, NoSuchElementException, InvalidArgumentException) as ex:
            print("Timeout or Invalid Argument. " + str(ex))

            data = {
                "strYayinKoduParm": strYayinKoduParm,
                'dateKunyeTarihiParm': created_on,
                "strYayinSahibiTicareUnvaniParm": yayinAdi,
                "strTuzelKisiTemsilcisiParm": tuzelKisi,
                "strYayinciParm": yayinci,
                "strSorumluMudurYaziIsleriMuduruParm": sorumlu,
                "strYonetimYeriParm": adres,
                "strIletisimTelefonuParm": tel,
                "strKurumsalePostaParm": email,
                "strUETSAdresiParm": uets,
                "strYerSaglayiciTicaretUnvaniParm": yersaglayici,
                "strYerSaglayiciAdresiParm": yersaglayiciAdres,
                "strRawDataXMLParm": strRawDataXMLParm,
                "strHttpStatusParm": "-1",
                "boolKunyeBilgisiTarandiParm": False
            }
        except ConnectionError as ex:
            print("Connection error", ex)
            data = {
                "strYayinKoduParm": strYayinKoduParm,
                'dateKunyeTarihiParm': created_on,
                "strYayinSahibiTicareUnvaniParm": yayinAdi,
                "strTuzelKisiTemsilcisiParm": tuzelKisi,
                "strYayinciParm": yayinci,
                "strSorumluMudurYaziIsleriMuduruParm": sorumlu,
                "strYonetimYeriParm": adres,
                "strIletisimTelefonuParm": tel,
                "strKurumsalePostaParm": email,
                "strUETSAdresiParm": uets,
                "strYerSaglayiciTicaretUnvaniParm": yersaglayici,
                "strYerSaglayiciAdresiParm": yersaglayiciAdres,
                "strRawDataXMLParm": strRawDataXMLParm,
                "strHttpStatusParm": "-2",
                "boolKunyeBilgisiTarandiParm": False
            }
        except Exception as ex:
            print("other exception", type(ex).__name__)
            data = {
                'dateKunyeTarihiParm': created_on,
                'strYayinKoduParm': strYayinKoduParm,
                "strYayinSahibiTicareUnvaniParm": yayinAdi,
                "strTuzelKisiTemsilcisiParm": tuzelKisi,
                "strYayinciParm": yayinci,
                "strSorumluMudurYaziIsleriMuduruParm": sorumlu,
                "strYonetimYeriParm": adres,
                "strIletisimTelefonuParm": tel,
                "strKurumsalePostaParm": email,
                "strUETSAdresiParm": uets,
                "strYerSaglayiciTicaretUnvaniParm": yersaglayici,
                "strYerSaglayiciAdresiParm": yersaglayiciAdres,
                "strRawDataXMLParm": strRawDataXMLParm,
                "strHttpStatusParm": "-3",
                "boolKunyeBilgisiTarandiParm": False
            }
        result_list.append(data)
        # driver.quit()
        endCTime = datetime.datetime.now()
        timeCDelta = endCTime - startCTime
        print(timeCDelta.seconds, "sn crawl süresi.")
    else:
        # URL'in boş olması durumu
        data = {
            "strYayinKoduParm": strYayinKoduParm,
            'dateKunyeTarihiParm': created_on,
            "strYayinSahibiTicareUnvaniParm": yayinAdi,
            "strTuzelKisiTemsilcisiParm": tuzelKisi,
            "strYayinciParm": yayinci,
            "strSorumluMudurYaziIsleriMuduruParm": sorumlu,
            "strYonetimYeriParm": adres,
            "strIletisimTelefonuParm": tel,
            "strKurumsalePostaParm": email,
            "strUETSAdresiParm": uets,
            "strYerSaglayiciTicaretUnvaniParm": yersaglayici,
            "strYerSaglayiciAdresiParm": yersaglayiciAdres,
            "strRawDataXMLParm": "",
            "strHttpStatusParm": "-4",  # r.status_code
            "boolKunyeBilgisiTarandiParm": True
        }
        result_list.append(data)


def main():
    print("running python script system argv=", outFolder)
    url_list = []
    paths = []
    d = {}
    data = []

    startTime = datetime.datetime.now()
    queue = Queue()

    producer1 = Thread(target=producer, args=(queue,))
    producer1.start()
    producer1.join()
    consumers = []
    print("waiting for population")
    # time.sleep(5)
    print("consumers started")
    drivers = []
    for x in range(int(threadCount)):
        c = Thread(target=consumer, args=(queue, webdriver.Chrome, x))
        c.start()
        consumers.append(c)

    for x in range(0, len(consumers)):
        consumers[x].join()

    # crawl("https://onurerden.com/news/urfanatik.html")
    # driver.quit()
    fileName = outFolder + 'crawledData' + '.json'
    outfile2 = open(fileName, 'w')
    json.dump(result_list, outfile2, cls=DateTimeEncoder)
    endTime = datetime.datetime.now()
    timeDelta = endTime - startTime

    resultFile = str(created_on.date()) + "-" + str(created_on.time()).split(".")[0].replace(":",
                                                                                             "-") + '-result' + '.json'
    outfile3 = open(outFolder + resultFile, 'w')
    text = []
    resultDict = {
        "urlCount": str(urlCount) + " adedince link crawl edildi.",
        "date": str(created_on),
        "crawlTime": str(timeDelta.seconds) + " saniye sürdü",
        "results": result_list,
    }
    text.append(resultDict)
    json.dump(text, outfile3, cls=DateTimeEncoder)
    print(timeDelta.seconds, "saniye sürdü.")
    # crawl(url_list[7], paths[7])


if __name__ == "__main__":
    main()
