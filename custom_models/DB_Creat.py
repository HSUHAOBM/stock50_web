import DB_Creattable_DB
import DB_Creattable_stock50_DB
#建立table
DB_Creattable_DB.member_basedata() #會員資料庫
DB_Creattable_DB.message_predict() #會員預測推文

DB_Creattable_stock50_DB.stock50_data()#建立股市資料庫
DB_Creattable_stock50_DB.stock50_stopdeal_date()#建立休市資料庫


#存資料

#頻率一年一次
DB_Creattable_stock50_DB.getstock50_stopdeal()#將休市資料存入

#頻率每天一次
