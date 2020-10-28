import requests
from bs4 import BeautifulSoup
import pyodbc
from datetime import datetime
url_main = "https://www.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,Bobrowiec:29768,,,,,-1500"
odpowiedz = requests.get(url_main)
html_doc = odpowiedz.text
soup_main = BeautifulSoup(html_doc, 'html.parser')
newurl=soup_main.find_all(id="pagination-outer")[0]

print(newurl)