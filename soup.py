import winsound
import requests
import asyncio
import time
import yaml
import sys

from colorama import init, Fore, Back, Style
from datetime import datetime
from bs4 import BeautifulSoup

def setColor(string, color):
    return color + string + Style.RESET_ALL

async def check(name, url, wait):
    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        price = soup.select(
            'html body div#__next div div div main#pageContent div div div div div.productDetail div strong'
        )[0].text.strip()
        price = setColor(price, Fore.CYAN)

        availability = soup.select(
            'html body div div div div main#pageContent div div div div div.productDetail div span span span.availabilityText div div'
            )[0].text

        color = ""
        if "Livré" in availability:
            winsound.PlaySound("alert.wav", winsound.SND_FILENAME)
            color = Fore.GREEN
        elif("Entre") in availability:
            winsound.PlaySound("alert.wav", winsound.SND_FILENAME)
            color = Fore.CYAN
        elif "Non disponible" in availability:
            color = Fore.RED
        elif("Nous clarifions") in availability:
            color = Fore.RED
        else:
             color = Fore.YELLOW
        color += Style.BRIGHT

        availability = setColor(availability, color)

        print ("%s - %s (%s) - %s" % (now, name, price, availability), flush = True)
        await asyncio.sleep(wait)

# ====================================================================================================================================== #

async def main():
    with open("config.yaml", "r") as yamlfile:
        cfg = yaml.safe_load(yamlfile)

    wait = cfg['refreshTime']
    items = cfg['products']
    wait = cfg['refreshTime']

    tasks = []

    init()
    for item in items:
        tasks.append(asyncio.create_task(check(item['name'], item['url'], wait)))

    for task in tasks:
        await task

    print ("Successfully terminated")

# ====================================================================================================================================== #

asyncio.run(main())