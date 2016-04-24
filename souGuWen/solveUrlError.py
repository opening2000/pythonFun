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



import UrlMainUtil
import UrlInfoUtil
import UrlErrorUtil



os_name = 'windows'


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





def work():
    
    while True:
        #从url_error表中拿到solveFlag为0的数据，即没有处理过的错误url
        #solveFlag为0，1，2分别表示，错误未处理，处理过但是没成功，处理成功
        errorUrls = UrlErrorUtil.findErrorUrlsBySolveFlag('0', 100)
        
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
            urlMain = UrlMainUtil.getUrlMainByUrlMd5(urlMd5)
            
            errUrlMd5 = getMd5Str(errUrl)
            #print errUrlMd5
            errUrlMain = UrlMainUtil.getUrlMainByUrlMd5(errUrlMd5)
            
            #没必要去url_cache表中查看是否存在记录了，肯定存在，因为url_cache中也记录了404等的错误链接
            
            #其实不需要对这个链接内容进行解析，只需要判断下是否可以访问就可以，剩下访问链接内容及处理其中链接，由主任务进行就可以了
            if test404(url):
                #如果可以访问
                
                #向url_main表插入一条记录
                if not urlMain:
                    #urlMd5 , parentUrlMd5 , url , name , level , isVisited
                    #print urlMd5 , errUrlMain.parentUrlMd5 , url , errUrlMain.name , errUrlMain.level , '0'
                    urlMain1 = UrlMainUtil.UrlMain(urlMd5 , errUrlMain.parentUrlMd5 , url , errUrlMain.name , errUrlMain.level , '0')
                    UrlMainUtil.saveUrlMain(urlMain1)
                
                #将错误的urlmain置的validdate置为0
                UrlMainUtil.updateUrlMainValiDateByUrlMd5(errUrlMd5, '0')
                
                #如果是这种情况，那么将solveFlag置为2
                UrlErrorUtil.updateUrlErrorByUrlMd5(errUrlMd5 , urlMd5, url, '2')
                
            else:
                pass
                #如果不能访问
                #如果不是，将solveFlag置为1
                UrlErrorUtil.updateUrlErrorByUrlMd5(errUrlMd5 , '', '', '1')
    

if __name__ == '__main__':
    
    conn , cur = createConn()
    work()
    closeConn(conn , cur)
    
    #test404()





    
