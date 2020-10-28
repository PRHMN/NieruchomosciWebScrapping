import requests
from bs4 import BeautifulSoup
import pyodbc
from datetime import datetime

starting_time = datetime.now()

cnt = -1
server = 'LAPTOP-6FDB4KPM' 
database = 'NieruchomosciScrapping' 

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';'+'Trusted_Connection=yes;')


while(cnt!=0): 
    cnt=0
    url = "https://www.otodom.pl/sprzedaz/dzialka/piaseczno/budowlana/?search%5Bfilter_float_m%3Afrom%5D=900&search%5Bfilter_float_m%3Ato%5D=1300&search%5Bdescription%5D=1&search%5Bregion_id%5D=7&search%5Bsubregion_id%5D=184&search%5Bcity_id%5D=811&search%5Bdist%5D=5&nrAdsPerPage=72"
    while(url!=""):

        odpowiedz = requests.get(url)
        html_doc = odpowiedz.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        articles = soup.find_all("article")
        for article in articles:
            miejsce = article.find_all(class_="text-nowrap")[1].contents[1].replace("\n","")
            cena = article.find(class_="offer-item-price").text.replace(" ","")
            powierzchnia = article.find(class_="visible-xs-block").text
            cena_za_m2 = article.find(class_="hidden-xs offer-item-price-per-m").text
            url=article.find("h3").contents[1]["href"]
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM dbo.otodom WHERE url = '+'\''+url+'\'')
            if cursor.rowcount == 0:
                sql_statement='INSERT INTO dbo.otodom VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',GETDATE(), 1)' % (url, miejsce, cena, powierzchnia, cena_za_m2)
                cursor.execute(sql_statement) 
                cnt = cnt+1 
        url=soup.find(class_="pager-next").contents[1]["href"]   
    conn.commit() 
    ending_time = datetime.now()
    print('Execution time: ' + str((ending_time-starting_time).total_seconds()))
    print('Rows inserted: ' + str(cnt))

