import re
import mysql.connector
from datetime import datetime

import time
from custom_models import connection_pool


def load_stock_data(stock_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select * from stock50_data where stock_id='%s'order by time desc limit 1;"%(stock_id))
        records = cursor.fetchone()

        return {"stock_id":records[1],"stock_name":records[2],"date":records[3].strftime('%Y-%m-%d'),
        "total":records[4],"open_price":records[5],"high_price":records[6],"low_price":records[7],
        "end_price":records[8],"differ":records[9],"total_deal":records[10],"update_time":records[11].strftime('%Y-%m-%d %H:%M')}
    finally:
        cursor.close()
        connection.close()


