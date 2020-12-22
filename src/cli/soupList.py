import winsound
import requests
import asyncio
import time
import yaml
import sys

from datetime import datetime
from bs4 import BeautifulSoup

def check(url, wait):
    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        articles = soup.select('html body div#__next div div div main#pageContent div div div#productListingContainer div div.productList article.panelProduct')
        availabilities = soup.select('html body div#__next div div div main#pageContent div div div#productListingContainer div div.productList article.panelProduct div div span svg')
        names = soup.select('html body div#__next div div div main#pageContent div div div#productListingContainer div div.productList article.panelProduct div div div div div.productName')
        prices = soup.select('html body div#__next div div div main#pageContent div div div#productListingContainer div div.productList article.panelProduct div div div div div span strong')

        for article in articles:
            availability = article.select_one('div div span svg')
            name = article.select_one('div div div div div.productName').text
            price = article.select_one('div div div div div span strong').text
            print ("%s - %s (%s) - %s" % (now, name, price, availability), flush = True)
            
        time.sleep(wait)

# ====================================================================================================================================== #

async def main():
    wait = 60
    url = "https://www.digitec.ch/fr/s1/producttype/cartes-graphiques-106?pdo=39-666%3A742%7C39-347%3A628536&tagIds=76&so=1"

    check(url, wait)

    print ("Successfully terminated")

# ====================================================================================================================================== #

asyncio.run(main())