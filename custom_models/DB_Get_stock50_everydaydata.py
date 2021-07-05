import requests
import json
from datetime import datetime
import time
import mysql.connector
import configparser
import os

#取得台灣50
stock_id=[]
stock_name=[]
def loadstock50dataname():
    url_tese='https://www.yuantaetfs.com/api/Composition?fundid=1066'
    res= requests.get(url_tese)
    stock50_namedata = json.loads(res.text)
    for i in range(len(stock50_namedata)):
        stock_id.append(stock50_namedata[i]["stkcd"])    
        stock_name.append(stock50_namedata[i]["name"])

    return stock_name,stock_id

#功能_爬台灣證券網，延遲3s設定
def loadstockdata(stocknumber):
    url_tese='https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+datetime.now().strftime('%Y%m%d')+'&stockNo='+str(stocknumber)+'&_=1604642840350'
    res= requests.get(url_tese)
    jdata = json.loads(res.text)
    time.sleep(3)
    return jdata["data"][-1][0],jdata["data"][-1][1],jdata["data"][-1][3],jdata["data"][-1][4],jdata["data"][-1][5],jdata["data"][-1][6],jdata["data"][-1][7],jdata["data"][-1][8]

#功能_轉捔民國日期為西元:106/01/02->20170102
def convertDate(date): 
    str1 = str(date)
    yearstr = str1[:3]
    realyear = str(int(yearstr) + 1911)
    realdate = realyear + str1[4:6] + str1[7:9]
    return realdate

#資料庫_存50的相關資料
def stock50_getstock50_toDB(stock_id,stock_name,data,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal):
    try:
        connection = mysql.connector.connect(
        host="localhost",         
        database="stock50_web", 
        user="root",      
        password="root") 
        cursor = connection.cursor()
        sql = "INSERT INTO stock50_data (stock_id,stock_name,date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        data=(stock_id,stock_name,data,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal)
        cursor = connection.cursor()
        cursor.execute(sql, data)
        connection.commit()
        print("資料庫連線")

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")


#執行
def stock50_getdata():
    i=0
    loadstock50dataname()
    for index in stock_id:
        data,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal=loadstockdata(index)
        data=convertDate(data)
        print(stock_id[i],stock_name[i],data,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal)
        if(stock_total!="0"):
            if differ =="X0.00":
                print(stock_name[i],"今日除息")
                differ=round(float(open_price)-float(end_price), 2)
                differ=str(differ)
            stock50_getstock50_toDB(stock_id[i],stock_name[i],data,stock_total.replace(',',''),open_price.replace(',',''),high_price.replace(',',''),low_price.replace(',',''),end_price.replace(',',''),differ.replace(',',''),totaldeal.replace(',',''))
        i=i+1

# stock50_getdata()