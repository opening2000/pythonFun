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
    #conn , cur = createConn()
    cur.execute('select urlMd5 , parentUrlMd5 , url , name , level , isVisited from url_main where urlmd5= %s ' , (urlMd5,))
    result = cur.fetchone()
    #closeConn(conn , cur)
    
    if result and len(result) > 0:
        urlMain = UrlMain(result[0] , result[1] ,result[2] ,result[3] ,result[4] ,result[5] )
        return urlMain
    else:
        return None

#保存UrlMain对象
def saveUrlMain(urlMain):
    url = urlMain.url
    parentUrlMd5 = urlMain.parentUrlMd5
    urlMd5 = urlMain.urlMd5
    name = urlMain.name
    level = int(urlMain.level)
    isVisited = urlMain.isVisited
    
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    #conn , cur = createConn()
    cur.execute('insert into url_main(urlMd5 , parentUrlMd5 , url , name , level , isVisited ,inserttime ,updatetime) values(%s,%s,%s,%s,%s,%s,%s,%s)', (urlMd5 , parentUrlMd5 , url , name , level , isVisited , nowStr , nowStr))
    conn.commit()
    #closeConn(conn , cur)
    

#根据urlmd5置validate标志位
def updateUrlMainValiDateByUrlMd5(urlMd5 , valiDate):
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    #conn , cur = createConn()
    cur.execute('update url_main set validate = %s ,updatetime = %s where urlmd5 = %s', (valiDate , nowStr , urlMd5))
    conn.commit()
    #closeConn(conn , cur)

#根据urlmd5置solveFlag标志位
def updateUrlErrorByUrlMd5(urlMd5 , rightUrlMd5, rightUrl, solveFlag):
    nowStr = time.strftime('%Y-%m-%d %H:%M:%S')
    #conn , cur = createConn()
    cur.execute('update url_error set rightUrlMd5 = %s , rightUrl = %s, solveFlag=%s, updatetime = %s where urlmd5 = %s', (rightUrlMd5, rightUrl, solveFlag, nowStr, urlMd5))
    conn.commit()
    #closeConn(conn , cur)


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



def test404(url):
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        content = html.decode('utf-8').encode('utf-8')
        return True
    except Exception , e:
        print 'Exception'
        return False
    except Error , e1:
        print 'Error'
        return False




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
            #print errUrl
            
            #处理下url，看看是不是url拼错了导致的
            #获取到url的根路径，然后后面拼接asp
            #http://so.gushiwen.org/guwen/bookv_2284.aspx/author_820.aspx
#            orgIndex = errUrl.find('.org')
#            if orgIndex > 0:
#                rootUrl = errUrl[0:orgIndex+4]
#            
#            aspxIndex = errUrl.rfind('.aspx')
#            if aspxIndex > -1:
#                u = errUrl[aspxIndex+5:]
#            url = rootUrl + u
            
            #http://so.gushiwen.org/guwen/bookv_2284.aspx/author_820.aspx
            #http://so.gushiwen.org/type.aspx?p=1&t=%e5%b0%8f%e5%ad%a6%e6%96%87%e8%a8%80%e6%96%87/guwen/book_33.aspx
            #http://so.gushiwen.org/guwen/book_19.aspxjavascript:like(19)
            pattern1 = re.compile('(.*?).org/(.*?).aspx.*?/(.*?).aspx',re.S)
            urlItems1 = re.findall(pattern1,errUrl)
            
            if len(urlItems1) >0:
                url = urlItems1[0][0] + '.org/' + urlItems1[0][-1] + '.aspx'
            else:
                pattern2 = re.compile('(.*?).org/(.*?).aspx',re.S)
                urlItems2 = re.findall(pattern2,errUrl)
                if len(urlItems2)>0:
                    url = urlItems2[0][0] + '.org/' + urlItems2[0][-1] + '.aspx'
            
            urlMd5 = getMd5Str(url)
            urlMain = getUrlMainByUrlMd5(urlMd5)
            
            errUrlMd5 = getMd5Str(errUrl)
            #print errUrlMd5
            errUrlMain = getUrlMainByUrlMd5(errUrlMd5)
            
            #没必要去url_cache表中查看是否存在记录了，肯定存在，因为url_cache中也记录了404等的错误链接
            
            #其实不需要对这个链接内容进行解析，只需要判断下是否可以访问就可以，剩下访问链接内容及处理其中链接，由主任务进行就可以了
            if test404(url):
                #如果可以访问
                
                #向url_main表插入一条记录
                if not urlMain:
                    #urlMd5 , parentUrlMd5 , url , name , level , isVisited
                    #print urlMd5 , errUrlMain.parentUrlMd5 , url , errUrlMain.name , errUrlMain.level , '0'
                    urlMain1 = UrlMain(urlMd5 , errUrlMain.parentUrlMd5 , url , errUrlMain.name , errUrlMain.level , '0')
                    saveUrlMain(urlMain1)
                
                #将错误的urlmain置的validdate置为0
                updateUrlMainValiDateByUrlMd5(errUrlMd5, '0')
                
                #如果是这种情况，那么将solveFlag置为2
                updateUrlErrorByUrlMd5(errUrlMd5 , urlMd5, url, '2')
                
            else:
                pass
                #如果不能访问
                #如果不是，将solveFlag置为1
                updateUrlErrorByUrlMd5(errUrlMd5 , '', '', '1')
    

if __name__ == '__main__':
    
    conn , cur = createConn()
    work()
    closeConn(conn , cur)
    
    #test404()





    
