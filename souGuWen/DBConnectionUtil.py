# -*- coding: utf-8 -*-
# DBConnectionUtil.py
# version : 1.0


import MySQLdb
import ConfigParser
import string, sys



#从db.conf中读取配置参数
cf = ConfigParser.ConfigParser()
 
cf.read("db.conf")

db_host = cf.get("db", "db_host")
db_port = cf.getint("db", "db_port")
db_user = cf.get("db", "db_user")
db_pass = cf.get("db", "db_pass")
db_database = cf.get("db", "db_database")


#mysql
def createConn():
    conn = MySQLdb.connect(host = db_host , user = db_user , passwd = db_pass , port = db_port , charset='utf8')
    cur = conn.cursor()
    conn.select_db(db_database)
    conn.autocommit(1) 
    
    return conn , cur

def closeConn( conn , cur):
    conn.commit()
    cur.close()
    conn.close()

