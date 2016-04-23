# -*- coding: utf-8 -*-
# UrlUtil.py
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

#conn = None
#cur = None



def findUrlInfoByUrl(url):
    #conn , cur = createConn()
    cur.execute('select content from url_cache where url= %s ' , (url,))
    result = cur.fetchone()
    #closeConn(conn , cur)
    #print result is not None    #is not None 是非空
    #print len(result)
    if result and len(result) == 1:
        return result[0]
    else:
        return None


def findUrlInfoByUrlMd5(urlMd5):
    #conn , cur = createConn()
    cur.execute('select content from url_cache where urlmd5= %s ' , (urlMd5,))
    result = cur.fetchone()
    #closeConn(conn , cur)
    #print result is not None    #is not None 是非空
    #print len(result)
    if result and len(result) == 1:
        return result[0]
    else:
        return None


def insertUrlInfoByUrl(url , content):
    urlmd5 = getMd5Str(url)
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    #conn , cur = createConn()
    cur.execute('insert into url_cache(url ,urlmd5 , content ,inserttime ,updatetime) values(%s,%s,%s,%s,%s)', (url , urlmd5 , content , nowStr , nowStr))
    conn.commit()
    #closeConn(conn , cur)


