from tokenize import String
import requests
from bs4 import BeautifulSoup, NavigableString
import pyodbc
from datetime import datetime
from geopy.geocoders import Nominatim
from math import sin, cos, sqrt, atan2, radians
import time
from user_agent import generate_user_agent

def getRynek(rynek):
    
    rynki=['wtórny','pierwotny','wtorny']

    for r in rynki:
        if r in rynek.lower():
            return r

    return ""

def getDzielnica(tytul):

    dzielnice=['Mokotów', 'Ursynów', 'Wola', 'Białołęka', 'Bielany', 'Bemowo', 'Targówek', 'Śródmieście', 'Ochota','Wawer','Praga-Północ','Praga-Południe','Praga','Ursus','Żoliborz','Włochy','Wilanów','Wesoła','Rembertów', 'Bródno', 'Skorosze','Gocław','Odolany','Żerań','Ząbki','Szczęśliwice','Marki','Tarchomin','Siekierki','Powiśle','Raków','Grochów','Służewiec','Chrzanów','Piaseczno','Legionowo','Ksawerów','Kabaty','Łomianki','Sadyba','Saska Kępa','Szmulowizna','Mirów','Sielce','Służew','Pruszków','Stara Miłosna','Nowa Miłosna','Miłosna','Powsin','Chomiczówka','Wierzbno']

    for dzielnica in dzielnice:
        if dzielnica.lower() in tytul.lower():
            return dzielnica
        
    return tytul

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
server = 'LAPTOP-6FDB4KPM' 
database = 'NieruchomosciScrapping' 
session = requests.Session()
session.trust_env = False
user_agent = generate_user_agent(os=('mac', 'linux', 'win'))
headers = {'user-agent': user_agent}
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';'+'Trusted_Connection=yes;MARS_Connection=Yes')
cursor_distance=conn.cursor()
cursor_distance.execute('TRUNCATE TABLE stg.nieruchomosci_mieszkania')
conn.commit()
cnt = 0
urls = ["https://warszawa.nieruchomosci-online.pl/szukaj.html?3,mieszkanie,sprzedaz,,Warszawa:20571,,,,,,,,,,,,,4"
]
for url_main in urls:
    while url_main != "":
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
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dbo.nieruchomosci_mieszkania WHERE url = '+'\''+url+'\'')
            if(cursor.rowcount>0):
                continue
            try:
                dzielnica = dzialka.find_all(class_ = "province__wrapper")[0].find(class_ = "province").find_all('a', {'class' : 'margin-right4'})[0].contents[0]
            except:
                dzielnica = ""
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
            try:
                cena=soup.find_all(class_="info-primary-price")[0].text
            except:
                cena=""
            try:
                cena_za_m2=soup.find_all(class_="info-secondary-price")[0].text
            except:
                cena_za_m2=""
            try:
                powierzchnia=soup.find_all(class_="info-area")[0].text
            except:
                powierzchnia=""
            miejsce=soup.find_all(class_="title-b")[0].text
            dzielnica = getDzielnica(miejsce)
            panel_z_informacjami = soup.find_all(class_ = "box__attributes desktop")[0]
            pietro=""
            liczba_pokoi=""
            rok_budowy=""
            miejsce_parkingowe=""
            stan_mieszkania=""
            rynek=""
            czynsz=""
            wyposazenie=""
            for info in panel_z_informacjami:
                if(isinstance(info, NavigableString)):
                    continue
                content = info.find('div', {'class': 'box__attributes--content'})
                subcontent = content.find_all('span', {'class': 'fheader'})[0].contents[0]
                if(subcontent=="Piętro:"):
                    for span in content:
                        if(len(span.attrs) == 0):
                            continue
                        if(span.attrs['class'][0])=="fheader":
                            continue
                        pietro = pietro + span.contents[0]

                elif(subcontent=="Liczba pokoi:"):
                    for span in content:
                        if(len(span.attrs) == 0):
                            continue
                        if(span.attrs['class'][0])=="fheader":
                            continue
                        liczba_pokoi = liczba_pokoi + span.contents[0]

                elif(subcontent=="Rok budowy:"):
                    for span in content:
                        if(len(span.attrs) == 0):
                            continue
                        if(span.attrs['class'][0])=="fheader":
                            continue
                        rok_budowy = rok_budowy + span.contents[0]

                elif(subcontent=="Miejsce parkingowe:"):
                    for span in content:
                        if(len(span.attrs) == 0):
                            continue
                        if(span.attrs['class'][0])=="fheader":
                            continue
                        miejsce_parkingowe = miejsce_parkingowe + span.contents[0]

                elif(subcontent=="Stan mieszkania:"):
                    for span in content:
                        if(len(span.attrs) == 0):
                            continue
                        if(span.attrs['class'][0])=="fheader":
                            continue
                        stan_mieszkania = stan_mieszkania + span.contents[0]

            tabela = soup.find_all(class_ = "box-offer-inside box-offer-inside__as")[0]
            
            for info in tabela:
                if(isinstance(info, NavigableString)):
                    continue
                if(info.name=="h3"):
                    continue
                for subinfo in info.contents:
                    for sub_subinfo in subinfo.contents:
                        if isinstance(sub_subinfo, NavigableString):
                            continue
                        if sub_subinfo.contents[0] == "Rynek:":
                            rynek=subinfo.contents[2].string
                        if sub_subinfo.contents[0] == "Czynsz:":
                            czynsz=subinfo.contents[2].string

            cursor_distance=conn.cursor()
            cursor_distance.execute('SELECT * FROM dbo.odleglosci WHERE adres = '+'\''+miejsce+'\'')
            if cursor_distance.rowcount == 0:
                try:
                    odleglosc_od_PKP = getDistance(miejsce, "Dworcowa 9, Piaseczno, mazowieckie")
                except:
                    odleglosc_od_PKP = 'NULL'
                try:
                    odleglosc_od_Centrum = getDistance(miejsce, "Plac Defilad 1, Warszawa, mazowieckie")
                except:
                    odleglosc_od_Centrum = 'NULL'
                sql='INSERT INTO dbo.odleglosci VALUES (\'%s\',%s,%s)' % (miejsce, odleglosc_od_PKP, odleglosc_od_Centrum,)
                cursor_distance.execute(sql)
                conn.commit()
            if cursor.rowcount == 0:
                sql_statement='INSERT INTO stg.nieruchomosci_mieszkania([url],[miejsce],[dzielnica],[pietro],[liczba_pokoi],[rok_budowy],[miejsce_parkingowe],[czynsz],[wyposazenie],[rynek],[cena],[powierzchnia],[cena_za_m2],[data_wstawienia],[agent]) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',GETDATE(),\'%s\')' % (url, miejsce, dzielnica, pietro, liczba_pokoi, rok_budowy, miejsce_parkingowe, czynsz, wyposazenie, rynek, cena, powierzchnia, cena_za_m2, agent)
                cursor.execute(sql_statement)
                conn.commit()
                cnt+=1
        ending_time = datetime.now()
        print('Execution time: ' + str((ending_time-starting_time).total_seconds()))
        try:
            url_main=soup_main.find_all(id="pagination-outer")[0].find(class_="btn-a")["href"]
        except TypeError:
            url_main=""
        conn.commit()
ending_time_global = datetime.now()
print('Execution time of the entire script: ' + str((ending_time_global-starting_time_global).total_seconds()))
print('Rows inserted: ' + str(cnt))
    
cursor_distance=conn.cursor()
cursor_distance.execute('EXEC dbo.refresh_nieruchomosci_mieszkania')
conn.commit()