import re
import mysql.connector
from datetime import datetime
from custom_models import connection_pool

import time

# from werkzeug.utils import escape



def search_keyword_data(key_word):
    member_data=False
    stock_data=False
    have_data=False

    stock_return=search_keyword_data_stock(key_word)
    member_return=search_keyword_data_member(key_word)
    if(member_return):
        member_data=True
    if(stock_return):
        stock_data=True

    if(member_data==False and stock_data==False):
        have_data=False
    else:
        have_data=True

    return {'data_have':have_data,'data_member':member_data ,"member_data":member_return,'data_stock':stock_data,"stock_data":stock_return}



def search_keyword_data_member(key_word):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select name,picturesrc from member_basedata where name LIKE '%{}%' ;".format(key_word))
        records = cursor.fetchall()
        print(records)
        return records
    finally:
        cursor.close()
        connection.close()

def search_keyword_data_stock(key_word):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select stock_id,stock_name from stock50 where stock_name LIKE '%{}%' or stock_id LIKE '%{}%' ;".format(key_word,key_word))
        records = cursor.fetchall()
        print(records)
        return records
    finally:
        cursor.close()
        connection.close()