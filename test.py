import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from lxml import etree

def crawling(url, path):
    outfile = open('result2.json', 'w')
    print(url)  
    r = requests.get(url)
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        raise SystemExit(e)
    soup = BeautifulSoup(r.content,
                         "html.parser")
    #dom = etree.HTML(str(soup))
    dom = soup.find_all("div", {"class": "entry-content est-content-1"})
    for i in dom:
        print( i.find('p').text)
        data = {
            "text": i.find('p').text
        }
    json.dump(data, outfile)
    #print(dom.xpath(path))
  

url = "https://www.olay.com.tr/kunye"
path = '/html/body/div[5]/div[2]/div[4]'
crawling(url,path)
