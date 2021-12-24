# SJTU EE208

import threading
import queue
import time
import urllib.error
import urllib.parse
import urllib.request
import os
import re
import string
import sys
from bs4 import BeautifulSoup







def valid_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    n = 10
    while(n):
        try:
            print('downloading page %s' % page)
            #content = urllib.request.urlopen(page,timeout=50).read()
            content = urllib.request.urlopen(page).read()
            return content
        except:
            print("This is the {0}th try for the website {1}".format(n,page))
            n-=1
            #pass
    return None




def get_all_links(content, page):
    links = []
    soup = str(content)
    front = 0
    rear = 0
    while(soup.find("href",front)!=-1):
        while(soup[front:front+4]!="http"):
            front += 1
        rear = front
        while(soup[rear:rear+1]!='"' or soup[rear:rear+1]!="'"):
            rear += 1
        links.append(soup[front:rear])
        front = rear
    return links








#def get_all_links(content, page):
#    links = []
#    soup = BeautifulSoup(content)
#    for i in soup.findAll('a',{"href" : re.compile("^http|^/")}):
#        t = i.get('href','')
#        t = urllib.parse.urljoin(page, t)
#        if t not in links:
#            links.append(t)
#    return links


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



def working():

    global count
    
    while True:
        page = q.get()

        if page not in crawled:

            content = get_page(page)
            #网页如果访问无效则本次任务结束，继续进行之后的任务
            if not content:
                q.task_done()
                continue
            #
            outlinks = get_all_links(content, page)
            add_page_to_folder(page, content)
            for link in outlinks:
                q.put(link)
            
            ##锁住变量count操作

            varLock.acquire()
            count += 1
            if(count>=100):
                varLock.release()
                while 1:
                    try:
                        q.task_done()
                    except:
                        break
                return
            graph[page] = outlinks
            crawled.append(page)
            varLock.release()
            
            ##

            q.task_done()



start = time.time()
###
###count在操作的过程中需要注意锁死，不然容易被其他线程访问
###
NUM = 8

count = 0   #先从访问100份出发

crawled = []
graph = {}
varLock = threading.Lock()
q = queue.Queue()
q.put("https://www.sjtu.edu.cn/")
#q.put("https://www.baidu.com")
for i in range(NUM):
    t = threading.Thread(target=working)
    t.setDaemon(True)
    t.start()
q.join()
#while(count<100):
#    time.sleep(1)
#    pass
end = time.time()
print(end - start)