# -*- coding: utf-8 -*-
# UrlErrorUtil.py
# version : 1.0



import time
import DBConnectionUtil



class UrlError:
    
    def __init__(self, urlMd5, url, rightUrlMd5, rightUrl, errorMessage, solveFlag, solution, insertTime, updateTime):
        self.urlMd5 = urlMd5
        self.url = url
        self.rightUrlMd5 = rightUrlMd5
        self.rightUrl = rightUrl
        self.errorMessage = errorMessage
        self.solveFlag = solveFlag
        self.solution = solution
        self.insertTime = insertTime
        self.updateTime = updateTime


#向url_error插入一条记录
def insertUrlError(urlError):
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('insert into url_error(urlMd5, url, rightUrlMd5, rightUrl, errorMessage, solveFlag, solution, insertTime, updateTime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)', (urlError.urlMd5, urlError.url, urlError.rightUrlMd5, urlError.rightUrl, urlError.errorMessage, urlError.solveFlag, urlError.solution, nowStr, nowStr))
    conn.commit()
    DBConnectionUtil.closeConn(conn , cur)



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
    
