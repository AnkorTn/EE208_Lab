# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import jieba

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

from urllib import parse

import sys, os, lucene, threading, time, re
from datetime import datetime

from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from org.apache.lucene.analysis.core import WhitespaceAnalyzer

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir).toPath())
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

    #找到contents里面的attr属性内容，如self.getTxtAttribute(contents, 'Title')
    def getTxtAttribute(self, contents, attr):
        m = re.search(attr + ': (.*?)\n',contents)
        if m:
            return m.group(1)
        else:
            return ''
    def indexDocs(self, root, writer):   

        t1 = FieldType()
        #是否存储
        t1.setStored(True)
        #是否分词
        t1.setTokenized(False)
        #   Allows to set the indexing options, possible values are docs (only doc numbers are indexed)
        #   freqs (doc numbers and term frequencies), and positions (doc numbers, term frequencies and positions).
        #   Defaults to positions for analyzed fields, and to docs for not_analyzed fields. 
        #   It is also possible to set it to offsets (doc numbers, term frequencies, positions and offsets).
        t1.setIndexOptions(IndexOptions.NONE)  # Not Indexed
        
        t2 = FieldType()
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)  # Indexes documents, frequencies and positions.


        #将index.txt里面的url以及对应的文件名保存下来，dic是文件名指向网址的一个字典
        File = open("index.txt","r")
        dic = {}
        for url in File.readlines():
            front = url.find('\t')
            #建立从文件名->网页链接的字典关系
            dic[url[front+1:-1]+'.html']=url[:front]
        File.close()

        url_picture = []
        #判断url是否已经被读入了

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.html'):
                    continue
                print("adding", filename)
                try:
                    path = os.path.join(root, filename)


                    file = open(path, encoding='gbk')
                    try:
                        contents = file.read()
                    except UnicodeDecodeError:
                        file = open(path, encoding='utf-8', errors="ignore")
                        contents = file.read()
                    soup = BeautifulSoup(contents,features="html.parser")
                    file.close()
                    doc = Document()

                    for i in soup.findAll('img'):
                        #imgurl即图片网址  data即图片内容
                        imgurl = i.get('src','')
                        data= i.get('alt','')
                        #url = path
                        #data需要分词与url合并
                        #防止图片有大量重复
                        if(imgurl in url_picture):
                            continue
                        url_picture.append(imgurl)
                        #分词
                        data = jieba.cut(data, cut_all=False)
                        data = ' '.join(data)
                        #将内容放入doc中，其中data需要建立搜索，故需要以t2的域
                        if len(data) > 0:
                            doc.add(Field("data", data, t2))
                            doc.add(Field("imgurl", imgurl, t1))
                            doc.add(Field("url", dic[filename], t1))
                            #测试是否有加入
                            #print("data = {0}, imgurl = {1}, url={2}".format(data,imgurl,dic[filename]))
                        else:
                            print("warning: no content in %s" % filename)
                        #data分词与imgurl一起加入内部    
                    writer.addDocument(doc)
                except Exception as e:
                    print("Failed in indexDocs:", e)

if __name__ == '__main__':
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    start = datetime.now()
    try:
        """
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))
                   """
        analyzer = WhitespaceAnalyzer()
        IndexFiles('html', "index", analyzer)
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
