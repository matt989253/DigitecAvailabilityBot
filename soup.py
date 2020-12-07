import requests
import time
import json
import sys

from colorama import init, Fore, Back, Style
from datetime import datetime
from bs4 import BeautifulSoup

url = sys.argv[1] # product url
wait = int(sys.argv[2]) # time to wait in secconds

init()

while True:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")    
    name = soup.select('html body div#__next div div div main#pageContent div div div div div.productDetail h1')[0].text

    availability = soup.select('html body div div div div main#pageContent div div div div div.productDetail div span span span.availabilityText div div')[0].text
    price = soup.select('html body div#__next div div div main#pageContent div div div div div.productDetail div span strong')[0].text.strip()

    print ("%s - %s (%s) - %s%s%s" % (now, name, price, Fore.RED + Style.BRIGHT, availability, Style.RESET_ALL), flush = True)
    time.sleep(wait)