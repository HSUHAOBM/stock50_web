import mysql.connector

import configparser
import os

import urllib.request as req
import bs4
from datetime import datetime


config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('aws_rd', 'DBhost')   
DBdatabase=config.get('aws_rd', 'DBdatabase')
DBuser=config.get('aws_rd', 'DBuser')
DBpassword=config.get('aws_rd', 'DBpassword')

# DBhost="localhost"
# DBdatabase="stock50_web_v2"
# DBuser="root"
# DBpassword="root"

#建立台50基本資料庫
def stock50_data():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE stock50_data  (
            stock_id int PRIMARY KEY,
            stock_name VARCHAR(25),
            date date,
            stock_total INT ,
            open_price float,
            high_price float,
            low_price float,
            end_price float,
            differ float,
            totaldeal int,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''


        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            
#建立休市資料庫
def stock50_stopdeal_date():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE stock50_stopdeal_date  (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date date,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")




#取休市資料
#取的休市的日期
def getstock50_stopdeal():
    url="https://www.twse.com.tw/zh/holidaySchedule/holidaySchedule"
    request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36"})
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8") #取的網站原始碼 編碼
    root=bs4.BeautifulSoup(data,"html.parser")
    listresult=root.find_all("td",attrs={"align":"center"})[1::2]
    
    datestr=""
    for i in listresult:
        datestr=datestr+(str(i).replace('<td align="center">',"").replace('</td>',"").replace('<br/>',",").replace('(110年),',",").replace('(111年)',"").replace('月',"/").replace('日',""))
        datestr=datestr+","
    datestr=datestr.split(",")[:-2]
    for iten in datestr:
        print(datetime.strptime(str(datetime.now().year)+"/"+iten, "%Y/%m/%d").strftime('%Y-%m-%d'))
        stock_stopdeal(datetime.strptime(str(datetime.now().year)+"/"+iten, "%Y/%m/%d").strftime('%Y-%m-%d'))

#將休市日期存入資料庫
def stock_stopdeal(date):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = "INSERT INTO stock50_stopdeal_date (date) VALUES (%s)"
        cursor = connection.cursor()
        
        cursor.execute(sql,[(date)])

        connection.commit()
        print("資料庫連線")

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")