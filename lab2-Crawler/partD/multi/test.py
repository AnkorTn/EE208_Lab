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


content = urllib.request.urlopen("https://www.sjtu.edu.cn/",timeout=500).read()
File = open("T1.txt","w")
File.write(str(content))
File.close()
#print(content)
soup = str(content)
front, rear = 0, 0
links =[]
while(soup.find("href",front)!=-1):
    front = soup.find("http:/",front)
    rear1 = soup.find("\'",front)
    rear2 = soup.find('\"',front)
    rear = min(rear1, rear2)
    if(rear-front>7):
        links.append(soup[front:rear])
        print("front={0},rear={1},{2}".format(front,rear,soup[front:rear]))
    front = rear
front, rear = 0, 0
while(soup.find("href",front)!=-1):
    front = soup.find("https:/",front)
    rear1 = soup.find("\'",front)
    rear2 = soup.find('\"',front)
    rear = min(rear1, rear2)
    if(rear-front > 8):
        links.append(soup[front:rear])
        print("front={0},rear={1},{2}".format(front,rear,soup[front:rear]))
    front = rear


def crawler():
    content = urllib.request.urlopen("https://www.sjtu.edu.cn/",timeout=500).read()
    soup = str(content)
    while(soup.find("href",front)!=-1):
        #爬取的有http开头或者https开头的链接
        front = soup.find("http:/",front)
        #front = soup.find("https:/",front)
        #这些链接基本是以单引号或者上引号结尾的
        rear1 = soup.find("\'",front)
        rear2 = soup.find('\"',front)
        #因为无法判断，所以选取二者的最小
        rear = min(rear1, rear2)
        #如果链接不为空则存入爬取链接中（https则为8）
        if(rear-front>7):
            links.append(soup[front:rear])
            print("front={0},rear={1},{2}".format(front,rear,soup[front:rear]))
        #继续爬取
        front = rear