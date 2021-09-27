import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')
parent_dir = os.path.dirname(os.path.abspath(__file__))
config.read(parent_dir + "/config.ini")

DBhost=config.get('aws_rd', 'DBhost')   
DBdatabase=config.get('aws_rd', 'DBdatabase')
DBuser=config.get('aws_rd', 'DBuser')
DBpassword=config.get('aws_rd', 'DBpassword')

# DBhost="localhost"
# DBdatabase="stock50_web_v2"
# DBuser="root"
# DBpassword="root"

from DBUtils.PooledDB import PooledDB,SharedDBConnection
import pymysql
def getConnection():
    connection = PooledDB(
    creator=pymysql,
    maxconnections=5,   #最大連接
    mincached=3,        #啟動開啟空連接
    maxcached=6,        #最大可用連接
    maxshared=6,        #大可共享連接
    host=DBhost,
    charset='utf8',
    database=DBdatabase,
    user=DBuser,
    password=DBpassword)
    return connection
