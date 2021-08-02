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



#讀取排行數據並存資料庫
def message_predict_rank_update():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("select name from member_basedata")
        records = cursor.fetchall()
        for member_ in range(len(records)):
            check_data=message_predict_rank_update_select_total_check(records[member_][0])
            if(check_data):
                predict_total=message_predict_rank_update_select_total(records[member_][0])
                predict_win=message_predict_rank_update_select_win(records[member_][0])
                predict_fail=predict_total-predict_win
                predict_win_rate=int(round(predict_win/predict_total,2)*100)
                predict_good=member_message_predict_like_number(records[member_][0])
                # print(predict_total,predict_win,predict_fail,predict_win_rate)
                message_predict_rank_add(records[member_][0],predict_win_rate,predict_win,predict_fail,predict_total,predict_good)
                
        return "排行數據已更新"
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

#取得總預測數            
def message_predict_rank_update_select_total(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("select count(*) from message_predict where message_user_name='%s';"%(member_name))
        records = cursor.fetchone()
        return records[0]

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
#取得總成功數
def message_predict_rank_update_select_win(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("select count(*) from message_predict where message_user_name='%s' and check_status=1;"%(member_name))
        records = cursor.fetchone()
        return records[0]
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
#將數據送進資料庫
def message_predict_rank_add(member_name,predict_win_rate,predict_win,predict_fail,predict_total,predict_good):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        cursor = connection.cursor()
        
        cursor.execute("select member_name from message_predict_rank where member_name='%s';"%(member_name))
        records = cursor.fetchone()
        if(records):
            print("會員已有資料_更新")                
            cursor = connection.cursor()
            cursor.execute("UPDATE message_predict_rank SET predict_win_rate ='%s',predict_win='%s' ,predict_fail='%s',predict_total='%s',predict_good='%s' where member_name='%s';"%(predict_win_rate,predict_win,predict_fail,predict_total,predict_good,member_name))
            connection.commit()
        else:
            print("會員無資料_新增")                

            sql = "INSERT INTO message_predict_rank (member_name,predict_win_rate,predict_win,predict_fail,predict_total,predict_good) VALUES (%s,%s,%s,%s,%s,%s);"
            data=(member_name,predict_win_rate,predict_win,predict_fail,predict_total,predict_good)
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()    
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


#檢查會員有無預測
def message_predict_rank_update_select_total_check(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("select * from message_predict where message_user_name='%s' LIMIT 1 ;"%(member_name))
        records = cursor.fetchone()
        if(records):
            return True
        else:
            return False

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


#會員總共有多少讚
def member_message_predict_like_number(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        cursor = connection.cursor()
        cursor.execute("SELECT count(*) FROM message_predict_good WHERE mid_member= '%s' ;" % (member_name))
        records = cursor.fetchone()
            
        return records[0]
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()