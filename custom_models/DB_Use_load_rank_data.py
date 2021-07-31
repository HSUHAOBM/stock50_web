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

# 成績彙整讀取(user_name,stock_id,data_number,data_status)
def message_predict_rank_load(user_name,stock_id,data_number,data_status):
    try:
        message_predict_load_rank_list=[]

        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        cursor = connection.cursor(buffered=True)

        if(user_name==None and stock_id==None):
            if(data_status=="rate"):
                cursor.execute("select * from message_predict_rank where predict_win_rate > 0 order by cast(predict_win_rate as unsigned) DESC limit %d , %d;"%((int(data_number))*10,10))
                records = cursor.fetchall()
            if(data_status=='win'):
                cursor.execute("select * from message_predict_rank where predict_win > 0 order by cast(predict_win as unsigned) DESC limit %d , %d;"%((int(data_number))*10,10))
                records = cursor.fetchall()
            if(data_status=='total'):
                cursor.execute("select * from message_predict_rank where predict_total > 0 order by cast(predict_total as unsigned) DESC limit %d , %d;"%((int(data_number))*10,10))
                records = cursor.fetchall()
            if(data_status=='like'):
                cursor.execute("select * from message_predict_rank where predict_good > 0 order by cast(predict_good as unsigned) DESC limit %d , %d;"%((int(data_number))*10,10))
                records = cursor.fetchall()

            if(records):
                for i in range(len(records)):

                    message_predict_load_rank_list.append({
                        "member_name":records[i][0],
                        "predict_win_rate":records[i][1],
                        "predict_win":records[i][2],
                        "predict_fail":records[i][3],
                        "predict_total":records[i][4],
                        "predict_good":records[i][5],
                        "member_src":load_member_src(records[i][0])

                    })
                return message_predict_load_rank_list
            else:
                return {"No_data":True}

        if(stock_id != None):
            cursor.execute("select * from message_predict_rank_stock_info where stock_id='%s' and predict_win > 0 order by cast(predict_win_rate as unsigned) DESC limit %d , %d;"%(stock_id,(int(data_number))*5,5))
            records = cursor.fetchall()
            if(records):
                
                for i in range(len(records)):
                    message_predict_load_rank_list.append({
                        "predict_load_rank":True,
                        "stock_id":records[i][1],
                        "stock_name":records[i][2],
                        "member_name":records[i][3],
                        "predict_win_rate":records[i][4],
                        "predict_win":records[i][5],
                        "predict_fail":records[i][6],
                        "predict_total":records[i][7],
                        "member_src":load_member_src(records[i][3])
                    })
                return message_predict_load_rank_list
            else:
                return {"No_data":True}
        if(user_name != None and data_status!=None):
            if(data_status=='rate'):
                load_rank_data_return=load_rank_data_predict_win_rate(user_name)
            if(data_status=='win'):
                load_rank_data_return=load_rank_data_predict_win(user_name)
            if(data_status=='fail'):
                load_rank_data_return=load_rank_data_predict_fail(user_name)
            if(load_rank_data_return):
                for i in range(len(load_rank_data_return)):
                    message_predict_load_rank_list.append({
                        "predict_load_rank":True,
                        "stock_id":load_rank_data_return[i][1],
                        "stock_name":load_rank_data_return[i][2],
                        "member_name":load_rank_data_return[i][3],
                        "predict_win_rate":load_rank_data_return[i][4],
                        "predict_win":load_rank_data_return[i][5],
                        "predict_fail":load_rank_data_return[i][6],
                        "predict_total":load_rank_data_return[i][7]
                        # "member_src":load_member_src(load_rank_data_return[i][3])
                    })
                return message_predict_load_rank_list        
            else:
                print("無資料")
                return {"member_no_data":True,"message":"此會員無預測資料"}
        else:
            return {"error":True,"message":"錯誤"}


    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")
#load img src
def load_member_src(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("select picturesrc from member_basedata where name='%s';"%(member_name))
        records = cursor.fetchone()
        # print(records)
        return records[0]
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()




def load_rank_data_predict_win_rate(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        cursor = connection.cursor()
        cursor.execute("select * from message_predict_rank_stock_info where member_name='%s' and predict_win>0 order by cast(predict_win_rate as unsigned) DESC limit 5 ;"%(member_name))
        records = cursor.fetchall()
        # print(records)
        return records
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def load_rank_data_predict_win(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        cursor = connection.cursor()
        cursor.execute("select * from message_predict_rank_stock_info where member_name='%s' and predict_win>0 order by cast(predict_win as unsigned) DESC limit 5 ;"%(member_name))
        records = cursor.fetchall()
        return records
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

def load_rank_data_predict_fail(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        cursor = connection.cursor()
        cursor.execute("select * from message_predict_rank_stock_info where member_name='%s' and predict_fail>0 order by cast(predict_fail as unsigned) DESC limit 5 ;"%(member_name))
        records = cursor.fetchall()
        return records
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


