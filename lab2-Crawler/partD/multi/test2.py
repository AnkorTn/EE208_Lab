# SJTU EE208

import threading
import queue
import time
import urllib
import os
import re
import string
import sys
from bs4 import BeautifulSoup


import re
from urllib.request import urlopen

url="https://www.sjtu.edu.cn/"
#url = "https://www.baidu.com/"
#req = urllib.request.Request(url)
#req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36')
soup = urllib.request.urlopen(url).read()

print(str(soup))
tag1 = re.findall(r'<a href="([a-zA-z]+://[^\s]*)"', str(soup))
tag2 = re.findall(r'<a href="(/[^\s]*)"', str(soup))

print(tag1)
tag2 = [url+i for i in tag2]
print(tag2)