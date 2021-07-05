
import mysql.connector
from datetime import datetime,date
import configparser
import os
import time

import DB_Use_message,DB_Get_stock50_everydaydata

config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')   
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')

#取得休市日期
def DB_get_stopdealdate():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("SELECT date FROM stock50_stopdeal_date")
        records = cursor.fetchall()

            
        return(records)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")




#設定爬取時間為下午1點45分
def main(h=10,m=16,wd1=6,wd2=7):
    while True:
        print("現在時間為",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        trun_get=True
        for i in stopdeal_date:
            if(datetime.now().month == i[0].month):
                if(datetime.now().day == i[0].day):
                    print("國定假日，休市")
                    trun_get=False

                
        if(trun_get):
            now = datetime.now()
            if now.isoweekday()!=wd1 and now.isoweekday()!=wd2:            
                if now.hour == h and now.minute == m :
                    print("今天有開市，並將開始執行爬蟲")
                    doSth()
                else:
                    print("今天有開市，但未收盤或已執行。")
            else: 
                print("休市")


        time.sleep(60)
        print("-持續監控中-")

def doSth():
    print("取得最新的股市資料")
    DB_Get_stock50_everydaydata.stock50_getdata() #取得最新的股市資料
    
    print("留言資料的檢測")
    DB_Use_message.message_predict_check() #留言資料的檢測


stopdeal_date=DB_get_stopdealdate()
main()