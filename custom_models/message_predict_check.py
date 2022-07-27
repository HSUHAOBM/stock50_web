import connection_pool
#-----------------------*

#留言板_預測檢測
def message_predict_check():
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            sql = "select mid,stock_id,stock_state from message_predict where check_status=0"
            cursor.execute(sql)
            records = cursor.fetchall()
            for message_data in records:
                stock50_check(message_data[0],message_data[1],message_data[2])
            return {"ok": True, "message": "會員預測留言檢查完成"}

    except Exception as ex:
        print(ex)

#檢查預測留言值有無成功
def stock50_check(mid,stock_id,stock_state):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:

            cursor.execute("select differ from stock50_data WHERE stock_id= '%s' ORDER BY date DESC LIMIT 0 , 1;" % (stock_id))
            records = cursor.fetchone()
            if stock_state == "1" and records[0] > 0:
                message_predict_check_correct(mid)
            elif stock_state == "0" and records[0] == 0:
                message_predict_check_correct(mid)
            elif stock_state == "-1" and records[0] < 0:
                message_predict_check_correct(mid)

            else:
                message_predict_check_error(mid)
            return records
    except Exception as ex:
        print(ex)

#預測留言成功
def message_predict_check_correct(mid):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            cursor.execute("UPDATE message_predict SET check_status='1' where mid='%s';"%(mid))
            connection.commit()
            return {"ok": True, "message": "預測成功，結果已上傳資料庫"}
    except Exception as ex:
        print(ex)

#預測留言失敗
def message_predict_check_error(mid):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()

        with connection.cursor() as cursor:
            cursor.execute("UPDATE message_predict SET check_status='-1' where mid='%s';"%(mid))
            connection.commit()
            return {"ok": True, "message": "預測失敗，結果已上傳資料庫"}
    except Exception as ex:
        print(ex)



#-----------------------*