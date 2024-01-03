import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians
import time
from user_agent import generate_user_agent

def getMiejscowosc(miejsce):
    miejscowosci=['Piaseczno','Bobrowiec','Głosków','Gołków','Konstancin-Jeziona', 'Wołomin','Zalesie Dolne','Zalesie Górne','Zalesie','Nadarzyn','Warszawa','Laski','Chotomów','Gołków-Letnisko','Chylice','Henryków-Urocze']

    for miejscowosc in miejscowosci:
        if miejscowosc.lower() in miejsce.lower():
            return miejscowosc
        
    return miejsce

def getDistance(place1, place2):

    time.sleep(0.4)
    geolocator = Nominatim(user_agent="nieruchomosci_scrapping")
    location1 = geolocator.geocode(place1)
    location2 = geolocator.geocode(place2)
    x1 = location1.latitude
    y1 = location1.longitude

    x2 = location2.latitude
    y2 = location2.longitude

    R = 6373.0

    lat1 = radians(x1)
    lon1 = radians(y1)
    lat2 = radians(x2)
    lon2 = radians(y2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

starting_time_global = datetime.now()


session = requests.Session()
session.trust_env = False
user_agent = generate_user_agent(os=('mac', 'linux', 'win'))
headers = {'user-agent': user_agent}

#conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';'+'Trusted_Connection=yes;MARS_Connection=Yes')

connection = psycopg2.connect(user="postgres",
                                  password="mamuska1",
                                  host="localhost",
                                  port="5432",
                                  database="NieruchomosciWebScrapping")
cursor_distance=connection.cursor()
cursor_distance.execute('TRUNCATE TABLE stg.nieruchomosci_dzialki')
cnt = 0
urls = ["https://www.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,Piaseczno:31230,,,10,,,,,,,,,,,,,,,1", 
"https://www.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,Bobrowiec:29768,,,10,,,,,,,,,,,,,,,1",
"https://warszawa.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,Warszawa:20571,,,10,,,,,,,,,,,,,,,1",
"https://warszawa.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,Podkowa%20Le%C5%9Bna:43852,,,10,,,,,,,,,,,,,,,1",
"https://warszawa.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,Konstancin-Jeziorna:49975,,,10,,,,,,,,,,,,,,,1",
"https://warszawa.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,Zalesie%20G%C3%B3rne:43409,,,10,,,,,,,,,,,,,,,1",
"https://www.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,G%C5%82osk%C3%B3w-Letnisko:47458,,,,,,,,,,,,,,,,,,1",
"https://www.nieruchomosci-online.pl/szukaj.html?3,dzialka,sprzedaz,,G%C5%82osk%C3%B3w:12639,,,,,,,,,,,,,,,,,,1"
]
for url_main in urls:
    while url_main != "":
        try:
            starting_time = datetime.now()
            odpowiedz = session.get(url_main, headers=headers)
            html_doc = odpowiedz.text
            soup_main = BeautifulSoup(html_doc, 'html.parser')
            dzialki = soup_main.find_all(class_="tertiary")
            print('parsing page: ' + url_main)
            for dzialka in dzialki:

                if len(dzialka.find("h2").contents[0])==0:
                    continue
                try:
                    url=dzialka.find("h2").contents[0]["href"]
                except KeyError:
                    continue
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM public.nieruchomosci_dzialki WHERE url = '+'\''+url+'\'')
                if(cursor.rowcount>0):
                    continue
                odpowiedz = requests.get(url, headers=headers)
                html_doc = odpowiedz.text
                soup = BeautifulSoup(html_doc, 'html.parser')
                try:
                    if soup.find_all(class_="secondary")[0].find(class_="name")["title"] == "":
                        agent=soup.find_all(class_="secondary")[0].find(class_="name").text
                    else:
                        agent=soup.find_all(class_="secondary")[0].find(class_="name")["title"]
                except:
                        agent = ""
                cena=soup.find_all(class_="info-primary-price")[0].text
                cena_za_m2=soup.find_all(class_="info-secondary-price")[0].text
                powierzchnia=soup.find_all(class_="info-area")[0].text
                miejsce=soup.find_all(class_="title-b")[0].text
                miejscowosc=getMiejscowosc(miejsce)
                cursor_distance=connection.cursor()
                cursor_distance.execute('SELECT * FROM public.odleglosci WHERE adres = '+'\''+miejsce+'\'')
                if cursor_distance.rowcount == 0:
                    try:
                        odleglosc_od_PKP = getDistance(miejsce, "Dworcowa 9, Piaseczno, mazowieckie")
                    except:
                        odleglosc_od_PKP = 'NULL'
                    try:
                        odleglosc_od_Centrum = getDistance(miejsce, "Plac Defilad 1, Warszawa, mazowieckie")
                    except:
                        odleglosc_od_Centrum = 'NULL'
                    sql='INSERT INTO public.odleglosci VALUES (\'%s\',%s,%s)' % (miejsce, odleglosc_od_PKP, odleglosc_od_Centrum,)
                    cursor_distance.execute(sql)
                    connection.commit()
                if cursor.rowcount == 0:
                    sql_statement='INSERT INTO stg.nieruchomosci_dzialki (url,miejsce,miejscowosc,cena,powierzchnia,cena_za_m2,data_wstawienia,agent) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',NOW(),\'%s\')' % (url, miejsce, miejscowosc, cena, powierzchnia, cena_za_m2, agent)
                    cursor.execute(sql_statement)
                    connection.commit()
                    cnt+=1
            ending_time = datetime.now()
            print('Execution time: ' + str((ending_time-starting_time).total_seconds()))
        except Exception as e:
            print("ERROR: " + str(e))
        try:
            url_main=soup_main.find_all(id="pagination-outer")[0].find(class_="btn-a")["href"]
        except TypeError:
            url_main=""
        connection.commit()
ending_time_global = datetime.now()
cursor_distance=connection.cursor()
cursor_distance.execute('EXEC public.refresh_nieruchomosci_dzialki')
print('Execution time of the entire script: ' + str((ending_time_global-starting_time_global).total_seconds()))
print('Rows inserted: ' + str(cnt))
    