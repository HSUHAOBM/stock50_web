
from datetime import datetime
import os
import time

import DB_Get_stock50_everydaydata,DB_Use_rank,DB_Use_rank_stock_info,message_predict_check
import connection_pool


modelPath = os.path.dirname(os.path.realpath(__file__))

import logging
logger = logging.getLogger("log")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(modelPath+"/spam.log", encoding='utf-8')
fh.setLevel(logging.DEBUG)

# 日誌格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


logger.info("日誌紀錄寫入中")





#取得休市日期
def DB_get_stopdealdate():
    try:

        connection = connection_pool.getConnection()
        connection = connection.connection()
        cursor = connection.cursor()

        cursor.execute("SELECT date FROM stock50_stopdeal_date")
        records = cursor.fetchall()


        return records

    finally:
        cursor.close()
        connection.close()
        print("資料庫連線已關閉")




#設定爬取時間為下午1點45分
def main(h=13,m=45,wd1=6,wd2=7):
    stopdeal_date = DB_get_stopdealdate()

    print("現在時間為",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logger.info(str(datetime.now().month)+"月"+str(datetime.now().day)+"日 "+str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second))

    trun_get = True
    for i in stopdeal_date:
        if(datetime.now().month == i[0].month):
            if(datetime.now().day == i[0].day):
                print("國定假日，休市")
                logger.info("國定假日，休市")
                trun_get=False
    if(trun_get):
        now = datetime.now()
        if now.isoweekday()!=wd1 and now.isoweekday()!=wd2:
            if now.hour == h and now.minute == m :
                print("今天有開市，並將開始執行爬蟲")
                logger.info("今天有開市，並將開始執行爬蟲")
                doSth()
            else:
                print("今天有開市，但未收盤或已執行。")
                logger.info("今天有開市，但未收盤或已執行。")
        else:
            print("休市")
            logger.info("休市")


    # time.sleep(60)
    print("-持續監控中-")
    logger.info("-持續監控中-")

def doSth():
    print("取得最新的股市資料")
    logger.info("取得最新的股市資料")

    DB_Get_stock50_everydaydata.stock50_getdata() #取得最新的股市資料

    time.sleep(5)

    return_stock50_getstock50_check_error = DB_Get_stock50_everydaydata.stock50_getstock50_check_error()#檢查有無異常的資料
    logger.info(return_stock50_getstock50_check_error)
    time.sleep(1)

    print("留言資料的檢測")
    logger.info("留言資料的檢測")
    message_predict_check.message_predict_check() #留言資料的檢測

    print("排行榜的資料更新")
    logger.info("排行榜的資料更新")
    time.sleep(1)

    DB_Use_rank.message_predict_rank_update() #會員排行榜的資料更新
    DB_Use_rank_stock_info.message_predict_rank_update_stock_info_main()#各股排行榜資料更新
    logger.info("---處理完成---"+str(datetime.now().month)+"月"+str(datetime.now().day)+"日 "+str(datetime.now().hour)+":"+str(datetime.now().minute)+":"+str(datetime.now().second))

main()