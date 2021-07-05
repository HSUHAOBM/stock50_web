from dns.rdatatype import NULL
import requests
import json
from datetime import datetime
import time
import mysql.connector
import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('use_db', 'DBhost')   
DBdatabase=config.get('use_db', 'DBdatabase')
DBuser=config.get('use_db', 'DBuser')
DBpassword=config.get('use_db', 'DBpassword')

from dns.rdatatype import NULL
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
        connection = mysql.connector.connect(
        host=DBhost,         
        database=DBdatabase, 
        user=DBuser,      
        password=DBpassword) 
        cursor = connection.cursor()
        sql = "INSERT INTO stock50_data (stock_id,stock_name,date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        stock_data=(stock_id,stock_name,date,stock_total,open_price,high_price,low_price,end_price,differ,totaldeal)
        cursor = connection.cursor()
        cursor.execute(sql, stock_data)
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
