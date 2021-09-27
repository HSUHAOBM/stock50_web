import re
import mysql.connector
from datetime import datetime

import time
from custom_models import connection_pool

import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# def load_stock_data(stock_id):
#     try:
#         connection = connection_pool.getConnection()
#         connection = connection.connection()
#         cursor = connection.cursor()

#         cursor.execute("select * from stock50_data where stock_id='%s'order by time desc limit 1;"%(stock_id))
#         records = cursor.fetchone()

#         return {"stock_id":records[1],"stock_name":records[2],"date":records[3].strftime('%Y-%m-%d'),
#         "total":records[4],"open_price":records[5],"high_price":records[6],"low_price":records[7],
#         "end_price":records[8],"differ":records[9],"total_deal":records[10],"update_time":records[11].strftime('%Y-%m-%d %H:%M')}
#     finally:
#         cursor.close()
#         connection.close()


def load_stock_data(stock_id):
 
        pw = r.hgetall(stock_id)
        if not pw:
            try:
                print("無快取資料")

                connection = connection_pool.getConnection()
                connection = connection.connection()
                cursor = connection.cursor()

                cursor.execute("select * from stock50_data where stock_id='%s'order by time desc limit 1;"%(stock_id))
                records = cursor.fetchone()

                r.hmset(stock_id, {"stock_id":records[0],"stock_name":records[1],"date":records[2].strftime('%Y-%m-%d'),
                "total":records[3],"open_price":records[4],"high_price":records[5],"low_price":records[6],
                "end_price":records[7],"differ":records[8],"total_deal":records[9],"update_time":records[10].strftime('%Y-%m-%d %H:%M')})
                r.expire(stock_id, 600) 

                return {"stock_id":records[0],"stock_name":records[1],"date":records[2].strftime('%Y-%m-%d'),
                "total":records[3],"open_price":records[4],"high_price":records[5],"low_price":records[6],
                "end_price":records[7],"differ":records[8],"total_deal":records[9],"update_time":records[10].strftime('%Y-%m-%d %H:%M')}
            finally:
                cursor.close()
                connection.close()
        else:
            print("有快取資料")
            return {"stock_id":pw["stock_id"],"stock_name":pw["stock_name"],"date":pw["date"],
                "total":pw["total"],"open_price":pw["open_price"],"high_price":pw["high_price"],"low_price":pw["low_price"],
                "end_price":pw["end_price"],"differ":pw["differ"],"total_deal":pw["total_deal"],"update_time":pw["update_time"]}
