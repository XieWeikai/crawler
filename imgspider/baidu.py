import os
import re

import requests
import fake_useragent
from imgspider import proxy

url = 'https://image.baidu.com/search/acjson'  # baidu 图片api

# 通过chrome开发者工具查看的相关参数
params = {
    'tn': 'resultjson_com',  # 不明意义
    'ipn': 'rj',  # 不明意义
    'ct': '201326592', # 不明
    'fp': 'result',    # 不明
    'word': '',        # 查询词
    'queryWord': '',   # 查询词
    'cl': '2',
    'lm': '-1',
    'ie': 'utf-8',
    'oe': 'utf-8',
    'nc': '1',
    'pn': '0',         # 从第几条数据开始
    'rn': ''           # 要查询几条数据
}

headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',#此条少了就会"Forbid spider access"
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',#此条少了就会"Forbid spider access"
        'Upgrade-Insecure-Requests': '1'
}

# 百度有些数据字段加密了，这是网上找到的一段解密程序
# 但后来发现貌似不需要这个函数就行
# 在replace_Url里面有原始链接
def baidtu_uncomplie(url):
    res = ''
    c = ['_z2C$q', '_z&e3B', 'AzdH3F']
    d = {'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h', 't': 'i', '3': 'j', 'h': 'k',
         's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p', 'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v',
         'o': 'w', '8': '1', 'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9', 'a': '0',
         '_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}
    if (url == None or 'http' in url):
        return url
    else:
        j = url
        for m in c:
            j = j.replace(m, d[m])
        for char in j:
            if re.match('^[a-w\d]+$', char):
                char = d[char]
            res = res + char
        return res

# 爬取百度上图片的类
class baidu_img(object):
    # 搜索关键词
    # 如要爬苹果的图片则 spider = baidu_img('苹果')
    def __init__(self,key_word):
        self.key_word = key_word

    # 获取图片
    # 返回一个迭代器
    # 每一个迭代的元素为(data,content)
    # data为一个dict 各个字段如下:
    # title:图片源网页的标题 from:图片源网页url
    # imgURL:图片url type:图片类型
    # word: 查询的关键词
    # content为图片内容(二进制数据，可以直接写入文件即得到图片)
    def get_imgs(self,num,img='origin'):
        p = params.copy()
        p['word'] = self.key_word
        p['queryWord'] = self.key_word
        p['rn'] = str(num)
        headers['User-Agent'] = fake_useragent.UserAgent().random
        r = proxy.get(url,params=p,headers=headers)
        try:
            data = r.json()['data']
        except requests.exceptions.JSONDecodeError as e:
            print('\n')
            print(e)
            print(r.text)
            print('\n')
            return
        except Exception as e:
            print(e)
            return

        for item in data:
            if item:
                d = {}
                try:
                    d['title'] = item['fromPageTitleEnc']
                    d['from'] = baidtu_uncomplie(item['fromURL']) # item['replaceUrl'][0]['FromURL']
                    d['imgURL'] = baidtu_uncomplie(item['objURL']) # item['replaceUrl'][0]['ObjURL']
                    d['thumb'] = item['thumbURL']
                    # d['imgOrigin'] = baidtu_uncomplie(item['objURL'])
                    d['type'] = item['type']
                    d['word'] = self.key_word
                    if img == 'origin':
                        r = requests.get(d['imgURL'],headers=headers)
                    else:
                        r = requests.get(d['thumb'],headers=headers)
                except KeyError as e:
                    print('\n')
                    print(e)
                    print(r.text)
                    print('-----------------------------------')
                    print(item)
                    print('\n')
                    continue

                if r.status_code == 200:
                    yield d,r.content


if __name__ == '__main__':
    word = '三体水滴'
    t = baidu_img(word)
    try:
        os.makedirs(word)
    except OSError:
        print(OSError)
    cnt = 0
    for d,content in t.get_imgs(5,img='thumb'):
        print(d)
        s = '%s%d.%s'%(d['word'],cnt,d['type'])
        with open(os.path.join(word,s),'wb') as f:
            f.write(content)
        cnt += 1


