import re
import mysql.connector
from datetime import datetime
import configparser
import os
import time


config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')   
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')

def load_stock_data(stock_id):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("select * from stock50_data where stock_id='%s'order by time desc limit 1;"%(stock_id))
        records = cursor.fetchone()

        return {"stock_id":records[1],"stock_name":records[2],"date":records[3].strftime('%Y-%m-%d'),
        "total":records[4],"open_price":records[5],"high_price":records[6],"low_price":records[7],
        "end_price":records[8],"differ":records[9],"total_deal":records[10],"update_time":records[11].strftime('%Y-%m-%d %H:%M')}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


