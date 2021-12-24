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


import sys, os, lucene, threading, time
from datetime import datetime

# from java.io import File
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField
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

    def __init__(self, root, storeDir):
        
        #若地址不存在则建立相应文件夹
        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        # store = SimpleFSDirectory(File(storeDir).toPath())
        #store 将文件存入文件系统中
        store = SimpleFSDirectory(Paths.get(storeDir))
        #建立分词器analyzer，规则为StandardAnalyzer(中英文皆可适用)
        #可以1.对原有句子按照空格进行了分词2.所有的大写字母都可以能转换为小写的字母3.可以去掉一些没有用处的单词，例如"is","the","are"等单词，也删除了所有的标点
        
        analyzer = WhitespaceAnalyzer()
        #analyzer = StandardAnalyzer()

        #限定分词器内token的数量，防止过大
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        #IndexWriter的实例化
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        #建立以store为基础、config配置的索引
        writer = IndexWriter(store, config)


        self.indexDocs(root, writer)
        ticker = Ticker()
        print('commit index')
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print('done')

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
        t2.setStored(False)
        t2.setTokenized(True)
        t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)  # Indexes documents, frequencies and positions.
        
        #将index.txt里面的url以及对应的文件名保存下来，dic是文件名指向网址的一个字典
        File = open("index.txt","r")
        dic = {}
        #urls = []
        #Filename = []
        for url in File.readlines():
            front = url.find('\t')
            #建立从文件名->网页链接的字典关系
            dic[url[front+1:-1]+'.html']=url[:front]
            #urls.append(url[:front])
            #Filename.append(url[front+1:-1])


        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                #文件夹内无文件，则跳出循环
                if not filename.endswith('.html'):
                    continue
                #正在将filename.txt加入writer内
                print("adding", filename)
                try:
                    path = os.path.join(root, filename)
                    file = open(path, encoding='gbk')
                    try:
                        contents = file.read()
                    except UnicodeDecodeError:
                        file = open(path, encoding='utf-8', errors="ignore")
                        contents = file.read()
                    #file = open(path, encoding='gbk', errors='ignore')
                    soup = BeautifulSoup(contents,features="html.parser")
                    contents = ''.join(soup.findAll(text=True))
                    #contents内仅保留汉字进行分词
                    contents = re.sub("[^\u4e00-\u9fa5]","",contents)
                    contents = jieba.cut(contents, cut_all=False)
                    contents = ' '.join(contents)
                    #此处限制长度是为了保证减少一定的无意义词的出现，如 的 地 了 哦 啊...
                    #contents = ' '.join(i for i in contents if len(i)>1)
                    file.close()
                    #添加标题、路径、内容
                    #path title url name
                    title = soup.find('title').string
                    doc = Document()
                    doc.add(Field("path", path, t1))
                    doc.add(Field("title", title, t1))
                    doc.add(Field("url", dic[filename], t1))
                    doc.add(Field("name", filename, t1))


                    #对contents利用jieba进行分词操作
                    if len(contents) > 0:
                        doc.add(Field("contents", contents, t2))
                    else:
                        print("warning: no content in %s" % filename)
                    writer.addDocument(doc)
                    #IndexWriter调用函数addDocument将索引写到索引文件夹中
                    #print(doc)
                    #doc是对文件内的文档进行的整合，并全部放入writer内，供其他文件的使用

                except Exception as e:
                    print("Failed in indexDocs:", e)
        

if __name__ == '__main__':
    lucene.initVM()#vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    # import ipdb; ipdb.set_trace()
    start = datetime.now()
    try:
        IndexFiles('html', "index")
        end = datetime.now()
        print(end - start)
    except Exception as e:
        print("Failed: ", e)
        raise e
