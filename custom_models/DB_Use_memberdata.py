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


#會員註冊
def member_registered (email,password,name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        #檢查是否註冊過
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM member_basedata WHERE name= '%s' or email='%s';" % (name,email))
        records = cursor.fetchone()

            
        if (records):
            print("註冊過了")
            return {"error": True, "message": "暱稱或信箱重複註冊!"}
            
        else:
            print("開始新增")
            #指令
            sql = "INSERT INTO member_basedata (email,password,name) VALUES (%s,%s,%s);"
            member_data = (email,password,name)
            cursor = connection.cursor()
            cursor.execute(sql, member_data)
            connection.commit()
            return {"ok": True, "message": "註冊成功!"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")


#會員登入
def member_signin(email,password):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        #檢查是否註冊過
        cursor = connection.cursor()
        cursor.execute("SELECT name,password FROM member_basedata WHERE email= '%s';" % (email))
        records = cursor.fetchone()
        if (records):
            print("帳號正確。。。開始檢查密碼")

            if (password==records[1]):
                print("密碼驗證成功")
                return {"ok": True}
            else:
                print("密碼錯誤")
                return {"error": True, "message": "帳號或密碼錯誤"}
        else:
            print("帳號錯誤")
            return {"error": True, "message": "帳號或密碼錯誤"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")