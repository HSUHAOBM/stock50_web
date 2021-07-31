import mysql.connector

import configparser
import os
import requests
import json

config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')   
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')

#會員基本資料的資料庫
def member_basedata():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE member_basedata  (
            no INT AUTO_INCREMENT PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(128) NOT NULL,
            name VARCHAR(50) UNIQUE NOT NULL ,
            gender VARCHAR(4) DEFAULT '無',
            address VARCHAR(255) DEFAULT '無',
            picturesrc VARCHAR(255) DEFAULT 'img/peo.png',
            level VARCHAR(1)  DEFAULT "0" NOT NULL,
            authentication VARCHAR(1)  DEFAULT "0" NOT NULL,
            birthday date,
            introduction VARCHAR(255) DEFAULT '無', 
            interests VARCHAR(255) DEFAULT '無',
            registertime datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
            logingtime datetime DEFAULT CURRENT_TIMESTAMP,
            ip VARCHAR(30) );'''



        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#建立留言預測的資料庫
def message_predict():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE message_predict  (
            no INT AUTO_INCREMENT PRIMARY KEY,
            mid VARCHAR(25) NOT NULL,
            message_user_email VARCHAR(200) NOT NULL,
            message_user_name VARCHAR(200) NOT NULL,
            message_user_imgsrc VARCHAR(200) NOT NULL,
            stock_id VARCHAR(25) NOT NULL,
            stock_name VARCHAR(25) NOT NULL,
            stock_state VARCHAR(25) NOT NULL,
            text VARCHAR(250) ,
            check_status VARCHAR(25) DEFAULT "0" NOT NULL,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#建立留言預測 讚 的資料庫
def message_predict_good():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE message_predict_good  (
            no INT AUTO_INCREMENT PRIMARY KEY,
            mid_member VARCHAR(25) NOT NULL,
            mid VARCHAR(25) NOT NULL,
            like_message_user_name VARCHAR(50) NOT NULL,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#建立留言預測<回覆>的資料庫
def message_predict_reply():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE message_predict_reply  (
            no INT AUTO_INCREMENT PRIMARY KEY,
            mid VARCHAR(25) NOT NULL,
            mid_reply VARCHAR(25) NOT NULL,
            message_reply_user_email VARCHAR(200) NOT NULL,
            message_reply_user_name VARCHAR(200) NOT NULL,
            message_reply_user_imgsrc VARCHAR(200) NOT NULL,
            message_reply_text VARCHAR(200) NOT NULL,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#建立成績彙整表_會員統整
def message_predict_rank():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE message_predict_rank (
            member_name VARCHAR(50) UNIQUE NOT NULL ,
            predict_win_rate VARCHAR(5),
            predict_win VARCHAR(10),
            predict_fail VARCHAR(10),
            predict_total VARCHAR(10),
            predict_good VARCHAR(10),
            time datetime DEFAULT CURRENT_TIMESTAMP);'''
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#建立成績彙整表_各股
def message_predict_rank_stock_info():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE message_predict_rank_stock_info (
            no INT AUTO_INCREMENT PRIMARY KEY,
            stock_id VARCHAR(10) NOT NULL,
            stock_name VARCHAR(10) NOT NULL,
            member_name VARCHAR(50) NOT NULL ,
            predict_win_rate VARCHAR(5),
            predict_win VARCHAR(10),
            predict_fail VARCHAR(10),
            predict_total VARCHAR(10),
            time datetime DEFAULT CURRENT_TIMESTAMP);'''
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

#建立台灣50名單資料庫
def stock50_db_creat():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        cursor = connection.cursor()

        sql = '''CREATE TABLE stock50  (
            stock_id int UNIQUE NOT NULL ,
            stock_name VARCHAR(25) UNIQUE NOT NULL,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#建立私人訊息的資料庫
def private_message_creat():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        sql = '''CREATE TABLE private_message  (
            no INT AUTO_INCREMENT PRIMARY KEY,
            private_message_member VARCHAR(25) NOT NULL,
            private_message_src VARCHAR(225) NOT NULL,
            private_message_text VARCHAR(100) NOT NULL,
            private_message_member_to VARCHAR(25) NOT NULL,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
# ----------------------------------------------#
#取得台灣50並存資料庫
def get_stock50_id():
    url_tese='https://www.yuantaetfs.com/api/Composition?fundid=1066'
    res= requests.get(url_tese)
    stock50_namedata = json.loads(res.text)
    for i in range(len(stock50_namedata)):
        stock50_db_add(stock50_namedata[i]["stkcd"],stock50_namedata[i]["name"])
#台50存資料庫
def stock50_db_add(stock_id,stock_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        cursor = connection.cursor()

        sql = "INSERT INTO stock50 (stock_id,stock_name) VALUES (%s,%s);"
        data=(stock_id,stock_name)
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()   


    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
# ----------------------------------------------#
