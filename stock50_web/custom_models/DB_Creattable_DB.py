
import configparser
import os
import requests
import json
import pymysql

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


#會員基本資料的資料庫
def member_basedata():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:

            sql = '''CREATE TABLE member_basedata  (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(64) NOT NULL,
                password VARCHAR(64) NOT NULL,
                name VARCHAR(20) UNIQUE NOT NULL ,
                gender VARCHAR(1) DEFAULT '無',
                address VARCHAR(5) DEFAULT '無',
                picturesrc VARCHAR(255) DEFAULT 'img/peo.png',
                level VARCHAR(1)  DEFAULT "0" NOT NULL,
                authentication VARCHAR(1)  DEFAULT "0" NOT NULL,
                birthday date,
                introduction VARCHAR(255) DEFAULT '無',
                interests VARCHAR(24) DEFAULT '無',
                registertime datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
                logingtime datetime DEFAULT CURRENT_TIMESTAMP,
                ip VARCHAR(30),
                index(name) )
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#建立留言預測的資料庫
def message_predict():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            sql = '''CREATE TABLE message_predict  (
                mid VARCHAR(25) NOT NULL PRIMARY KEY,
                user_id int NOT NULL,
                stock_id VARCHAR(10) NOT NULL,
                stock_state VARCHAR(2) NOT NULL,
                text VARCHAR(250) ,
                check_status VARCHAR(2) DEFAULT "0" NOT NULL,
                time datetime DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES member_basedata(id))
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#建立留言預測 讚 的資料庫
def message_predict_good():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:

            sql = '''CREATE TABLE message_predict_good  (
                no INT AUTO_INCREMENT PRIMARY KEY,
                mid VARCHAR(25) NOT NULL ,
                like_id int NOT NULL,
                time datetime DEFAULT CURRENT_TIMESTAMP,
                KEY `mid` (`mid`),
                FOREIGN KEY(mid) REFERENCES message_predict(mid) ON DELETE CASCADE ON UPDATE CASCADE)
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#建立留言預測<回覆>的資料庫
def message_predict_reply():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:
            sql = '''CREATE TABLE message_predict_reply  (
                no INT AUTO_INCREMENT PRIMARY KEY,
                mid VARCHAR(25) NOT NULL ,
                mid_reply VARCHAR(25) NOT NULL,
                user_id int NOT NULL,
                text VARCHAR(200) NOT NULL,
                time datetime DEFAULT CURRENT_TIMESTAMP,
                KEY `mid` (`mid`),
                FOREIGN KEY(mid) REFERENCES message_predict(mid) ON DELETE CASCADE ON UPDATE CASCADE)
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#建立成績彙整表_會員統整
def message_predict_rank():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:

            sql = '''CREATE TABLE predict_rank (
                user_id int NOT NULL PRIMARY KEY,
                win_rate VARCHAR(5),
                win VARCHAR(10),
                fail VARCHAR(10),
                total VARCHAR(10),
                good VARCHAR(10),
                time datetime DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES member_basedata(id) )
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#建立成績彙整表_各股
def message_predict_rank_stock_info():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:

            sql = '''CREATE TABLE predict_rank_stock_info (
                no INT AUTO_INCREMENT PRIMARY KEY,
                stock_id VARCHAR(10) NOT NULL,
                user_id int NOT NULL,
                win_rate VARCHAR(5),
                win VARCHAR(10),
                fail VARCHAR(10),
                total VARCHAR(10),

                KEY `user_id` (`user_id`),
                KEY `stock_id` (`stock_id`),

                time datetime DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES member_basedata(id))
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#建立台灣50名單資料庫
def stock50_db_creat():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:

            sql = '''CREATE TABLE stock50  (
                stock_id int NOT NULL PRIMARY KEY,
                stock_name VARCHAR(25) UNIQUE NOT NULL,
                time datetime DEFAULT CURRENT_TIMESTAMP)
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''

            cursor.execute(sql)
    except Exception as ex:
        print(ex)

#建立私人訊息的資料庫
def private_message_creat():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:

            sql = '''CREATE TABLE private_message  (
                no INT AUTO_INCREMENT PRIMARY KEY,
                user_id int NOT NULL ,
                text VARCHAR(100) NOT NULL,
                user_id_to int NOT NULL,

                KEY `user_id` (`user_id`),
                KEY `user_id_to` (`user_id_to`),

                time datetime DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES member_basedata(id))
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''


            cursor.execute(sql)
    except Exception as ex:
        print(ex)


#站內訊息的資料庫
def contact_message_creat():
    try:
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:

            sql = '''CREATE TABLE contact_message  (
                no INT AUTO_INCREMENT PRIMARY KEY,
                user_id int NOT NULL ,
                text VARCHAR(100) NOT NULL,
                KEY `user_id` (`user_id`),
                time datetime DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES member_basedata(id))
                ENGINE=InnoDB DEFAULT CHARSET=utf8;'''


            cursor.execute(sql)
    except Exception as ex:
        print(ex)
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
        conn = pymysql.connect(**db_settings)

        with conn.cursor() as cursor:

            sql = "INSERT INTO stock50 (stock_id,stock_name) VALUES (%s,%s);"
            data=(stock_id,stock_name)
            cursor.execute(sql, data)
            conn.commit()
    except Exception as ex:
        print(ex)
# ----------------------------------------------#
