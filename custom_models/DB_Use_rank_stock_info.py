import re
import mysql.connector
from datetime import datetime

import connection_pool



# 各股排行彙整：股票名>會員名>資料>資料庫
def message_predict_rank_update_stock_info_main():
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()


        cursor.execute("select stock_id,stock_name from stock50 ORDER BY stock_id")
        records = cursor.fetchall()
        for stock_id_ in range(len(records)):
            print("現在執行",records[stock_id_][0],records[stock_id_][1],"的檢查")
            message_predict_rank_update_stock_info_get_data_to_db(records[stock_id_][0],records[stock_id_][1])
            
    finally:
        cursor.close()
        connection.close()

#整理數據進資料庫 會員名>資料>資料庫
def message_predict_rank_update_stock_info_get_data_to_db(stock_id,stock_name):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select id from member_basedata ")
        records = cursor.fetchall()
        for member_ in range(len(records)):
            checkdata=message_predict_rank_update_select_total_stock_info_check(records[member_][0],stock_id)
            if(checkdata):
                # print("會員:",records[member_][0],"有",stock_id,"的資料")
                predict_total=message_predict_rank_update_select_total_stock_info(records[member_][0],stock_id)
                predict_win=message_predict_rank_update_select_win_stock_info(records[member_][0],stock_id)
                predict_fail=predict_total-predict_win
                predict_win_rate=int(round(predict_win/predict_total,2)*100)
                message_predict_rank_add_stock_info(stock_id,stock_name,records[member_][0],predict_win_rate,predict_win,predict_fail,predict_total)

    finally:
        cursor.close()
        connection.close()


#資料
def message_predict_rank_update_select_total_stock_info(id,stock_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select count(*) from message_predict where user_id='%s' and stock_id='%s' ;"%(id,stock_id))
        records = cursor.fetchone()
        return records[0]
    finally:
        cursor.close()
        connection.close()


def message_predict_rank_update_select_win_stock_info(id,stock_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()


        cursor.execute("select count(*) from message_predict where user_id='%s' and check_status=1 and stock_id='%s';"%(id,stock_id))
        records = cursor.fetchone()
        return records[0]
    finally:
        cursor.close()
        connection.close()


#資料：確認有預測過
def message_predict_rank_update_select_total_stock_info_check(member_name,stock_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select user_id from message_predict where user_id='%s' and stock_id='%s' LIMIT 1 ;"%(member_name,stock_id))
        records = cursor.fetchone()
        if(records):
            return True
        else:
            return False
    finally:
        cursor.close()
        connection.close()


#資料庫
def message_predict_rank_add_stock_info(stock_id,stock_name,id,predict_win_rate,predict_win,predict_fail,predict_total):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        
        cursor.execute("select user_id from predict_rank_stock_info where user_id='%s' and stock_id='%s' LIMIT 1;"%(id,stock_id))
        records = cursor.fetchone()
        
        if(records):
            print(stock_id,"會員",id,"已有資料_更新")                
            cursor = connection.cursor()
            cursor.execute("UPDATE predict_rank_stock_info SET win_rate ='%s',win='%s' ,fail='%s',total='%s' where user_id='%s' and stock_id='%s';"%(predict_win_rate,predict_win,predict_fail,predict_total,id,stock_id))
            connection.commit()
        else:
            print(stock_id,"會員無",id,"資料_新增")                
            sql = "INSERT INTO predict_rank_stock_info (stock_id,user_id,win_rate,win,fail,total) VALUES (%s,%s,%s,%s,%s,%s);"
            data=(stock_id,id,predict_win_rate,predict_win,predict_fail,predict_total)
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()    
    finally:
        cursor.close()
        connection.close()








