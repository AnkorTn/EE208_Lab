# SJTU EE208

import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    n = 10
    #设定最多进行10次重连尝试
    while(n):
        try:
            # 给予一定的访问时间缓冲 timeout
            content = urllib.request.urlopen(page,timeout=2000).read()
            return content
        except:
            # 告诉用户具体哪个网页在访问时出了问题
            print("This is the {0}th try for the website {1}".format(n,page))
            n-=1
    return None
#Question:如果网页无法访问的情况下，返回什么值才能继续进行操作呢？
#例如这个无法打开的网站：http://www.beian.miit.gov.cn/

def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content)
    for i in soup.findAll('a',{"href" : re.compile("^http|^/")}):
        t = i.get('href','')
        #将相对链接转化为绝对连接（如果是http开头则不会改变）
        t = urllib.parse.urljoin(page, t)
        if t not in links:
            links.append(t)
    return links


def union_dfs(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中
    index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'html'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(str(page.encode('ascii', 'ignore')) + '\t' + filename + '\n')
    #index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(str(content))  # 将网页存入文件
    #f.write(content)  # 将网页存入文件
    f.close()


def crawl(seed, max_page):
    tocrawl = [seed]
    crawled = []
    count = 0

    #error url set
    error_url = []
    #

    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            # 获取网页内容
            content = get_page(page)
            # 发现获取的是空的，即获取失败
            if not content:
                # 此处设立了一个无法访问网页的记录列表可以供使用者参考
                error_url.append(page)
                continue
            #
            print(page)
            # 网页保存后记入文件夹中
            add_page_to_folder(page, content)
            # 存储外链
            outlinks = get_all_links(content, page)
            union_dfs(tocrawl, outlinks)
            # 爬取完毕，已经爬取的网页数+1
            crawled.append(page)
            count += 1
            if count >= max_page:
                #######
                ##print(error_url)
                ######
                return crawled
    #######
    ##print(error_url)
    ######
    return crawled


if __name__ == '__main__':


    #seed = "https://www.sjtu.edu.cn/"
    #max_page = 100

    seed = sys.argv[1]
    max_page = int(sys.argv[2])

    crawled = crawl(seed, max_page)