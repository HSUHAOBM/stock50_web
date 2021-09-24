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
        cursor.execute("SELECT id,name,password,picturesrc,level FROM member_basedata WHERE email= '%s' limit 1;" % (email))
        records = cursor.fetchone()
        if (records):
            # print("帳號正確。。。開始檢查密碼")

            if (password==records[2]):
                # print("密碼驗證成功")
                cursor = connection.cursor()
                cursor.execute("UPDATE member_basedata SET logingtime = CURRENT_TIMESTAMP , ip='%s' where email='%s';"%(logip,email))
                connection.commit()
                return {"ok": True,"member_id":records[0],"member_name":records[1],"picturesrc":records[3],"level":records[4]}
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
        cursor.execute("SELECT id,email,name,picturesrc,level FROM member_basedata WHERE  email='%s' limit 1;" % (email))
        records = cursor.fetchone()

            
        if (records):
            # print("登入")
            return {"ok": True, "message": "登入","id":records[0],"member_email":records[1],"member_name":records[2],"member_src":records[3],"level":records[4]}
            
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
            
            
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM member_basedata WHERE password='%s' limit 1;" % (password))
            records = cursor.fetchone()


            return {"ok": True,"id":records[0] ,"message": "登入","member_email":email,"member_name":name,"member_src":img_src,"level":"0"}
    finally:
        cursor.close()
        connection.close()
            # print("資料庫連線已關閉")


#會員詳細資料讀取
def load_member_data (id,login_name,login_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM member_basedata WHERE id= '%s' limit 1 ;" % (id))
        records = cursor.fetchone()
        if(records):
            # print(records[9])
            if(records[9]):
                birthday=records[9].strftime('%Y-%m-%d')
            else:
                birthday="無"
            registertime= records[12].strftime('%Y-%m-%d %H:%M:%S')
            return {"ok":True, 
            "id":records[0],
            "name":records[3],
            "gender":records[4],
            "address":records[5],
            "picturesrc":records[6],
            "level":records[7],
            "birthday":birthday,
            "introduction":records[10],
            "interests":records[11],
            "registertime":registertime,
            "login_member_name":login_name,
            "login_member_id":login_id,
            "like_total_number":member_message_predict_like_number(id),
            "rank_total":message_rank_select(id)
            }    
        else:
            return {"error":True,"message":"無此會員"}
    finally:
        cursor.close()
        connection.close()
        # print("資料庫連線已關閉")
#會員詳細資料修改
def modify_member_data (id,email,name,newname,gender,address,birthday,introduction,interests):
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
                cursor.execute("UPDATE member_basedata SET name='%s',gender='%s',address='%s',birthday='%s',introduction='%s',interests='%s' WHERE id= '%s'  ;" % (newname,gender,address,birthday,introduction,interests,id))
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
def modify_member_picturesrc (id,picturesrc):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("UPDATE member_basedata SET picturesrc='%s' WHERE id= '%s';" % (picturesrc,id))
        connection.commit()      

        return {"ok":True}
    finally:
        cursor.close()
        connection.close()
#待修正
#會員總共有多少讚 
def member_message_predict_like_number(id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        sql ='''SELECT count(*) from message_predict_good
        Inner join message_predict on message_predict_good.mid=message_predict.mid
        WHERE message_predict.user_id= '%s' '''
        
        cursor = connection.cursor()
        cursor.execute(sql%id)
        records = cursor.fetchone()
            
        return records[0]
    finally:
        cursor.close()
        connection.close()



#取得預測成績            
def message_rank_select(id):
    connection = connection_pool.getConnection()
    connection = connection.connection()
    cursor = connection.cursor()

    cursor.execute("select * from predict_rank where user_id='%s' limit 1;"%(id))
    records = cursor.fetchone()
    try:
        if(records):
            return {"ok":True,"rate":records[1],"win":records[2],"fail":records[3],"total":records[4]}
        else:
            return {"nodata":True}
    finally:
        cursor.close()
        connection.close()

