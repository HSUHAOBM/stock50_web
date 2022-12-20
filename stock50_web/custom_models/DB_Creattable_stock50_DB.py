import pymysql

import configparser
import os

import urllib.request as req
import bs4
from datetime import datetime


config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')

db_settings = {
    "host": DBhost,
    "user": DBuser,
    "password": DBpassword,
    "db": DBdatabase,
}


#建立台50基本資料庫
def stock50_data():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            sql = '''CREATE TABLE stock50_data  (
                no INT AUTO_INCREMENT PRIMARY KEY,
                stock_id int ,
                stock_name VARCHAR(25),
                date date,
                stock_total INT ,
                open_price float,
                high_price float,
                low_price float,
                end_price float,
                differ float,
                totaldeal int,
                time datetime DEFAULT CURRENT_TIMESTAMP)
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#建立休市資料庫
def stock50_stopdeal_date():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            sql = '''CREATE TABLE stock50_stopdeal_date  (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date date,
                time datetime DEFAULT CURRENT_TIMESTAMP)
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#取休市資料
#取的休市的日期
def getstock50_stopdeal():
    url="https://www.twse.com.tw/zh/holidaySchedule/holidaySchedule"
    request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"})
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8") #取的網站原始碼 編碼
    root = bs4.BeautifulSoup(data,"html.parser")

    listresult = root.find_all("td",attrs={"align":"center"})[1::2]
    # print(listresult)

    datestr=""
    for i in listresult:
        # print(str(i).replace('<td align="center">',"").replace('</td>',""))
        datestr = datestr+(str(i).replace('<td align="center">',"").replace('</td>',"").replace('<br/>',",").replace('(110年),',",").replace('(111年)',"").replace('月',"/").replace('日',""))
        datestr = datestr+","

    datestr = datestr.split(",")[:-2]
    # print('datestr',datestr)

    for iten in datestr:
        if iten:
            if '</br>' in iten:
                iten_ = iten.split("</br>")
                stock_stopdeal(datetime.strptime(str(datetime.now().year)+"/"+ iten_[0], "%Y/%m/%d").strftime('%Y-%m-%d'))
                # print(datetime.strptime(str(datetime.now().year)+"/"+ iten_[0], "%Y/%m/%d").strftime('%Y-%m-%d'))

            elif '<br>' in iten:
                iten_ = iten.split("<br>")
                for i in iten_ :
                    stock_stopdeal(datetime.strptime(str(datetime.now().year)+"/"+i, "%Y/%m/%d").strftime('%Y-%m-%d'))
                    # print(datetime.strptime(str(datetime.now().year)+"/"+i, "%Y/%m/%d").strftime('%Y-%m-%d'))
            else:
                stock_stopdeal(datetime.strptime(str(datetime.now().year)+"/"+iten, "%Y/%m/%d").strftime('%Y-%m-%d'))
                # print(datetime.strptime(str(datetime.now().year)+"/"+iten, "%Y/%m/%d").strftime('%Y-%m-%d'))

# #將休市日期存入資料庫
def stock_stopdeal(date):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            sql = "INSERT INTO stock50_stopdeal_date (date) VALUES (%s)"
            cursor.execute(sql,date)
            conn.commit()
    except Exception as ex:
        print(ex)