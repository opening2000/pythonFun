# -*- coding: utf-8 -*-
# UrlMainUtil.py
# version : 1.0


#import MySQLdb
#import string, sys

import time
import DBConnectionUtil



#conn = None
#cur = None

class UrlMain:
    
    def __init__(self , urlMd5 , parentUrlMd5 , url , name , level , isVisited):
        self.urlMd5 = urlMd5
        self.parentUrlMd5 = parentUrlMd5
        self.url = url
        self.name = name
        if not level:
            level = 0
        if level == '':
            level = 0
        self.level = int(level)
        self.isVisited = isVisited
    

#根据urlMd5值获取UrlMain对象
def getUrlMainByUrlMd5(urlMd5):
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('select urlMd5 , parentUrlMd5 , url , name , level , isVisited from url_main where urlmd5= %s ' , (urlMd5,))
    result = cur.fetchone()
    DBConnectionUtil.closeConn(conn , cur)
    
    if result and len(result) > 0:
        urlMain = UrlMain(result[0] , result[1] ,result[2] ,result[3] ,result[4] ,result[5] )
        return urlMain
    else:
        return None

def getUrlMainsByLevelAndIsVisited(level , isVisited = '0'):
    urlMains = []
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('select urlMd5 , parentUrlMd5 , url , name , level , isVisited from url_main where level= %s and isVisited = %s' , (level, isVisited))
    results = cur.fetchall()    #获取游标中剩余的所有
    
    for result in results:
        if result and len(result) > 0:
            urlMain = UrlMain(result[0] , result[1] ,result[2] ,result[3] ,result[4] ,result[5] )
            urlMains.append(urlMain)
    DBConnectionUtil.closeConn(conn , cur)
    return urlMains

#分页查找
def getUrlMainsByLevelAndIsVisitedLimit(level , isVisited = '0' , pageSize = 100):
    urlMains = []
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('select urlMd5 , parentUrlMd5 , url , name , level , isVisited from url_main where level= %s and isVisited = %s limit %s' , (level, isVisited , pageSize ))
    results = cur.fetchall()    #获取游标中剩余的所有
    
    for result in results:
        if result and len(result) > 0:
            urlMain = UrlMain(result[0] , result[1] ,result[2] ,result[3] ,result[4] ,result[5] )
            urlMains.append(urlMain)
    DBConnectionUtil.closeConn(conn , cur)
    return urlMains


#查找符合level和isvisited条件的url_main表的记录数
def getUrlMainTotalCountAccordingToLevelAndIsVisited(level , isVisited = '0'):
    totalCount = 0
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('select count(*) from url_main where level= %s and isVisited = %s' , (level, isVisited))
    result = cur.fetchone()
    if result and len(result) > 0:
        totalCount = result[0]
    DBConnectionUtil.closeConn(conn , cur)
    return totalCount
    
    

#保存UrlMain对象
def saveUrlMain(urlMain):
    url = urlMain.url
    parentUrlMd5 = urlMain.parentUrlMd5
    urlMd5 = urlMain.urlMd5
    name = urlMain.name
    level = int(urlMain.level)
    isVisited = urlMain.isVisited
    
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('insert into url_main(urlMd5 , parentUrlMd5 , url , name , level , isVisited ,inserttime ,updatetime) values(%s,%s,%s,%s,%s,%s,%s,%s)', (urlMd5 , parentUrlMd5 , url , name , level , isVisited , nowStr , nowStr))
    conn.commit()
    DBConnectionUtil.closeConn(conn , cur)


#根据urlmd5的值删除url_main表中记录
def deleteUrlMainByUrlMd5(urlmd5):
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('delete from url_main where urlmd5=%s', (urlmd5, ))
    conn.commit()
    DBConnectionUtil.closeConn(conn , cur)

#将Url_main表中的isvisited标志位置为1或者0
def updateVisitedFlagForUrlMainByUrlMd5(urlMd5 , isVisited):
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('update url_main set isvisited = %s ,updatetime = %s where urlmd5 = %s', (isVisited , nowStr , urlMd5))
    conn.commit()
    DBConnectionUtil.closeConn(conn , cur)
    
#根据urlmd5置validate标志位
def updateUrlMainValiDateByUrlMd5(urlMd5 , valiDate):
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('update url_main set validate = %s ,updatetime = %s where urlmd5 = %s', (valiDate , nowStr , urlMd5))
    conn.commit()
    DBConnectionUtil.closeConn(conn , cur)

#根据urlmd5置solveFlag标志位
def updateUrlErrorByUrlMd5(urlMd5 , rightUrlMd5, rightUrl, solveFlag):
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    conn , cur = DBConnectionUtil.createConn()
    cur.execute('update url_error set rightUrlMd5 = %s , rightUrl = %s, solveFlag=%s, updatetime = %s where urlmd5 = %s', (rightUrlMd5, rightUrl, solveFlag, nowStr, urlMd5))
    conn.commit()
    DBConnectionUtil.closeConn(conn , cur)


