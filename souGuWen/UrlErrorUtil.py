# -*- coding: utf-8 -*-
# UrlErrorUtil.py
# version : 1.0



import time
import DBConnectionUtil


#根据urlmd5置solveFlag标志位
def updateUrlErrorByUrlMd5(urlMd5 , rightUrlMd5, rightUrl, solveFlag):
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('update url_error set rightUrlMd5 = %s , rightUrl = %s, solveFlag=%s, updatetime = %s where urlmd5 = %s', (rightUrlMd5, rightUrl, solveFlag, nowStr, urlMd5))
    conn.commit()
    DBConnectionUtil.closeConn(conn , cur)


def findErrorUrlsBySolveFlag(solveFlag, pageSize=100):
    errorUrls = []
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('select url from url_error where solveFlag= %s limit %s' , (solveFlag, pageSize ))
    results = cur.fetchall()    #获取游标中剩余的所有
    
    for result in results:
        if result and len(result) > 0:
            errorUrls.append(result[0])
    
    DBConnectionUtil.closeConn(conn , cur)
    return errorUrls
    
