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

from DBUtils.PooledDB import PooledDB,SharedDBConnection
import pymysql
def getConnection():
    connection = PooledDB(
    creator=pymysql,
    maxconnections=3,   
    mincached=2,
    maxcached=5,
    maxshared=3,
    host=DBhost,
    charset='utf8',
    database=DBdatabase,
    user=DBuser,
    password=DBpassword)
    return connection
