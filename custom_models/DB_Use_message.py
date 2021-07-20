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

#留言板_預測留言
def message_predict_add(message_user_email,message_user_name,message_user_imgsrc,stock_id,stock_name,stock_state,text):
    try:
        # print(message_user_email,message_user_name,message_user_imgsrc,stock_id,stock_name,stock_state,text)
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword)  

        cursor = connection.cursor()
        sql = "INSERT INTO message_predict (mid,message_user_email,message_user_name,message_user_imgsrc,stock_id,stock_name,stock_state,text) VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"
        mid=message_select_mid()
        data=(mid,message_user_email,message_user_name,message_user_imgsrc,stock_id,stock_name,stock_state,text)
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()

        return {"ok":True,"mid":mid,"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")


#功能-留言板流水號製作
def message_select_mid():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        sql = "SELECT mid from message_predict ORDER BY time DESC"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchone()
        if(records):
            #print(records[0].split("_")[-1])#現在的流水號
            # print("留言編號:","mid_"+str(int(records[0].split("_")[-1])+1))
            return "mid_"+str(int(records[0].split("_")[-1])+1)
        else:
            print("預測留言資料庫是空的，開始建立新編號")
            return "mid_1"
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

#-----------------------*

#留言板_預測檢測
def message_predict_check():
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        sql = "select mid,message_user_email,stock_id,stock_state from message_predict where check_status=0"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        for message_data in records:
            stock50_check(message_data[0],message_data[1],message_data[2],message_data[3])
        return {"ok": True, "message": "會員預測留言檢查完成"}

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

#檢查預測留言值有無成功
def stock50_check(mid,account,stock_id,stock_state):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()

        cursor.execute("select differ from stock50_data WHERE stock_id= '%s' ORDER BY date DESC;" % (stock_id))
        records = cursor.fetchone()
        if stock_state =="1" and records[0]>0:
            message_predict_check_correct(mid)
        elif stock_state =="0" and records[0]==0:
            message_predict_check_correct(mid)
        elif stock_state =="-1" and records[0]<0:
            message_predict_check_correct(mid)
        
        else:
            message_predict_check_error(mid)
        return records
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

#預測留言成功
def message_predict_check_correct(mid):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        
        cursor.execute("UPDATE message_predict SET check_status='1' where mid='%s';"%(mid))
        connection.commit()
        return {"ok": True, "message": "預測成功，結果已上傳資料庫"}

        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")


#預測留言失敗
def message_predict_check_error(mid):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        
        cursor.execute("UPDATE message_predict SET check_status='-1' where mid='%s';"%(mid))
        connection.commit()
        return {"ok": True, "message": "預測失敗，結果已上傳資料庫"}

        
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

#-----------------------*



#預測留言讀取(member_name,user_name,data_keyword)
def message_predict_load(member_name,user_name,data_keyword,data_number,data_status):
    try:
        message_predict_load_list=[]

        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        cursor = connection.cursor(buffered=True)
        if(user_name==None and data_keyword==None  and data_status==None):
            # cursor.execute("Select * from taipei_trip limit %d , %d;"%((int(WebPage))*12,12)) 


            cursor.execute("select * from message_predict order by time DESC limit %d , %d;"%((int(data_number))*5,5))
            records = cursor.fetchall()

        if(user_name!=None):
            #檢查有無會員
            cursor.execute("select * from member_basedata where name ='%s';"%(user_name))
            records = cursor.fetchone()
            
            if(records):
                cursor = connection.cursor()
                cursor.execute("select * from message_predict where message_user_name ='%s'order by time DESC limit %d , %d;"%(user_name,(int(data_number))*5,5))
                records = cursor.fetchall()
            else:
                print("無此會員")

                return {"error":True,"message":"無資料"}
                

        if(data_keyword!=None):
            #檢查有無股票資料
            cursor.execute("select * from stock50_data where stock_id ='%s' limit 1 ;"%(data_keyword))
            records = cursor.fetchone() 
            
            if(records):
                cursor = connection.cursor()
                cursor.execute("select * from message_predict where stock_id ='%s'order by time DESC limit %d , %d;"%(data_keyword,(int(data_number))*5,5))
                records = cursor.fetchall()   
            else:
                print("股市代號輸入錯誤")
                return {"error":True,"message":"無資料"}

        print(len(records))
        if(len(records)==0):
            return False
        else:
            for i in range(len(records)):
                message_predict_like_check_return=message_predict_like_check(records[i][1],member_name)
                message_predict_like_number_return=message_predict_like_number(records[i][1])
                message_predict_reply_number_return=message_predict_reply_number(records[i][1])
                message_predict_reply_load_return=message_predict_reply_load(records[i][1])
                time_ago_use_return=time_ago_use(records[i][10])
                message_predict_load_list.append({
                    "mid":records[i][1],
                    "message_user_email":records[i][2],
                    "message_user_name":records[i][3],
                    "message_user_imgsrc":records[i][4],
                    "stock_id":records[i][5],
                    "stock_name":records[i][6],
                    "predict":records[i][7],
                    "message_user_text":records[i][8],
                    "message_check_status":records[i][9],
                    "message_time":records[i][10].strftime('%Y-%m-%d %H:%M:%S'),
                    "message_time_about":time_ago_use_return,
                    "login_member_name_good_have":message_predict_like_check_return,
                    "message_good_number":str(message_predict_like_number_return),
                    "reply_message_number":str(message_predict_reply_number_return),
                    "reply_message_data":message_predict_reply_load_return


                })

            return message_predict_load_list
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

#預測留言讀取_回覆
def message_predict_reply_load(mid):
    try:
        connection = mysql.connector.connect(
        host="localhost",         
        database="stock50_web", 
        user="root",      
        password="root") 
        message_predict_reply_load_list=[]
        
        cursor = connection.cursor()
        cursor.execute("select * from message_predict_reply where mid ='%s' order by time;" %(mid))
        records = cursor.fetchall()

        if (records):
            for j in range(len(records)):
                message_predict_reply_load_list.append({
                "message_mid":records[j][1],
                "message_reply_mid":records[j][2],
                "message_reply_user_name":records[j][4],
                "message_reply_user_imgsrc":records[j][5],
                "message_reply_text":records[j][6],
                "message_reply_time":records[j][7].strftime('%Y-%m-%d %H:%M:%S'),
                "message_reply_time_about":time_ago_use(records[j][7])
                })
            return{"data":True,"message_predict_reply_load_data":message_predict_reply_load_list}
                
                
            
        else:
            return {"data":False}


    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

#預測留言按讚
def message_predict_like(mid,like_message_user_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        #檢查是否註按過
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM message_predict_good WHERE mid= '%s' and like_message_user_name='%s';" % (mid,like_message_user_name))
        records = cursor.fetchone()
            
        if (records):
            return {"error": True, "message": "已經按過讚"}

        else:
            cursor = connection.cursor()
            sql = "INSERT INTO message_predict_good (mid,like_message_user_name) VALUES (%s,%s);"

            data=(mid,like_message_user_name)
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()

            return {"ok":True}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

#預測留言取消按讚
def message_predict_unlike(mid,like_message_user_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        cursor = connection.cursor()
        cursor.execute("DELETE FROM message_predict_good WHERE mid= '%s' and like_message_user_name='%s';" % (mid,like_message_user_name))
        connection.commit()

        return {"ok":True}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

#檢查當前使用者有無按讚
def message_predict_like_check(mid,like_message_user_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM message_predict_good WHERE mid= '%s' and like_message_user_name='%s';" % (mid,like_message_user_name))
        records = cursor.fetchone()
            
        if (records):
            return True
        else:
            return False
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")


#文章總共有多少讚
def message_predict_like_number(mid):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        cursor = connection.cursor()
        cursor.execute("SELECT count(*) FROM message_predict_good WHERE mid= '%s' ;" % (mid))
        records = cursor.fetchone()
            
        return records[0]
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()



#文章總共有多少回覆
def message_predict_reply_number(mid):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        cursor = connection.cursor()
        cursor.execute("SELECT count(*) FROM message_predict_reply WHERE mid= '%s' ;" % (mid))
        records = cursor.fetchone()
            
        return records[0]
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()




#留言板_預測留言_的回覆
def message_predict_add_reply(mid,message_reply_user_email,message_reply_user_name,message_reply_user_imgsrc,message_reply_text):
    try:
        # print(message_user_email,message_user_name,message_user_imgsrc,stock_id,stock_name,stock_state,text)
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword)  

        cursor = connection.cursor()
        sql = "INSERT INTO message_predict_reply (mid,mid_reply,message_reply_user_email,message_reply_user_name,message_reply_user_imgsrc,message_reply_text) VALUES (%s,%s,%s,%s,%s,%s);"
        mid_reply=message_select_mid_reply(mid)
        data=(mid,mid_reply,message_reply_user_email,message_reply_user_name,message_reply_user_imgsrc,message_reply_text)
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()

        return {"ok":True,"mid":mid,"mid_reply":mid_reply,"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")


#功能-留言板流水號製作
def message_select_mid_reply(mid):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("SELECT mid_reply from message_predict_reply where mid='%s' ORDER BY time DESC ;" % (mid))

        records = cursor.fetchone()
        if(records):
            #print(records[0].split("_")[-1])#現在的流水號
            # print("留言編號:","mid_"+str(int(records[0].split("_")[-1])+1))
            return mid+"_"+str(int(records[0].split("_")[-1])+1)
        else:
            print("預測留言資料庫是空的，開始建立新編號")
            return mid+"_1"
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()

#將時間轉換成XXX前
def time_ago_use(time_ago):
    now_time=datetime.now()
    sent_time=time_ago
    # sent_time=datetime.strptime(time_ago,'%Y-%m-%d %H:%M:%S')
    # print("now_time",now_time,"sent_time",sent_time)
    diff_time=now_time-sent_time
    diff_d,diff_h,diff_m=days_hours_minutes(diff_time)
    # print(diff_d,diff_h,diff_m)
    if(diff_d!=0):
        return str(diff_d)+" 天前"
    if(diff_h!=0):
        return str(diff_h)+" 小時前"
    if(diff_m!=0):
        return str(diff_m)+" 分鐘前"
    else:
        return "剛剛"
    
def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60