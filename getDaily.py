# coding: utf-8
import urllib, urllib2
import hashlib
from bs4 import BeautifulSoup
import MySQLdb
import genHtml


if __name__ == '__main__':

    # str = u'中问'
    # print str.encode('utf-8')

    reqUrlStr = 'http://daily.zhihu.com/'
    reqHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    }

    req = urllib2.Request(url = reqUrlStr, headers = reqHeaders)
    res = urllib2.urlopen(req)

    trueUrl = res.geturl()
    head = res.info()
    body = res.read()

    md5Str = hashlib.md5(body).hexdigest()
    soup = BeautifulSoup(body)
    print 'md5Str: ', md5Str

    # 链接数据库
    conn = MySQLdb.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'root',
            db = 'zhihu'
        )
    conn.set_character_set('utf8')
    cur = conn.cursor()

    # 判断当前获取的页面是否已经处理过
    sqlStr = 'select count(*) as cnt from zhihu_site_md5 where md5=%s'
    retNum = cur.execute(sqlStr, (md5Str, ))
    ret = cur.fetchmany(retNum)
    isChanged = True if retNum > 0 and ret[0][0] < 1 else False
    print 'isChanged: ', isChanged

    # 如果没有被处理过，即当前获取的页面变化了
    if isChanged == True:
        # 记录当前获取的页面的md5，用来后续判断
        sqlStr = 'insert into zhihu_site_md5 (md5) values (%s);'
        cur.execute(sqlStr, (md5Str, ))

        aTags = []
        for aTag in soup.find_all('a'):
            url = aTag.get('href')
            # 过滤、只得到真正的知乎日报url
            if url.find('daily.zhihu.com/story') >= 0:
                title = aTag.span.string
                aTags.append( (url, title) )
        # 数据入库
        sqlStr = "insert ignore into zhihu_daily (url, title) values (%s, %s);"
        print 'update total number: ', cur.executemany(sqlStr, aTags)

    sqlStr = 'select * from zhihu_daily;'
    retNum = cur.execute(sqlStr)
    ret = cur.fetchmany(retNum)
    genHtml.do( ret );

    conn.commit()
    cur.close()
    conn.close()