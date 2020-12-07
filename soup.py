import requests
import asyncio
import time
import json
import sys

from colorama import init, Fore, Back, Style
from datetime import datetime
from bs4 import BeautifulSoup

async def check(name, url, wait):
    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")    
        price = soup.select('html body div#__next div div div main#pageContent div div div div div.productDetail div span strong')[0].text.strip()
        availability = soup.select('html body div div div div main#pageContent div div div div div.productDetail div span span span.availabilityText div div')[0].text

        print ("%s - %s (%s) - %s%s%s" % (now, name, price, Fore.RED + Style.BRIGHT, availability, Style.RESET_ALL), flush = True)
        
        await asyncio.sleep(wait)

# ===================================================================================================================================================================== #

async def main():
    items = [
            ("5900x", "https://www.digitec.ch/fr/s1/product/amd-ryzen-9-5900x-am4-370ghz-12-core-processeurs-13987917"),
            ("3080 STRIX", "https://www.digitec.ch/fr/s1/product/asus-geforce-rog-strix-rtx-3080-o10g-gaming-10go-cartes-graphiques-13751783"),
            ]
    wait = 60

    tasks = []

    init()
    for item in items:
        tasks.append(asyncio.create_task(check(item[0], item[1], wait)))

    for task in tasks:
        await task

    print ("Successfully terminated")

# ===================================================================================================================================================================== #

asyncio.run(main())