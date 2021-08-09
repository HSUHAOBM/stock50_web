import requests
import json
from datetime import datetime
import time
# import mysql.connector
# import configparser
# import os
import connection_pool


# config = configparser.ConfigParser()
# config.read('config.ini')
# parent_dir = os.path.dirname(os.path.abspath(__file__))
# config.read(parent_dir + "/config.ini")

# DBhost=config.get('use_db', 'DBhost')   
# DBdatabase=config.get('use_db', 'DBdatabase')
# DBuser=config.get('use_db', 'DBuser')
# DBpassword=config.get('use_db', 'DBpassword')



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
    time.sleep(3)

    url_tese='https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+datetime.now().strftime('%Y%m%d')+'&stockNo='+str(stocknumber)+'&_='
    print("網址來源：",url_tese)
    res= requests.get(url_tese)
    jdata = json.loads(res.text)
    
    if ('data' not in jdata):
        print(datetime.now().strftime('%Y%m%d'))
        return datetime.now().strftime('%Y%m%d') ,None ,None ,None ,None ,None ,None ,None
    else:
        print(jdata['data'][-1])

        returndata=jdata['data'][-1]
        
        return jdata['date'] ,returndata[1].replace(',','') ,returndata[3].replace(',','') ,returndata[4].replace(',','') ,returndata[5].replace(',','') ,returndata[6].replace(',','') ,returndata[7].replace(',','') ,returndata[8].replace(',','')

#資料庫_存50的相關資料
def stock50_getstock50_toDB(stock_id,stock_name,date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        
        sql = "INSERT INTO stock50_data (stock_id,stock_name,date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        stock_data=(stock_id,stock_name,date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal)
        cursor = connection.cursor()
        cursor.execute(sql, stock_data)
        connection.commit()
        print("資料庫連線")

    finally:
        cursor.close()
        connection.close()
        print("資料庫連線已關閉")




#執行
def stock50_getdata():
    i=0    

    stock_name,stock_id=loadstock50dataname()

    for index in stock_id:
        date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal=loadstockdata(index)

        print(stock_id[i],stock_name[i],date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal)
        if(stock_total!="0"):
            if differ =="X0.00":
                print(stock_name[i],"今日除息")
                differ=round(float(open_price)-float(end_price), 2)
                differ=str(differ)
            stock50_getstock50_toDB(stock_id[i],stock_name[i],date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal)
        i=i+1


#檢查是否有沒抓到資料
def stock50_getstock50_check_error():
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        
        cursor.execute("select * from stock50_data where open_price is null")
        records = cursor.fetchall()
        if (records):
            for i in range(len(records)):
                getstock50_data=loadstockdata(records[i][1])
                stock50_getstock50_error_modify(getstock50_data,records[i][1])
            return "錯誤修改完成。"
        else:
            return "今日無錯誤。"
    finally:
        cursor.close()
        connection.close()
        print("資料庫連線已關閉")

#修正程式
def stock50_getstock50_error_modify(getstock50_data,stock_id):
    try:
        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()
        
        stock_total,open_price,high_price,low_price,end_price,differ,totaldeal=getstock50_data[1],getstock50_data[2],getstock50_data[3],getstock50_data[4],getstock50_data[5],getstock50_data[6],getstock50_data[7]
        
        cursor = connection.cursor()
        cursor.execute("UPDATE stock50_data SET stock_total='%s',open_price='%s',high_price='%s',low_price='%s',end_price='%s',differ='%s',totaldeal='%s' WHERE stock_id= '%s' ;" % (stock_total,open_price,high_price,low_price,end_price,differ,totaldeal,stock_id))
        connection.commit()  


    finally:
        cursor.close()
        connection.close()
        print("資料庫連線已關閉")