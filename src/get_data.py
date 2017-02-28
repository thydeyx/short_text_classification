# -*- coding:utf-8 -*-
#
#        Author : TangHanYi
#        E-mail : thydeyx@163.com
#   Create Date : 2017-01-22 11:53:38 CST
# Last modified : 2017-01-24 05:09:53 CST
#     File Name : get_data.py
#          Desc :
import requests
import json
import time
import md5
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getParam(tmp):

    asas = ''
    cpcp = ''
    t = int(tmp / 1e3)
    e = str(hex(t)).upper()
    m1 = md5.new()
    m1.update(str(t))
    i = m1.hexdigest().upper()
    if len(e) != 8:
        asas = 'A1F578081475106'
        cpcp = '588425417036CE1'
    else:
        n = i[0:5]
        o = i[-5:]
        a = ''
        for s in range(5):
            a += n[s] + e[s]
        r = ''
        for c in range(5):
            r += e[c + 3] + o[c]
        asas = 'A1' + a + e[-3:]
        cpcp = e[0:3] + r + 'E1'
    return (asas, cpcp)


if __name__ == "__main__":
    target = 'game'
    result_file = open(target + '.json', 'a')
    log = open('log.log', 'w')
    headers = {
        'Host': 'www.toutiao.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.toutiao.com/',
        'Connection': 'keep-alive',
        'Cookie': 'csrftoken=ecb0a87f5b1c11a957ad4731eb47e1f2; tt_webid=47715174110; uuid="w:7550576205d1458ba96310c7058bdb14"; CNZZDATA1259612802=146458814-1483523793-https%253A%252F%252Fwww.baidu.com%252F%7C1485057404; _ga=GA1.2.1787530265.1483523908; __tasessionId=vfdnjky4a1485057620141',
        'Cache-Control': 'max-age=0',
    }
    """
    url = 'http://www.toutiao.com/api/article/user_log/?c=/news_tech/&ev=article_show_count&ext_id=7&sid=vfdnjky4a1485057620141&type=event&t=1485058787814'
    url = 'http://www.toutiao.com/api/article/user_log/?c=/news_tech/&ev=refresh_item_click&sid=vfdnjky4a1485057620141&type=event&t=1485058787502'
    url = 'http://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=1485050845&as=A145E8F844232E3&cp=5884D3229EE33E1'
    url = 'http://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=1485053545&as=A155E8489463616&cp=588433E69146EE1<F6>'
    url = 'http://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=1485053545&as=479BB4B7254C150&cp=7E0AC8874BB0985'
    url = 'http://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source=toutiao&widen=1&max_behot_time=0&max_behot_time_tmp=1485053545&as=' + asas + '&cp=' + cpcp
    """
    i = 1
    t = 1485244755
    while i < 10000:
        asas, cpcp = getParam(t)
        url = 'http://www.toutiao.com/api/pc/feed/?category=news_' + target + '&utm_source=toutiao&widen=1&max_behot_time=' + str(t) + '&max_behot_time_tmp=' + str(t) + '&as=' + asas + '&cp=' + cpcp
        t -= 1200
    
        try:
            r = requests.get(url, headers=headers)
            content = r.content.decode('utf-8')
            d = json.loads(r.content)
            print url + '\t' + str(i) + '\t' + str(len(d['data']))
            """
            for key,value in d.items():
                print key,value
                print "#" * 30
            """
            if len(d['data']) == 0:
                for key,value in d.items():
                    print key,value,url
            for info in d['data']:
                info['label'] = target
                info_json = json.dumps(info)
                print >> result_file, info_json
            i += 1
        except Exception as e:
            continue
