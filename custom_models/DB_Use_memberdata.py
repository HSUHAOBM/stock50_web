from re import escape
import mysql.connector
from datetime import datetime
import hashlib

from custom_models import connection_pool

member_password_key = "w50stock"




#一般會員註冊
def member_registered (email,password,name):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        #檢查是否註冊過
        cursor.execute("SELECT name FROM member_basedata WHERE name= '%s' or email='%s' limit 1;" % (name,email))
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
        cursor.close()
        connection.close()


#一般會員登入
def member_signin(email,password,logip):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        password=password+member_password_key
        # print("password字串",password)

        password = hashlib.sha256(password.encode('utf-8')).hexdigest()   
        # print("password加密",password)
            
        #檢查是否註冊過
        cursor.execute("SELECT name,password,level FROM member_basedata WHERE email= '%s' limit 1;" % (email))
        records = cursor.fetchone()
        if (records):
            # print("帳號正確。。。開始檢查密碼")

            if (password==records[1]):
                # print("密碼驗證成功")
                cursor = connection.cursor()
                cursor.execute("UPDATE member_basedata SET logingtime = CURRENT_TIMESTAMP , ip='%s' where email='%s';"%(logip,email))
                connection.commit()
                return {"ok": True,"member_name":records[0],"level":records[2]}
            else:
                # print("密碼錯誤")
                return {"error": True, "message": "帳號或密碼錯誤"}
        else:
            # print("帳號錯誤")
            return {"error": True, "message": "帳號或密碼錯誤"}
    finally:
        cursor.close()
        connection.close()
            # print("資料庫連線已關閉")




#第三方會員登入與註冊
def member_registered_thirdarea (email,password,name,img_src):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        #資料處理
        email=password+email
        #檢查是否註冊過
        cursor.execute("SELECT email,name,picturesrc,level FROM member_basedata WHERE  email='%s' limit 1;" % (email))
        records = cursor.fetchone()

            
        if (records):
            # print("登入")
            return {"ok": True, "message": "登入","member_email":records[0],"member_name":records[1],"member_src":records[2],"level":records[3]}
            
        else:
            #註冊進資料庫 檢查名子是否被使用
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM member_basedata WHERE name= '%s' limit 1;" % (name))
            records = cursor.fetchone()

            if(records):
                name=name+"_google"
            # print("開始新增")
            password=password+member_password_key
            # print("password字串",password)
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()   
            # print("password加密",password)

            sql = "INSERT INTO member_basedata (email,password,name,picturesrc) VALUES (%s,%s,%s,%s);"
            member_data = (email,password,name,img_src)
            cursor = connection.cursor()
            cursor.execute(sql, member_data)
            connection.commit()


            return {"ok": True, "message": "登入","member_email":email,"member_name":name,"member_src":img_src,"level":"0"}
    finally:
        cursor.close()
        connection.close()
            # print("資料庫連線已關閉")


#會員詳細資料讀取
def load_member_data (name,member_name):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM member_basedata WHERE name= '%s' limit 1 ;" % (name))
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
        cursor.close()
        connection.close()
        # print("資料庫連線已關閉")
#會員詳細資料修改
def modify_member_data (email,name,newname,gender,address,birthday,introduction,interests):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        
        if(name!=newname):
        #檢查名稱是否重複
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM member_basedata  WHERE name= '%s' limit 1 ;" % (newname))
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
        cursor.close()
        connection.close()
        # print("資料庫連線已關閉")

#會員頭貼修改
def modify_member_picturesrc (email,name,picturesrc):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
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
        cursor.close()
        connection.close()

#會員總共有多少讚
def member_message_predict_like_number(member_name):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("SELECT count(*) FROM message_predict_good WHERE mid_member= '%s' ;" % (member_name))
        records = cursor.fetchone()
            
        return records[0]
    finally:
        cursor.close()
        connection.close()



#取得預測成績            
def message_rank_select(member_name):
    connection = connection_pool.getConnection()
    connection = connection.connection()
    cursor = connection.cursor()

    cursor.execute("select * from message_predict_rank where member_name='%s' limit 1;"%(member_name))
    records = cursor.fetchone()
    try:
        if(records):
            return {"ok":True,"rate":records[1],"win":records[2],"fail":records[3],"total":records[4]}
        else:
            return {"nodata":True}
    finally:
        cursor.close()
        connection.close()

