import mysql.connector
from datetime import datetime
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')   
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')


#存50的相關資料
def stock50_everydaydata(stock_id,stock_name,data,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        sql = "INSERT INTO stock50_data (stock_id,stock_name,date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        data=(stock_id,stock_name,data,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal)
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")