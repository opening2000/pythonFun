# -*- coding: utf-8 -*-
# solveUrlError.py 
# version : 1.0


import urllib
import urllib2
import re
import os
import time, threading
#import md5    #md5不被推荐，推荐使用hashlib代替
import hashlib
import MySQLdb
import ConfigParser
import string, sys



os_name = 'windows'
conn = None
cur = None


#从db.conf中读取配置参数
cf = ConfigParser.ConfigParser()
 
cf.read("db.conf")

db_host = cf.get("db", "db_host")
db_port = cf.getint("db", "db_port")
db_user = cf.get("db", "db_user")
db_pass = cf.get("db", "db_pass")
db_database = cf.get("db", "db_database")






def appendStrToFile(filename , str):
    f = open(filename,'a')    #+表示可读可写，open和file都可以返回一个文件对象，不过建议使用open
    #must begin with one of 'r', 'w', 'a' or 'U'
    f.write(str)
    f.close()
    
def writeToFile(fileName , txt , encoding):
    file=codecs.open(fileName,"w",encoding)
    file.write(txt)
    file.close()

#根据字符串得到对应的md5摘要
def getMd5Str(info):
    #m = md5.new()    #md5的方法
    m = hashlib.md5()    #hashlib的方法
    m.update(info)
    return m.hexdigest()


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



#将Url_main表中的isvisited标志位置为1或者0
def updateVisitedFlagForUrlMainByUrlMd5(urlMd5 , isVisited):
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    #conn , cur = createConn()
    cur.execute('update url_main set isvisited = %s ,updatetime = %s where urlmd5 = %s', (isVisited , nowStr , urlMd5))
    conn.commit()
    #closeConn(conn , cur)




def test404():
    try:
        response = urllib2.urlopen('/')
        html = response.read()
        content = html.decode('utf-8').encode('utf-8')
    except Exception , e:
        print 'Exception'
    except Error , e1:
        print 'Error'




def insertUrlInfoByUrl(url , content):
    urlmd5 = getMd5Str(url)
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    #conn , cur = createConn()
    cur.execute('insert into url_cache(url ,urlmd5 , content ,inserttime ,updatetime) values(%s,%s,%s,%s,%s)', (url , urlmd5 , content , nowStr , nowStr))
    conn.commit()
    #closeConn(conn , cur)
    

def findErrorUrlsBySolveFlag(solveFlag, pageSize=100):
    errorUrls = []
    #conn , cur = createConn()
    cur.execute('select url from url_error where solveFlag= %s limit %s' , (solveFlag, pageSize ))
    results = cur.fetchall()    #获取游标中剩余的所有
    
    for result in results:
        if result and len(result) > 0:
            errorUrls.append(result[0])
    
    #closeConn(conn , cur)
    return errorUrls
    



def work():
    
    while True:
        #从url_error表中拿到solveFlag为0的数据，即没有处理过的错误url
        #solveFlag为0，1，2分别表示，错误未处理，处理过但是没成功，处理成功
        errorUrls = findErrorUrlsBySolveFlag('0', 100)
        
        #如果没有需要处理的错误url，那么退出循环
        if not errorUrls and len(errorUrls) == 0:
            break
        
        
        #循环查出来的list
        for errUrl in errorUrls:
            print errUrl
            #处理下url，看看是不是url拼错了导致的
            #获取到url的根路径，然后后面拼接asp
            #http://so.gushiwen.org/guwen/bookv_2284.aspx/author_820.aspx
            orgIndex = errUrl.find('.org')
            if orgIndex > 0:
                rootUrl = errUrl[0:orgIndex+4]
            
            aspxIndex = errUrl.find('.aspx')
            if aspxIndex > -1:
                u = errUrl[aspxIndex+5:]
            newUrl = rootUrl + u
            
            
            
        break    
        #如果是这种情况，那么将solveFlag置为2
        #想url_cache表中插入记录
        #如果不是，将solveFlag置为1
    

if __name__ == '__main__':
    
    conn , cur = createConn()
    work()
    closeConn(conn , cur)
    
    #test404()





    
