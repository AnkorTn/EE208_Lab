# SJTU EE208

import re
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def parseZhihuDaily(content, url):
    zhihulist = list()



    ########################
    #利用BeautifulSoup将网页内容content转化为方便操作的数据结构soup
    soup = BeautifulSoup(content)

    #首先爬取图片网址
    for i in soup.findAll('img',{"class":"preview-image"}):
        t = i.get('src','')
        #这里的图片网址利用列表来封装起来，方便后面的项目直接append
        s = []
        s.append(t)        
        zhihulist.append(s)
    
    #其次爬取文本内容，为保证一对一，此处设立了计数器cccnt
    cccnt = 0
    for i in soup.findAll('span',{"class":"title"}):
        t = i.string
        #将文本内容append到相应的图片网址之后
        zhihulist[cccnt].append(t)
        #另一种写法
        #t = i.contents
        #zhihulist[cccnt].append(t[0])
        cccnt += 1

    #最后爬取网页链接，同样设立了计数器cnt
    cnt = 0
    for i in soup.findAll('a',{"class":"link-button"}):
        t = i.get('href','')
        #由于这里得到的链接为/story...故需要与知乎的网站连接成绝对地址
        zhihulist[cnt].append(urllib.parse.urljoin(url, t))
        cnt += 1
    ########################

    return zhihulist


def write_outputs(zhihus, filename):
    file = open(filename, "w", encoding='utf-8')
    for zhihu in zhihus:
        for element in zhihu:
            file.write(element)
            file.write('\t')
        file.write('\n')
    file.close()


def main():
    url = "http://daily.zhihu.com/"
    
    ####
    ########
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36')
    ########
    ####
    
    content = urllib.request.urlopen(url).read()
    zhihus = parseZhihuDaily(content, url)
    write_outputs(zhihus, "res3.txt")







if __name__ == '__main__':
    main()
