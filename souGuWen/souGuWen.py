# -*- coding: utf-8 -*-
# souGuWen.py 
# version : 1.1

#1.0    创建这个脚本
#1.1    分页查询

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


import UrlMainUtil
import UrlInfoUtil



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




def findUrlsInPage(url):
    urls = []
    urlmd5 = getMd5Str(url)
    urlMain = UrlMainUtil.getUrlMainByUrlMd5(urlmd5)
    
    #查看此url是否已经被缓存过
    content = UrlInfoUtil.findUrlInfoByUrl(url)
    
    if not content:
        #print 'no cached'
        try:
            #如果url不是以http开头的话，那么要给他拼接上父url
            #要保证url_cache表中的url都是以http开头的，不能是相对路径
            if not url.startswith('http') and not url.startswith('HTTP'):
                parentUrlMain = UrlMainUtil.getUrlMainByUrlMd5(urlMain.parentUrlMd5)
                parentUrl = parentUrlMain.url
                url = parentUrl + url
            
            response = urllib2.urlopen(url)
            html = response.read()
            content = html.decode('utf-8').encode('utf-8')
        except Exception , e:
            print 'Exception'
            content = '404'
            print url , '  404'
        except Error , e1:
            print 'Error'
            content = '404'
            print url , '  404'
        
        #如果content为空，则将content置为404
        if not content:
            content = '404'
        #如果没有缓存过，将内容缓存
        UrlInfoUtil.insertUrlInfoByUrl(url , content)
    
    pattern = re.compile('<a.*?href="(.*?)".*?>(.*?)</a>',re.S)
    urlItems = re.findall(pattern,content)
    
    for item in urlItems:
        url1 = item[0]
        urlName = item[1]
        result = re.subn('<.*?>' , '' , urlName)
        urlName = result[0]
        
        if not url1.startswith('http') and not url1.startswith('HTTP'):
            url1 = url + url1
        #如果这个url已经在缓存表中存在记录了，那么久不需要想url_main表中插入了
        
        #查看缓存表中是否存在对应记录
        urlMd51 = getMd5Str(url1)
        urlMain1 = UrlMainUtil.getUrlMainByUrlMd5(urlMd51)
        
        if urlMain1:
            #已经缓存过了
            pass
            
        else:
            #url_main表还没有记录
            #向url_main表插入记录
            parentUrlMd5 = urlMain.urlMd5
            level = int(urlMain.level) + 1
            isVisited = '0'
            urlMain1 = UrlMainUtil.UrlMain(urlMd51 , parentUrlMd5 , url1 , urlName , level , isVisited)
            UrlMainUtil.saveUrlMain(urlMain1)
        
        
        #print 'url : ' , url
        #if os_name is 'windows':
        #    print 'name : ' , urlName.decode('utf-8').encode('gbk')
        #else:
        #    print 'name : ' , urlName
        urls.append(url1)
        
    return urls


def testRegxReplaceStr():
    name = '<strong>宋词</strong>'
    name = '宋词'
    name = re.subn('<.*?>' , '' , name)
    print name
    print name[0]

#测试下根据urlmd5获取UrlMain对象的方法
def testGetUrlMainByUrlMd5():
    urlMain = UrlMainUtil.getUrlMainByUrlMd5('9166e3ccb4560d45a76c9855f9c4ad48')
    print urlMain.url
    print urlMain.urlMd5
    print urlMain.parentUrlMd5



def test404():
    try:
        response = urllib2.urlopen('/')
        html = response.read()
        content = html.decode('utf-8').encode('utf-8')
    except Exception , e:
        print 'Exception'
    except Error , e1:
        print 'Error'

def work():
    urlRoot = 'http://www.gushiwen.org/guwen/'
    
    #urls = findUrlsInPage(urlRoot)
    #print 'num : ' , len(urls)
    
    urlMd5 = getMd5Str(urlRoot)
    urlMain = UrlMainUtil.getUrlMainByUrlMd5(urlMd5)
    if not urlMain:
        urlMain = UrlMainUtil.UrlMain(urlMd5 , '' , urlRoot , '古诗文网' , 1 , '0')
        UrlMainUtil.saveUrlMain(urlMain)
            
    #testGetUrlMainByUrlMd5()
    
    level = 1
    while level < 8:
        print level
        #根据level和isVisited
        #totalCount = getUrlMainTotalCountAccordingToLevelAndIsVisited(level , '0')
        
        #urlMains = getUrlMainsByLevelAndIsVisited(level , '0')    # 不使用分页的方式
        
        while True:
            urlMains = UrlMainUtil.getUrlMainsByLevelAndIsVisitedLimit(level , '0' , 100 )  #使用分页的方式
            
            #如果urlMains为空，则退出循环
            if not urlMains:
                break
            #如果urlMains长度为0，也要退出循环
            if len(urlMains) == 0:
                break
            
            for urlMain in urlMains:
                findUrlsInPage(urlMain.url)
                #处理完这个url后，将对应的url_main表中标志位置为1
                UrlMainUtil.updateVisitedFlagForUrlMainByUrlMd5(urlMain.urlMd5 , '1')
        
        level = level + 1

if __name__ == '__main__':
    
    work()
    
    #test404()





    
