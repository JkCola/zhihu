# coding: utf-8
import urllib, urllib2
import hashlib
import json
import genHtml, db

import sys


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    reqUrlStr = 'http://www.liwushuo.com/api/channels/1/items?limit=100'
    reqHeaders = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    }

    req = urllib2.Request(url = reqUrlStr, headers = reqHeaders)
    res = urllib2.urlopen(req)

    trueUrl = res.geturl()
    head = res.info()
    body = res.read()

    md5Str = hashlib.md5(body).hexdigest()
    jsonObj = json.loads(body)
    print 'md5Str: ', md5Str

    # 链接数据库，只是为了隐藏： MySQLdb.connect(host = 'localhost', port = 3306, user = 'root', passwd = 'root', db = 'liwushuo')
    conn = db.getConnection('liwushuo')
    cur = conn.cursor()

    # 判断当前获取的页面是否已经处理过
    sqlStr = 'select count(*) as cnt from liwushuo_site_md5 where md5=%s'
    retNum = cur.execute(sqlStr, (md5Str, ))
    ret = cur.fetchmany(retNum)
    isChanged = True if retNum > 0 and ret[0][0] < 1 else False
    print 'isChanged: ', isChanged

    if isChanged == True:
        # 记录当前获取的页面的md5，用来后续判断
        sqlStr = 'insert into liwushuo_site_md5 (md5) values (%s);'
        cur.execute(sqlStr, (md5Str, ))

        items = []
        for item in jsonObj['data']['items']:
            url = item['url']
            title = item['title']
            content = item['share_msg']
            imgSrc = item['cover_image_url']
            items.append( (url, title, content, imgSrc) )

        # 数据入库
        sqlStr = "insert ignore into liwushuo_post (url, title, content, img_src) values (%s, %s, %s, %s);"
        print 'update total number: ', cur.executemany(sqlStr, items)

    conn.commit()
    cur.close()
    conn.close()
