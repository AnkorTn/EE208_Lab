# SJTU EE208

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

import jieba

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.analysis.core import WhitespaceAnalyzer


"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer):
    while True:
        print ("Hit enter with no input to quit.")
        command = input("Query:").replace(" ","")
        command = jieba.cut(command, cut_all=False)
        command = " ".join(command)
        #command = " ".join(i for i in command if len(i)>1)
        # command = raw_input("Query:")
        # command = unicode(command, 'GBK')
        #conmand用来设定查找的关键词
        #command = 'EBook'
        #command = 'love'
        if command == '':
            return

        print()
        print ("Searching for:", command)
        query = QueryParser("contents", analyzer).parse(command)
        #应用样例：
        #Query query1 = parser.parse("(name:\"联想笔记本电脑\" OR simpleIntro:英特尔) AND type:电脑 AND price:999900")
        #Finds the top 50 hits for query.
        #scoreDocs = searcher.search(query, 50).scoreDocs
        scoreDocs = searcher.search(query, 50).scoreDocs
        #print(scoreDocs)
        print ("%s total matching documents." % len(scoreDocs))
        #添加标题、路径、内容
        #path title url name
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print ('path:', doc.get("path"), 'title:', doc.get("title"), 'url:', doc.get("url"), 'name:', doc.get("name"))
                #print( 'explain:', searcher.explain(query, scoreDoc.doc))
                #这个是解释如何计算文档的相关因子score的       
    

if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print ('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    #建立一个搜索器，提供搜索的索引为DirectoryReader.open(directory)
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()
    #analyzer = StandardAnalyzer()#Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
