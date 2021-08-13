import connection_pool
#-----------------------*

#留言板_預測檢測
def message_predict_check():
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        sql = "select mid,message_user_email,stock_id,stock_state from message_predict where check_status=0"
        cursor.execute(sql)
        records = cursor.fetchall()
        for message_data in records:
            stock50_check(message_data[0],message_data[1],message_data[2],message_data[3])
        return {"ok": True, "message": "會員預測留言檢查完成"}

    finally:
        cursor.close()
        connection.close()

#檢查預測留言值有無成功
def stock50_check(mid,account,stock_id,stock_state):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
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
        cursor.close()
        connection.close()


#預測留言成功
def message_predict_check_correct(mid):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        
        cursor.execute("UPDATE message_predict SET check_status='1' where mid='%s';"%(mid))
        connection.commit()
        return {"ok": True, "message": "預測成功，結果已上傳資料庫"}
    finally:
        cursor.close()
        connection.close()


#預測留言失敗
def message_predict_check_error(mid):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        
        cursor.execute("UPDATE message_predict SET check_status='-1' where mid='%s';"%(mid))
        connection.commit()
        return {"ok": True, "message": "預測失敗，結果已上傳資料庫"}
    finally:
        cursor.close()
        connection.close()



#-----------------------*