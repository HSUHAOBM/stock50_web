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

#留言板_預測留言
def message_predict_input(account,stock_id,stock_name,stock_state,text):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword)  

        cursor = connection.cursor()
        sql = "INSERT INTO message_predict (mid,account,stock_id,stock_name,stock_state,text) VALUES (%s,%s,%s,%s,%s,%s);"
        mid=message_select_mid()
        data=(mid,account,stock_id,stock_name,stock_state,text)
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")


#功能-留言板流水號製作
def message_select_mid():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        sql = "SELECT mid from message_predict ORDER BY time DESC"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchone()
        if(records):
            #print(records[0].split("_")[-1])#現在的流水號
            print("留言編號:","mid_"+str(int(records[0].split("_")[-1])+1))
            return "mid_"+str(int(records[0].split("_")[-1])+1)
        else:
            print("預測留言資料庫是空的，開始建立新編號")
            return "mid_1"
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


#留言板_預測檢測
def message_predict_check():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        sql = "select mid,account,stock_id,stock_state from message_predict where check_status=0"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        for message_data in records:
            stock50_check(message_data[0],message_data[1],message_data[2],message_data[3])
        return {"ok": True, "message": "會員預測留言檢查完成"}

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#檢查預測留言值有無成功
def stock50_check(mid,account,stock_id,stock_state):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()

        cursor.execute("select differ from stock50_data WHERE stock_id= '%s' ORDER BY date DESC;" % (stock_id))
        records = cursor.fetchone()
        if stock_state =="1" and records[0]>0:
            message_predict_check_correct(mid)
        elif stock_state =="0" and records[0]==0:
            message_predict_check_correct(mid)
        elif stock_state =="-1" and records[0]<0:
            message_predict_check_correct(mid)
        
        else:
            message_predict_check_error(mid)
        return records
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#預測留言成功
def message_predict_check_correct(mid):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        
        cursor.execute("UPDATE message_predict SET check_status='1' where mid='%s';"%(mid))
        connection.commit()
        return {"ok": True, "message": "預測成功，結果已上傳資料庫"}

        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")


#預測留言失敗
def message_predict_check_error(mid):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        
        cursor.execute("UPDATE message_predict SET check_status='-1' where mid='%s';"%(mid))
        connection.commit()
        return {"ok": True, "message": "預測失敗，結果已上傳資料庫"}

        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")