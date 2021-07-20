import mysql.connector

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
            password VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            gender VARCHAR(255) DEFAULT '無',
            address VARCHAR(255) DEFAULT '無',
            picturesrc VARCHAR(255) DEFAULT 'img/peo.png',
            level VARCHAR(255)  DEFAULT "0" NOT NULL,
            birthday date DEFAULT '19910101',
            introduction VARCHAR(255) DEFAULT '無', 
            interests VARCHAR(255) DEFAULT '無',
            registertime datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
            logingtime datetime DEFAULT CURRENT_TIMESTAMP,
            ip VARCHAR(255) );'''



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
            text VARCHAR(1280) ,
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
            mid VARCHAR(25) NOT NULL,
            like_message_user_name VARCHAR(200) NOT NULL,
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
            message_reply_text VARCHAR(1280) NOT NULL,
            time datetime DEFAULT CURRENT_TIMESTAMP);'''

        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")