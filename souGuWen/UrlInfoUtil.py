# -*- coding: utf-8 -*-
# UrlInfoUtil.py
# version : 1.0



import time
import DBConnectionUtil


def findUrlInfoByUrl(url):
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('select content from url_cache where url= %s ' , (url,))
    result = cur.fetchone()
    DBConnectionUtil.closeConn(conn , cur)
    #print result is not None    #is not None 是非空
    #print len(result)
    if result and len(result) == 1:
        return result[0]
    else:
        return None


def findUrlInfoByUrlMd5(urlMd5):
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('select content from url_cache where urlmd5= %s ' , (urlMd5,))
    result = cur.fetchone()
    DBConnectionUtil.closeConn(conn , cur)
    #print result is not None    #is not None 是非空
    #print len(result)
    if result and len(result) == 1:
        return result[0]
    else:
        return None


def insertUrlInfoByUrl(url , content):
    urlmd5 = getMd5Str(url)
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('insert into url_cache(url ,urlmd5 , content ,inserttime ,updatetime) values(%s,%s,%s,%s,%s)', (url , urlmd5 , content , nowStr , nowStr))
    conn.commit()
    DBConnectionUtil.closeConn(conn , cur)

