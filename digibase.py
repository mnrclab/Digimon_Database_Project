# '''LATIHAN web scrapping digimon dan disimpan ke database'''

from bs4 import BeautifulSoup
import requests

url = 'http://digidb.io/digimon-list/'
web = requests.get(url)
data = BeautifulSoup(web.content, 'html.parser')

#MENDAPATKAN DATA DARI TAG 'TD'
td = data.find_all('td')

list = []
List_OL = []
for i in td:
    if len(list) == 0:
        list.append(i.text[1:])
    elif len(list) == 1:
        list.append(i.text[2:])
    else:
        list.append(i.text)
        if len(list) == 13:
            List_OL.append(list)
            list = []

#MENCARI DATA DARI TAG 'img'
td_img = data.find_all('img')
td_img = td_img[2:-2]
for i in td_img:
    List_OL[td_img.index(i)].insert(14, i['src'])

#MENDAPATKAN NAMA KOLOM
Data_Tupple = []
for i in List_OL:
    k = tuple(i)
    Data_Tupple.append(k)

# MEMBUAT DATABASE
import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'kahfi2008',
    database = 'digimon'
)


c = db.cursor()
sql = 'insert into digibase (No, Digimon, Stage, Type, Attribute, Memory, Equip_Slots, HP, SP, Atk, Def, Init, Spd, Image) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
c.executemany(sql, Data_Tupple)
db.commit()
# print(c.rowcount, 'Data tersimpan')