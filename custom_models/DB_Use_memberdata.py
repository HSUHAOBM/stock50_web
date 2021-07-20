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
            print("註冊過了")
            return {"error": True, "message": "暱稱或信箱重複註冊!"}
            
        else:
            print("開始新增")
            #指令
            password=password+member_password_key
            print("password字串",password)

            password = hashlib.sha256(password.encode('utf-8')).hexdigest()   
            print("password加密",password)

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
            print("資料庫連線已關閉")


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
        cursor.execute("SELECT name,password FROM member_basedata WHERE email= '%s';" % (email))
        records = cursor.fetchone()
        if (records):
            print("帳號正確。。。開始檢查密碼")

            if (password==records[1]):
                print("密碼驗證成功")
                cursor = connection.cursor()
                cursor.execute("UPDATE member_basedata SET logingtime = CURRENT_TIMESTAMP , ip='%s' where email='%s';"%(logip,email))
                connection.commit()
                # member_signin_update_data(email,logip)
                return {"ok": True,"member_name":records[0]}
            else:
                print("密碼錯誤")
                return {"error": True, "message": "帳號或密碼錯誤"}
        else:
            print("帳號錯誤")
            return {"error": True, "message": "帳號或密碼錯誤"}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")




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
        cursor.execute("SELECT * FROM member_basedata WHERE name= '%s' and email='%s';" % (name,email))
        records = cursor.fetchone()

            
        if (records):

            print("登入")
            return {"ok": True, "message": "登入","member_email":email,"member_name":name}
            
        else:
            #註冊進資料庫
            #檢查名子是否被使用
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM member_basedata WHERE name= '%s';" % (name))
            records = cursor.fetchone()

            if(records):
                name=name+"_google"



            print("開始新增")
            #指令
            password=password+member_password_key
            print("password字串",password)

            password = hashlib.sha256(password.encode('utf-8')).hexdigest()   
            print("password加密",password)

            sql = "INSERT INTO member_basedata (email,password,name,picturesrc) VALUES (%s,%s,%s,%s);"
            member_data = (email,password,name,img_src)
            cursor = connection.cursor()
            cursor.execute(sql, member_data)
            connection.commit()
            return {"ok": True, "message": "登入","member_email":email,"member_name":name}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")


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
            birthday=records[8].strftime('%Y-%m-%d')
            registertime= records[11].strftime('%Y-%m-%d %H:%M:%S')
            return {"ok":True, "name":records[3],"gender":records[4],"address":records[5],"picturesrc":records[6],"level":records[7],"birthday":birthday,"introduction":records[9],"interests":records[10],"registertime":registertime,"login_member_name":member_name}    
        else:
            return {"error":True}
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")
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
            print("資料庫連線已關閉")

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
            print("資料庫連線已關閉")