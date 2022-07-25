import re
from datetime import datetime

import time
from custom_models import connection_pool




#留言板_預測留言
def message_predict_add(id,stock_id,stock_name,stock_state,text):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            #判斷是否為限制留言時段
            message_statsu_check=time_check()

            # print(message_statsu_check)
            if(message_statsu_check):

                cursor.execute("select count(*) from message_predict where user_id ='%s' and check_status=0;"%(id))
                records = cursor.fetchone()

                if(records[0]<=4):
                    cursor.execute("select * from message_predict where stock_id='%s' and user_id ='%s' and check_status=0 limit 1;"%(stock_id,id))
                    records = cursor.fetchone()
                    if(records):
                        return {"error": True, "message": stock_id+"－"+stock_name+"今日已預測過。"}

                    else:
                        sql = "INSERT INTO message_predict (mid,user_id,stock_id,stock_state,text) VALUES (%s,%s,%s,%s,%s);"
                        mid = message_select_mid()
                        data = (mid,id,stock_id,stock_state,text)
                        cursor.execute(sql, data)
                        connection.commit()

                        return {"ok":True,"mid":mid,"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                else:
                    return {"error": True, "message": "今日次數已達上限，明日再試。"}

            else:
                return {"error": True, "message": "為公平起見，下午13時至14時，不能送預測。"}
    except Exception as ex:
        print(ex)

#預測留言的刪除
def message_predict_delete(id,mid,member_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            cursor.execute("select level from member_basedata where id='%s' limit 1;"%(id))
            records = cursor.fetchone()
            print("權限",records[0])
            if(records[0]=="1"):
                cursor.execute("delete from message_predict where mid ='%s' ;"%(mid))
                connection.commit()

                cursor.execute("delete from predict_rank_stock_info where user_id ='%s' ;"%(member_id))
                connection.commit()

                cursor.execute("delete from predict_rank where user_id ='%s' ;"%(member_id))
                connection.commit()
                return {"ok": True, "message": "刪除"}
            else:
                return {"erorr": True, "message": "權限不足"}
    except Exception as ex:
        print(ex)

def time_check(h_start=13,wd1=6,wd2=7):
    # print("現在時間為",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    stopdeal_date = DB_get_stopdealdate()
    trun_get = True

    for i in stopdeal_date:
        if(datetime.now().month == i[0].month and datetime.now().day == i[0].day):
            # print("今日為國定假日，休市。")
            return True

        else:
            # print("判斷星期")
            trun_get=True


    if(trun_get):
        if datetime.now().isoweekday()!=wd1 and datetime.now().isoweekday()!=wd2:
            if datetime.now().hour == h_start :
                # print("開盤日、時段不能留言")
                return False
            else:
                # print("可以")
                return True
        else:
            # print("是六日，可以留言")
            return True

#取得休市日期
def DB_get_stopdealdate():
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT date FROM stock50_stopdeal_date")
            records = cursor.fetchall()
            return records

    except Exception as ex:
        print(ex)

#功能-留言板流水號製作
def message_select_mid():
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            # sql = "SELECT mid from message_predict ORDER BY time DESC "
            sql = "SELECT mid from message_predict ORDER BY time DESC  LIMIT 0 , 1"

            cursor.execute(sql)
            records = cursor.fetchone()
            if(records):
                #print(records[0].split("_")[-1])#現在的流水號
                # print("留言編號:","mid_"+str(int(records[0].split("_")[-1])+1))
                return "mid_"+str(int(records[0].split("_")[-1])+1)
            else:
                print("預測留言資料庫是空的，開始建立新編號")
                return "mid_1"
    except Exception as ex:
        print(ex)


#預測留言讀取(member_name,user_name,data_keyword)
def message_predict_load(id,member_id,data_keyword,data_number,data_status):

    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        message_predict_load_list=[]

        with connection.cursor() as cursor:
            if(member_id==None and data_keyword==None  and data_status==None):

                sql ='''SELECT message_predict.mid,user_id,stock_state,text,check_status,message_predict.time,
                member_basedata.name,picturesrc,stock50.stock_id,stock_name
                From message_predict
                Inner join member_basedata on message_predict.user_id=member_basedata.id
                Inner join stock50 on message_predict.stock_id=stock50.stock_id
                order by message_predict.time DESC limit %d , %d;'''

                cursor.execute(sql % ((int(data_number))*16,16))
                records = cursor.fetchall()
                return_text=int(data_number)*16+16

            if(member_id!=None):
                cursor.execute("select name from member_basedata where id ='%s' limit 1;"%(member_id))
                records = cursor.fetchone()
                #檢查有無此會員
                if(records):
                    cursor.execute("select mid from message_predict where user_id ='%s'limit 1;"%(member_id))
                    predict_records = cursor.fetchone()
                    return_text=records[0]

                    if(predict_records):

                        sql ='''SELECT message_predict.mid,user_id,stock_state,text,check_status,message_predict.time,
                        member_basedata.name,picturesrc,stock50.stock_id,stock_name
                        From message_predict
                        Inner join member_basedata on message_predict.user_id=member_basedata.id
                        Inner join stock50 on message_predict.stock_id=stock50.stock_id
                        where message_predict.user_id ='%s'
                        order by message_predict.time DESC limit %d , %d;'''

                        cursor.execute(sql % (member_id,(int(data_number))*16,16))
                        records = cursor.fetchall()

                    else:

                        # print("此會員無預測資料")
                        return {"member_no_data":True,"message":"此會員無預測資料"}

                else:
                    # print("無此會員")
                    return {"error":True,"message":"無資料"}


            if(data_keyword!=None):
                #檢查有無股票資料
                cursor.execute("select stock_name from stock50 where stock_id ='%s' limit 1 ;"%(data_keyword))
                records = cursor.fetchone()

                if(records):
                    return_text=records[0]

                    cursor.execute("select * from message_predict where stock_id ='%s'order by time DESC limit 1;"%(data_keyword))
                    records = cursor.fetchone()

                    if(records):

                        sql ='''SELECT message_predict.mid,user_id,stock_state,text,check_status,message_predict.time,
                        member_basedata.name,picturesrc,stock50.stock_id,stock_name
                        From message_predict
                        Inner join member_basedata on message_predict.user_id=member_basedata.id
                        Inner join stock50 on message_predict.stock_id=stock50.stock_id
                        where message_predict.stock_id ='%s'
                        order by message_predict.time DESC limit %d , %d;'''

                        cursor.execute(sql % (data_keyword,(int(data_number))*16,16))
                        records = cursor.fetchall()
                        # cursor = connection.cursor()
                        # cursor.execute("select * from message_predict where stock_id ='%s'order by time DESC limit %d , %d;"%(data_keyword,(int(data_number))*5,5))
                        # records = cursor.fetchall()
                    else:
                        return {"stock_no_data":True,"message":"此股票目前無預測資料","find":return_text}

                else:
                    print("股市代號輸入錯誤")
                    return {"error":True,"message":"股市代號輸入錯誤"}

            # print("資料數量",len(records))
            if(len(records)==0):
                return {"nodata":True,"message":"無資料","find":return_text}
            else:
                for i in range(len(records)):
                    # print(i)
                    message_predict_like_check_return=message_predict_like_check(records[i][0],id)
                    message_predict_like_number_return=message_predict_like_number(records[i][0])
                    message_predict_reply_number_return=message_predict_reply_number(records[i][0])
                    message_predict_reply_load_return=message_predict_reply_load(records[i][0])

                    time_ago_use_return=time_ago_use(records[i][5])

                    message_predict_load_list.append({
                        "predict_load":True,
                        "mid":records[i][0],
                        "user_id":records[i][1],
                        "message_user_name":records[i][6],
                        "message_user_imgsrc":records[i][7],
                        "stock_id":records[i][8],
                        "stock_name":records[i][9],
                        "predict":records[i][2],
                        "message_user_text":records[i][3],
                        "message_check_status":records[i][4],
                        "message_time":records[i][5].strftime('%Y-%m-%d %H:%M:%S'),
                        "message_time_about":time_ago_use_return,

                        "login_member_name_good_have":message_predict_like_check_return,
                        "message_good_number":str(message_predict_like_number_return),
                        "reply_message_number":str(message_predict_reply_number_return),
                        "reply_message_data":message_predict_reply_load_return
                    })

                return message_predict_load_list
    except Exception as ex:
        print(ex)

#待修正
#預測留言讀取_回覆
def message_predict_reply_load(mid):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            sql ='''SELECT message_predict_reply.*,member_basedata.name,picturesrc
            From message_predict_reply
            Inner join member_basedata on message_predict_reply.user_id=member_basedata.id
            where message_predict_reply.mid = '%s'
            order by message_predict_reply.time DESC ;'''

            cursor.execute(sql % mid)
            records = cursor.fetchall()
            message_predict_reply_load_list=[]

            if (records):
                for j in range(len(records)):
                    message_predict_reply_load_list.append({
                    "message_mid":records[j][1],
                    "message_reply_mid":records[j][2],
                    "message_reply_user_id":records[j][3],
                    "message_reply_user_name":records[j][6],
                    "message_reply_user_imgsrc":records[j][7],
                    "message_reply_text":records[j][4],
                    "message_reply_time":records[j][5].strftime('%Y-%m-%d %H:%M:%S'),
                    "message_reply_time_about":time_ago_use(records[j][5])
                    })
                return{"data":True,"message_predict_reply_load_data":message_predict_reply_load_list}
            else:
                return {"data":False}
    except Exception as ex:
        print(ex)
#-----------------------*

#預測留言按讚
def message_predict_like(mid,id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            #檢查是否註按過

            cursor.execute("SELECT mid FROM message_predict_good WHERE mid= '%s' and like_id='%s' limit 1;" % (mid,id))
            records = cursor.fetchone()

            if (records):
                return {"error": True, "message": "已經按過讚"}

            else:
                sql = "INSERT INTO message_predict_good (mid,like_id) VALUES (%s,%s);"
                data=(mid,id)
                cursor.execute(sql, data)
                connection.commit()

                return {"ok":True}
    except Exception as ex:
        print(ex)

#預測留言取消按讚
def message_predict_unlike(mid,id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:

            cursor.execute("DELETE FROM message_predict_good WHERE mid= '%s' and like_id='%s';" % (mid,id))
            connection.commit()

            return {"ok":True}
    except Exception as ex:
        print(ex)

#檢查當前使用者有無按讚
def message_predict_like_check(mid,id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT mid FROM message_predict_good WHERE mid= '%s' and like_id='%s' limit 1;" % (mid,id))
            records = cursor.fetchone()

            if (records):
                return True
            else:
                return False
    except Exception as ex:
        print(ex)

#文章總共有多少讚
def message_predict_like_number(mid):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:

            cursor.execute("SELECT count(*) FROM message_predict_good WHERE mid= '%s' limit 1 ;" % (mid))
            records = cursor.fetchone()

            return records[0]
    except Exception as ex:
        print(ex)




#文章總共有多少回覆
def message_predict_reply_number(mid):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM message_predict_reply WHERE mid= '%s' limit 1;" % (mid))
            records = cursor.fetchone()

            return records[0]
    except Exception as ex:
        print(ex)

#-----------------------*


#留言板_預測留言_的回覆
def message_predict_add_reply(mid,id,message_reply_text):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:

            sql = "INSERT INTO message_predict_reply (mid,mid_reply,user_id,text) VALUES (%s,%s,%s,%s);"
            mid_reply = message_select_mid_reply(mid)
            data = (mid,mid_reply,id,message_reply_text)
            cursor.execute(sql, data)
            connection.commit()

            return {"ok":True,"mid":mid,"mid_reply":mid_reply,"time":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    except Exception as ex:
        print(ex)

#-----------------------*

#功能-留言板流水號製作
def message_select_mid_reply(mid):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:

            cursor.execute("SELECT mid_reply from message_predict_reply where mid='%s' ORDER BY time DESC LIMIT 0 , 1 ;" % (mid))

            records = cursor.fetchone()
            if(records):
                #print(records[0].split("_")[-1])#現在的流水號
                # print("留言編號:","mid_"+str(int(records[0].split("_")[-1])+1))
                return mid+"_"+str(int(records[0].split("_")[-1])+1)
            else:
                # print("預測留言資料庫是空的，開始建立新編號")
                return mid+"_1"

    except Exception as ex:
        print(ex)

#-----------------------*

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
#-----------------------*

# 私訊
def private_message_add(id,private_message_text,private_message_member_to):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:

            sql = "INSERT INTO private_message (user_id,text,user_id_to)VALUES (%s,%s,%s);"
            data=(id,private_message_text,private_message_member_to)
            cursor = connection.cursor()
            cursor.execute(sql, data)
            connection.commit()

            return {"ok":True}
    except Exception as ex:
        print(ex)

def private_message_load(id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            sql ='''SELECT private_message.user_id,text,time,member_basedata.name,picturesrc
            From private_message
            Inner join member_basedata on private_message.user_id=member_basedata.id
            where private_message.user_id_to = '%s'
            order by private_message.time DESC ;'''

            return_list = []
            cursor.execute(sql%(id))
            records = cursor.fetchall()

            if(records):
                for i in range(len(records)):
                    return_list.append({'member_id':records[i][0],
                                        'member_name':records[i][3],
                                        'member_img':records[i][4],
                                    "message_text":records[i][1],
                                    "time":records[i][2].strftime('%Y-%m-%d %H:%M:%S'),
                                    'time_about':time_ago_use(records[i][2])})

                return return_list
            else:
                return {'private_message_not':True}
    except Exception as ex:
        print(ex)


#-----------------------*

#問題回報
def contact_message_add(id,message_text):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            sql = "INSERT INTO contact_message (user_id,text)VALUES (%s,%s);"
            data=(id,message_text)
            cursor.execute(sql, data)
            connection.commit()
            return {"ok":True}
    except Exception as ex:
        print(ex)

def contact_message_load():
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            return_list=[]


            sql ='''SELECT contact_message.user_id,text,time,member_basedata.name,picturesrc
            From contact_message
            Inner join member_basedata on contact_message.user_id=member_basedata.id
            order by contact_message.time DESC ;'''


            cursor.execute(sql)
            records = cursor.fetchall()
            if(records):
                for i in range(len(records)):
                    return_list.append({
                                        'member_id':records[i][0],
                                        'member_name':records[i][3],
                                        'member_img':records[i][4],
                                        "message_text":records[i][1],
                                        "time":records[i][2].strftime('%Y-%m-%d %H:%M:%S'),
                                        'time_about':time_ago_use(records[i][2])})
                print(return_list)
                return return_list
            else:
                return {'contact_message_not':True}
    except Exception as ex:
        print(ex)