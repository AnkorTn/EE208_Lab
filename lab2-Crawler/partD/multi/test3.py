import re
import urllib.request
 
response = urllib.request.urlopen("https://weixin.sogou.com/")
html = response.read()
tag = re.findall(r'<a href="([a-zA-z]+://[^\s]*)"', str(html))
print(tag)