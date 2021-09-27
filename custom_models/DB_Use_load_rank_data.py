import re
import mysql.connector
from datetime import datetime
import configparser
import os
import time
from custom_models import connection_pool




# 成績彙整讀取(user_name,stock_id,data_number,data_status)
def message_predict_rank_load(member_id,stock_id,data_number,data_status):
    try:
        message_predict_load_rank_list=[]

        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        if(member_id==None and stock_id==None):
            if(data_status=="rate"):

                sql ='''SELECT predict_rank.*,member_basedata.name,picturesrc
                From predict_rank 
                Inner join member_basedata on predict_rank.user_id=member_basedata.id
                where predict_rank.win_rate > 0
                order by cast(predict_rank.win_rate as unsigned) DESC limit %d , %d;'''
                cursor.execute(sql % ((int(data_number))*10,10))
                records = cursor.fetchall()

            if(data_status=='win'):

                sql ='''SELECT predict_rank.*,member_basedata.name,picturesrc
                From predict_rank 
                Inner join member_basedata on predict_rank.user_id=member_basedata.id
                where predict_rank.win > 0
                order by cast(predict_rank.win as unsigned) DESC limit %d , %d;'''

                cursor.execute(sql % ((int(data_number))*10,10))
                records = cursor.fetchall()

            if(data_status=='total'):

                sql ='''SELECT predict_rank.*,member_basedata.name,picturesrc
                From predict_rank 
                Inner join member_basedata on predict_rank.user_id=member_basedata.id
                where predict_rank.total > 0
                order by cast(predict_rank.total as unsigned) DESC limit %d , %d;'''

                cursor.execute(sql % ((int(data_number))*10,10))
                records = cursor.fetchall()

            if(data_status=='like'):
                sql ='''SELECT predict_rank.*,member_basedata.name,picturesrc
                From predict_rank 
                Inner join member_basedata on predict_rank.user_id=member_basedata.id
                where predict_rank.good > 0
                order by cast(predict_rank.good as unsigned) DESC limit %d , %d;'''


                cursor.execute(sql % ((int(data_number))*10,10))
                records = cursor.fetchall()

            if(records):
                for i in range(len(records)):

                    message_predict_load_rank_list.append({
                        "member_id":records[i][0],
                        "member_name":records[i][7],
                        "predict_win_rate":records[i][1],
                        "predict_win":records[i][2],
                        "predict_fail":records[i][3],
                        "predict_total":records[i][4],
                        "predict_good":records[i][5],
                        "member_src":records[i][8]

                    })
                return message_predict_load_rank_list
            else:
                return {"No_data":True}
        if(stock_id != None):
            
            sql ='''SELECT predict_rank_stock_info.*,member_basedata.name,picturesrc,stock50.stock_name
                From predict_rank_stock_info 
                Inner join member_basedata on predict_rank_stock_info.user_id=member_basedata.id
                Inner join stock50 on predict_rank_stock_info.stock_id=stock50.stock_id

                where predict_rank_stock_info.stock_id ='%s' and predict_rank_stock_info.win>0
                order by cast(predict_rank_stock_info.win_rate as unsigned) DESC limit %d , %d;'''


            cursor.execute(sql % (stock_id,(int(data_number))*5,5))
            records = cursor.fetchall()
            if(records):
                for i in range(len(records)):
                    message_predict_load_rank_list.append({
                        "predict_load_rank":True,
                        "stock_id":records[i][1],
                        "stock_name":records[i][10],
                        "member_name":records[i][8],
                        "predict_win_rate":records[i][3],
                        "predict_win":records[i][4],
                        "predict_fail":records[i][5],
                        "predict_total":records[i][6],
                        "member_src":records[i][9]
                    })
                return message_predict_load_rank_list
            else:
                return {"No_data":True}
        
        if(member_id != None and data_status!=None):
            if(data_status=='rate'):
                load_rank_data_return=load_rank_data_predict_win_rate(member_id)
            if(data_status=='win'):
                load_rank_data_return=load_rank_data_predict_win(member_id)
            if(data_status=='fail'):
                load_rank_data_return=load_rank_data_predict_fail(member_id)
            if(load_rank_data_return):
                for i in range(len(load_rank_data_return)):
                    message_predict_load_rank_list.append({
                        "predict_load_rank":True,
                        "stock_id":load_rank_data_return[i][1],
                        "stock_name":load_rank_data_return[i][10],
                        "member_name":load_rank_data_return[i][8],
                        "member_id":load_rank_data_return[i][2],
                        "predict_win_rate":load_rank_data_return[i][3],
                        "predict_win":load_rank_data_return[i][4],
                        "predict_fail":load_rank_data_return[i][5],
                        "predict_total":load_rank_data_return[i][6]

                    })
                return message_predict_load_rank_list        
            else:
                # print("無資料")
                return {"member_no_data":True,"message":"此會員無預測資料"}
        else:
            return {"error":True,"message":"錯誤"}
    finally:
        cursor.close()
        connection.close()
        
#load img src
def load_member_src(member_name):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("select picturesrc from member_basedata where name='%s';"%(member_name))
        records = cursor.fetchone()
        return records[0]
    finally:
        cursor.close()
        connection.close()




def load_rank_data_predict_win_rate(member_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        sql ='''SELECT predict_rank_stock_info.*,member_basedata.name,picturesrc,stock50.stock_name
                From predict_rank_stock_info 
                Inner join member_basedata on predict_rank_stock_info.user_id=member_basedata.id
                Inner join stock50 on predict_rank_stock_info.stock_id=stock50.stock_id

                where predict_rank_stock_info.user_id ='%s' and predict_rank_stock_info.win>0
                order by cast(predict_rank_stock_info.win_rate as unsigned) DESC limit 5;'''


        cursor.execute(sql % (member_id))
        records = cursor.fetchall()
        # print(records)
        return records
    finally:
        cursor.close()
        connection.close()

def load_rank_data_predict_win(member_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        sql ='''SELECT predict_rank_stock_info.*,member_basedata.name,picturesrc,stock50.stock_name
                From predict_rank_stock_info 
                Inner join member_basedata on predict_rank_stock_info.user_id=member_basedata.id
                Inner join stock50 on predict_rank_stock_info.stock_id=stock50.stock_id

                where predict_rank_stock_info.user_id ='%s' and predict_rank_stock_info.win>0
                order by cast(predict_rank_stock_info.win as unsigned) DESC limit 5;'''
        cursor.execute(sql % (member_id))

        records = cursor.fetchall()
        return records
    finally:
        cursor.close()
        connection.close()

def load_rank_data_predict_fail(member_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        sql ='''SELECT predict_rank_stock_info.*,member_basedata.name,picturesrc,stock50.stock_name
                From predict_rank_stock_info 
                Inner join member_basedata on predict_rank_stock_info.user_id=member_basedata.id
                Inner join stock50 on predict_rank_stock_info.stock_id=stock50.stock_id

                where predict_rank_stock_info.user_id ='%s' and predict_rank_stock_info.fail>0
                order by cast(predict_rank_stock_info.fail as unsigned) DESC limit 5;'''
        cursor.execute(sql % (member_id))

        records = cursor.fetchall()
        return records
    finally:
        cursor.close()
        connection.close()


