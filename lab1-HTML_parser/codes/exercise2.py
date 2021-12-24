# SJTU EE208

import re
import sys
import urllib.request

from bs4 import BeautifulSoup


def parseURL(content):
    urlset = set()

    ########################
    #利用BeautifulSoup将网页内容content转化为方便操作的数据结构soup
    soup = BeautifulSoup(content)
    for i in soup.findAll('img'):
        
        #找到链接
        t = i.get('src','')
        
        #判断合法性
        p1 = re.compile('^http.*$')
        m1 = p1.match(t)

        p2 = re.compile('^//.*$')
        m2 = p2.match(t)
        
        #若合法，则加入集合urlset中
        if(m1 or m2):
            urlset.add(t)
    ########################

    return urlset


def write_outputs(urls, filename):
    file = open(filename, 'w', encoding='utf-8')
    for i in urls:
        file.write(i)
        file.write('\n')
    file.close()


def main():
    url = "http://www.baidu.com"
    content = urllib.request.urlopen(url).read()
    urlSet = parseURL(content)
    write_outputs(urlSet, "res2.txt")


if __name__ == '__main__':
    main()
