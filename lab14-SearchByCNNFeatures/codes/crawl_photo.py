# SJTU EE208

import os
import re
import string
import sys
import urllib.error
import urllib.parse
import urllib.request
from urllib import parse
from bs4 import BeautifulSoup


from bs4 import BeautifulSoup

# 获取域名
basic_site = parse.urlparse("http://www.4399.com/").hostname

def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s

photo_name = {}
def get_name(page):
    if page in photo_name:
        return photo_name[page]
    return ""


def get_page(page):
    try:
        #content = urllib.request.urlopen(page,,2.0).read()
        content = urllib.request.urlopen(page,timeout=2000).read()
        return content
    except:
        print("This is the 1th try for the website {0}".format(page))
        #pass
    return None


def download_photo(page,cnt):
    try:
        #content = urllib.request.urlopen(page,,2.0).read()
        content = urllib.request.urlopen(page,timeout=2000).read()
        print("Picture{0} is already downloaded.website:{1}".format(cnt,page))
        index_filename = 'index.txt'  # index.txt中每行是'网址 对应的文件名'
        folder = 'pic'  # 存放网页的文件夹
        # 判定该图片类型是png还是jpg
        if '.png' in page:
            print("png")
            filename = get_name(page) + str(cnt) + '.png'  # 将网址变成合法的文件名
        else:
            print("jpg")
            filename = get_name(page) + str(cnt) + '.jpg'  # 将网址变成合法的文件名
        index = open(index_filename, 'a')
        index.write(str(page) + '\t' + filename + '\n')
        #index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
        index.close()
        if not os.path.exists(folder):  # 如果文件夹不存在则新建
            os.mkdir(folder)
        # 由于是媒体文件，需要利用wb格式存储
        f = open(os.path.join(folder, filename), 'wb')
        f.write(content)  # 将网页存入文件
        #f.write(content)  # 将网页存入文件
        f.close()

        return True
    except:
        print("This is the {0}th try for the website {1}".format(cnt,page))
    return False


def get_all_links(content, page):
    links = []
    soup = BeautifulSoup(content)
    for i in soup.findAll('a',{"href" : re.compile("^http|^/")}):
        t = i.get('href','')
        t = urllib.parse.urljoin(page, t)
        new_site = parse.urlparse(t).hostname
        # 必须确保准备爬取的网页链接与初始链接在同一域名
        if new_site == basic_site:
            if t not in links:
                links.append(t)
    return links



def get_all_photos(content, page):
    links = []
    soup = BeautifulSoup(content)
    for i in soup.findAll('img'):
        #imgurl即图片网址  data即图片内容
        imgurl = i.get('src','')
        imgurl = urllib.parse.urljoin(page, imgurl)
        if imgurl not in links:
            links.append(imgurl)
            
        data = i.get('alt','')
        # 文件名变成data.jpg
        if imgurl not in photo_name:
            photo_name[imgurl] = data
        
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
    photo = []
    #error url set
    error_url = []
    #

    while tocrawl:
        # 弹出需爬取网址
        page = tocrawl.pop()
        if page not in crawled:
            #
            content = get_page(page)
            if not content:
                error_url.append(page)
                continue
            #
            # 找到所有外链
            outlinks = get_all_links(content, page)
            # 添加仍未爬取的链接
            union_dfs(tocrawl, outlinks)
            # 爬取网页内出现的所有图片的链接
            temp_photo = get_all_photos(content, page)
            # 添加仍不在库的图片的链接
            union_dfs(photo, temp_photo)

            print(page)
            # add_page_to_folder(page, content)
            
            crawled.append(page)
            count += 1
            if count == max_page:
                break
    #######
    print(error_url)
    ######

    # print all pictrues into the indexfiles.
    cnt = 0
    for i in photo:
        if(download_photo(i,cnt)):
            cnt += 1
        print(cnt)
        if cnt>20000:
            break
    return crawled


if __name__ == '__main__':


    seed = "http://www.4399.com/"
    max_page = 500
    #seed = sys.argv[1]
    #max_page = sys.argv[2]
    crawled = crawl(seed, max_page)