import urllib.request
from bs4 import BeautifulSoup
#content = urllib.request.urlopen('http://www.baidu.com').read()
#soup = BeautifulSoup(content)
#print("*********************************")
#print(soup.head)
#print("*********************************")
#print(soup.head.title)
#print("*********************************")
#print(str(soup.head.title).encode('utf8').decode('utf8'))
#print("*********************************")
#print(str(soup.head.title.string))
#print("*********************************")
#print(soup.head.meta['content'])
#print("*********************************")
#print(soup.head.meta.get('content',''))
#print("*********************************")



import re
p = re.compile('a\dc')	#定义匹配规则，\d表示一个数字（0-9）
string1 = 'a1c'	#待检测的字符串
m = p.match(string1)
print(type(m))
print (m)		#如果结果不为None，表示匹配上
print (m.group())	#匹配的结果
string2 = 'abc'
m = p.match(string2)
print(type(m))
print (m)
if(type(m)==type(p.match(" "))):
    print(True)