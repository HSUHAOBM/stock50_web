import re
import mysql.connector
from datetime import datetime
import connection_pool



#讀取排行數據並存資料庫
def message_predict_rank_update():
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        cursor.execute("select id from member_basedata")
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
        cursor.close()
        connection.close()

#取得總預測數            
def message_predict_rank_update_select_total(id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        cursor.execute("select count(*) from message_predict where user_id='%s';"%(id))
        records = cursor.fetchone()
        return records[0]
    finally:
        cursor.close()
        connection.close()


#取得總成功數
def message_predict_rank_update_select_win(id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select count(*) from message_predict where user_id='%s' and check_status=1;"%(id))
        records = cursor.fetchone()
        return records[0]
    finally:
        cursor.close()
        connection.close()


#將數據送進資料庫
def message_predict_rank_add(id,predict_win_rate,predict_win,predict_fail,predict_total,predict_good):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        
        cursor.execute("select user_id from predict_rank where user_id='%s' limit 1;"%(id))
        records = cursor.fetchone()
        if(records):
            print("會員已有資料_更新")                
            cursor = connection.cursor()
            cursor.execute("UPDATE predict_rank SET win_rate ='%s',win='%s' ,fail='%s',total='%s',good='%s' where user_id='%s';"%(predict_win_rate,predict_win,predict_fail,predict_total,predict_good,id))
            connection.commit()
        else:
            print("會員無資料_新增")                

            sql = "INSERT INTO predict_rank (user_id,win_rate,win,fail,total,good) VALUES (%s,%s,%s,%s,%s,%s);"
            data=(id,predict_win_rate,predict_win,predict_fail,predict_total,predict_good)
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()    
    finally:
        cursor.close()
        connection.close()


#檢查會員有無預測
def message_predict_rank_update_select_total_check(id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select user_id from message_predict where user_id='%s' LIMIT 1 ;"%(id))
        records = cursor.fetchone()
        if(records):
            return True
        else:
            return False
    finally:
        cursor.close()
        connection.close()




#會員總共有多少讚
def member_message_predict_like_number(id):
    connection = connection_pool.getConnection()
    connection = connection.connection()
    
    sql ='''SELECT count(*) from message_predict_good
    Inner join message_predict on message_predict_good.mid=message_predict.mid
    WHERE message_predict.user_id= '%s' '''
    
    cursor = connection.cursor()
    cursor.execute(sql%id)
    records = cursor.fetchone()
        
    return records[0]