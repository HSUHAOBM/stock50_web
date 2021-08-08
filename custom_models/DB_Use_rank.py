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
        cursor.close()
        connection.close()

#取得總預測數            
def message_predict_rank_update_select_total(member_name):
    connection = connection_pool.getConnection()
    connection = connection.connection()
    cursor = connection.cursor()
    cursor.execute("select count(*) from message_predict where message_user_name='%s';"%(member_name))
    records = cursor.fetchone()
    return records[0]

#取得總成功數
def message_predict_rank_update_select_win(member_name):
    connection = connection_pool.getConnection()
    connection = connection.connection()
    cursor = connection.cursor()

    cursor.execute("select count(*) from message_predict where message_user_name='%s' and check_status=1;"%(member_name))
    records = cursor.fetchone()
    return records[0]


#將數據送進資料庫
def message_predict_rank_add(member_name,predict_win_rate,predict_win,predict_fail,predict_total,predict_good):
    connection = connection_pool.getConnection()
    connection = connection.connection()
    cursor = connection.cursor()
    
    cursor.execute("select member_name from message_predict_rank where member_name='%s' limit 1;"%(member_name))
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


#檢查會員有無預測
def message_predict_rank_update_select_total_check(member_name):
    connection = connection_pool.getConnection()
    connection = connection.connection()
    cursor = connection.cursor()

    cursor.execute("select message_user_name from message_predict where message_user_name='%s' LIMIT 1 ;"%(member_name))
    records = cursor.fetchone()
    if(records):
        return True
    else:
        return False




#會員總共有多少讚
def member_message_predict_like_number(member_name):
    connection = connection_pool.getConnection()
    connection = connection.connection()
    cursor = connection.cursor()

    cursor.execute("SELECT count(*) FROM message_predict_good WHERE mid_member= '%s' ;" % (member_name))
    records = cursor.fetchone()
        
    return records[0]
