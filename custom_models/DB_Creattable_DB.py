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
        gender VARCHAR(255),
        address VARCHAR(255),
        picturesrc VARCHAR(255),
        level VARCHAR(255)  DEFAULT "0" NOT NULL,
        birthday date,
        registertime datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
        logingtime datetime DEFAULT CURRENT_TIMESTAMP,
        ip VARCHAR(255) );'''



    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    cursor.close()
    connection.close()


#建立留言預測的資料庫
def message_predict():
    connection = mysql.connector.connect(
    host=DBhost,         
    database=DBdatabase, 
    user=DBuser,      
    password=DBpassword) 

    sql = '''CREATE TABLE message_predict  (
        no INT AUTO_INCREMENT PRIMARY KEY,
        mid VARCHAR(25) NOT NULL,
        account VARCHAR(25) NOT NULL,
        stock_id VARCHAR(25) NOT NULL,
        stock_name VARCHAR(25) NOT NULL,
        stock_state VARCHAR(25) NOT NULL,
        text VARCHAR(300) NOT NULL,
        check_status VARCHAR(25) DEFAULT "0" NOT NULL,
        time datetime DEFAULT CURRENT_TIMESTAMP);'''

    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    cursor.close()
    connection.close()


