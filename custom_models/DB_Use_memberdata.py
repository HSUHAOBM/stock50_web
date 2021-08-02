from re import escape
import mysql.connector
from datetime import datetime
import configparser
import os
import hashlib

member_password_key = "w50stock"
config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')   
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')


#一般會員註冊
def member_registered (email,password,name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        #檢查是否註冊過
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM member_basedata WHERE name= '%s' or email='%s';" % (name,email))
        records = cursor.fetchone()

            
        if (records):
            # print("註冊過了")
            return {"error": True, "message": "暱稱或信箱重複註冊!"}
            
        else:
            # print("開始新增")
            #指令
            password=password+member_password_key
            # print("password字串",password)

            password = hashlib.sha256(password.encode('utf-8')).hexdigest()   
            # print("password加密",password)

            sql = "INSERT INTO member_basedata (email,password,name) VALUES (%s,%s,%s);"
            member_data = (email,password,name)
            cursor = connection.cursor()
            cursor.execute(sql, member_data)
            connection.commit()
            return {"ok": True, "message": "註冊成功!"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")


#一般會員登入
def member_signin(email,password,logip):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        password=password+member_password_key
        # print("password字串",password)

        password = hashlib.sha256(password.encode('utf-8')).hexdigest()   
        # print("password加密",password)
            
        #檢查是否註冊過
        cursor = connection.cursor()
        cursor.execute("SELECT name,password,level FROM member_basedata WHERE email= '%s';" % (email))
        records = cursor.fetchone()
        if (records):
            # print("帳號正確。。。開始檢查密碼")

            if (password==records[1]):
                # print("密碼驗證成功")
                cursor = connection.cursor()
                cursor.execute("UPDATE member_basedata SET logingtime = CURRENT_TIMESTAMP , ip='%s' where email='%s';"%(logip,email))
                connection.commit()
                # member_signin_update_data(email,logip)


                return {"ok": True,"member_name":records[0],"level":records[2]}
            else:
                # print("密碼錯誤")
                return {"error": True, "message": "帳號或密碼錯誤"}
        else:
            # print("帳號錯誤")
            return {"error": True, "message": "帳號或密碼錯誤"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")




#第三方會員登入與註冊
def member_registered_thirdarea (email,password,name,img_src):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        #資料處理
        email=password+email

        # print(email)
        #檢查是否註冊過
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM member_basedata WHERE  email='%s';" % (email))
        records = cursor.fetchone()

            
        if (records):

            # print("權限",records[7])

            # print("登入")
            return {"ok": True, "message": "登入","member_email":records[1],"member_name":records[3],"member_src":records[6],"level":records[7]}
            
        else:
            #註冊進資料庫
            #檢查名子是否被使用
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM member_basedata WHERE name= '%s';" % (name))
            records = cursor.fetchone()

            if(records):
                name=name+"_google"



            # print("開始新增")
            #指令
            password=password+member_password_key
            # print("password字串",password)

            password = hashlib.sha256(password.encode('utf-8')).hexdigest()   
            # print("password加密",password)

            sql = "INSERT INTO member_basedata (email,password,name,picturesrc) VALUES (%s,%s,%s,%s);"
            member_data = (email,password,name,img_src)
            cursor = connection.cursor()
            cursor.execute(sql, member_data)
            connection.commit()

            cursor = connection.cursor()
            cursor.execute("select level from member_basedata where name='%s' limit 1;"%(name))
            records = cursor.fetchone()
            print("權限",records[0])

            return {"ok": True, "message": "登入","member_email":email,"member_name":name,"member_src":img_src,"level":records[0]}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")


#會員詳細資料讀取
def load_member_data (name,member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM member_basedata WHERE name= '%s'  ;" % (name))
        records = cursor.fetchone()
        if(records):
            # print(records[9])
            if(records[9]):
                birthday=records[9].strftime('%Y-%m-%d')
            else:
                birthday="無"
            registertime= records[12].strftime('%Y-%m-%d %H:%M:%S')
            return {"ok":True, 
            "name":records[3],
            "gender":records[4],
            "address":records[5],
            "picturesrc":records[6],
            "level":records[7],
            "birthday":birthday,
            "introduction":records[10],
            "interests":records[11],
            "registertime":registertime,
            "login_member_name":member_name,
            "like_total_number":member_message_predict_like_number(records[3]),
            "rank_total":message_rank_select(records[3])
            }    
        else:
            return {"error":True,"message":"無此會員"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")
#會員詳細資料修改
def modify_member_data (email,name,newname,gender,address,birthday,introduction,interests):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        
        if(name!=newname):
        #檢查名稱是否重複
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM member_basedata  WHERE name= '%s' ;" % (newname))
            records = cursor.fetchone()
            if (records):
                return {"error": True, "message": "暱稱已被註冊使用。"}

            else:
                cursor = connection.cursor()
                cursor.execute("UPDATE member_basedata SET name='%s',gender='%s',address='%s',birthday='%s',introduction='%s',interests='%s' WHERE name= '%s'  and email= '%s';" % (newname,gender,address,birthday,introduction,interests,name,email))
                connection.commit()  

                cursor = connection.cursor()
                cursor.execute("UPDATE message_predict SET message_user_name='%s' WHERE message_user_name= '%s'  and message_user_email= '%s';" % (newname,name,email))
                connection.commit()  
                
                cursor = connection.cursor()
                cursor.execute("UPDATE message_predict_reply SET message_reply_user_name='%s' WHERE message_reply_user_name= '%s'  and message_reply_user_email= '%s';" % (newname,name,email))
                connection.commit()  

                cursor = connection.cursor()
                cursor.execute("UPDATE message_predict_good SET like_message_user_name='%s' WHERE like_message_user_name= '%s' ;" % (newname,name))
                connection.commit()  

                cursor = connection.cursor()
                cursor.execute("UPDATE message_predict_rank SET member_name='%s' WHERE member_name= '%s' ;" % (newname,name))
                connection.commit()  

                cursor = connection.cursor()
                cursor.execute("UPDATE message_predict_rank_stock_info SET member_name='%s' WHERE member_name= '%s' ;" % (newname,name))
                connection.commit()  

                cursor = connection.cursor()
                cursor.execute("UPDATE private_message SET private_message_member='%s' WHERE private_message_member= '%s' ;" % (newname,name))
                connection.commit()
                
                cursor = connection.cursor()
                cursor.execute("UPDATE private_message SET private_message_member_to='%s' WHERE private_message_member_to= '%s' ;" % (newname,name))
                connection.commit()   

                return {"ok":True,"modify_name":True}
        else:
            cursor = connection.cursor()
            cursor.execute("UPDATE member_basedata SET gender='%s',address='%s',birthday='%s',introduction='%s',interests='%s' WHERE name= '%s'  and email= '%s';" % (gender,address,birthday,introduction,interests,name,email))
            connection.commit()        
        
            return {"ok":True}
    finally:
        
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

#會員頭貼修改
def modify_member_picturesrc (email,name,picturesrc):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        

        cursor = connection.cursor()
        cursor.execute("UPDATE member_basedata SET picturesrc='%s' WHERE name= '%s'  and email= '%s';" % (picturesrc,name,email))
        connection.commit()      


        cursor = connection.cursor()
        cursor.execute("UPDATE message_predict_reply SET message_reply_user_imgsrc='%s' WHERE message_reply_user_name= '%s'  and message_reply_user_email= '%s';" % (picturesrc,name,email))
        connection.commit() 
        
        cursor = connection.cursor()
        cursor.execute("UPDATE message_predict SET message_user_imgsrc='%s' WHERE message_user_name= '%s'  and message_user_email= '%s';" % (picturesrc,name,email))
        connection.commit()  


        return {"ok":True}
    finally:
        
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("資料庫連線已關閉")

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


#取得預測成績            
def message_rank_select(member_name):
    try:
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 

        cursor = connection.cursor()
        cursor.execute("select * from message_predict_rank where member_name='%s';"%(member_name))
        records = cursor.fetchone()
        if(records):
            return {"ok":True,"rate":records[1],"win":records[2],"fail":records[3],"total":records[4]}
        else:
            return {"nodata":True}
        

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
