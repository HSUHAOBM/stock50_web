import mysql.connector
from datetime import datetime
import connection_pool


#存50的相關資料
def stock50_everydaydata(stock_id,stock_name,data,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        sql = "INSERT INTO stock50_data (stock_id,stock_name,date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        data=(stock_id,stock_name,data,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal)
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()    
    finally:
        cursor.close()
        connection.close()
