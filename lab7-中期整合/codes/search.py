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


# 引入Flask类：
from flask import Flask, redirect, render_template, request, url_for
#创建Flask对象，我们将使用该对象进行应用的配置和运行：
app = Flask(__name__)

# 使用app变量的route()装饰器来告诉Flask框架URL如何触发我们的视图函数：
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        keyword = request.form['keyword']
        return redirect(url_for('result', keyword=keyword))
    return render_template("search.html")


@app.route('/result', methods=['POST','GET'])
def result():
    # if request.method == "POST":
    #     keyword = request.form['keyword']
    #     return redirect(url_for('result', keyword=keyword))
    
    keyword = request.args.get('keyword')
    keyword = jieba.cut(keyword, cut_all=False)
    keyword = " ".join(keyword)
    # print("keyword:" + str(keyword) + "    type:" + str(type(keyword)))
    # 如果没有搜索情况
    if(keyword == ""):
        return render_template("search.html")
    
    STORE_DIR = "index"
    
    s.attachCurrentThread()
    
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()

    query = QueryParser("contents", analyzer).parse(keyword)
    scoreDocs = searcher.search(query, 1000001).scoreDocs
    
    tmp = str(keyword)
    tmp = tmp.split(' ')
    tmp = ''.join(tmp)

    TEXTS = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        dic = {}
        dic['title'] = doc.get("title")
        dic['url'] = doc.get("url")
        content = doc.get("contents")
        search_word = keyword.split(' ')
        content = content.split(' ')
        j = 0
        test = 1
        #找到关键词左边的内容
        solutionl = []
        #找到关键词右边的内容
        solutionr = []
        flag = False
        for i in search_word:
            #已经找到了一次就直接退出，提高效率
            if(flag):
                break
            #一个一个词找过去比对
            for j in range(0,len(content)):
                if(flag):
                    break
                #找到之后，爬取上下文
                if(i==content[j]):
                    flag = True
                    if(j>0):
                        test = 4
                        while(test>0):
                            if(j-test>=0):
                                solutionl.append(content[j-test])
                            test -= 1
                    if(j<len(content)):
                        test = 1
                        while(j+test<len(content) and test<=4):
                            solutionr.append(content[j+test])
                            test += 1
        #上下文保存并用dic存入
        solutionl = "".join(solutionl)
        solutionr = "".join(solutionr)
        dic['left'] = solutionl
        dic['right']= solutionr
        # print(solutionl)
        # print(solutionr)
        #content ="".join(content.split(' '))
        # print("================")
        #print(content)
        #dic['content'] = conttt
        TEXTS.append(dic)
    return render_template("result.html", keyword=tmp, TEXTS=TEXTS, number=len(TEXTS))



@app.route('/search_img', methods=['POST', 'GET'])
def search_img():
    if request.method == "POST":
        keyword = request.form['keyword']
        return redirect(url_for('result_img', keyword=keyword))
    return render_template("search_img.html")


@app.route('/result_img', methods=['POST','GET'])
def result_img():
    
    keyword = request.args.get('keyword')
    keyword = jieba.cut(keyword, cut_all=False)
    keyword = " ".join(keyword)
    
    if(keyword == ""):
        return render_template("search_img.html")
    
    STORE_DIR = "index2"
    
    s.attachCurrentThread()
    
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()

    query = QueryParser("data", analyzer).parse(keyword)
    scoreDocs = searcher.search(query,1000001).scoreDocs
    
    tmp = str(keyword)
    tmp = tmp.split(' ')
    tmp = ''.join(tmp)
    TEXTS = []
    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        dic = {}
        dic['data'] = doc.get('data').replace(' ','')
        dic['url'] = doc.get("url")
        #url是网页地址，imgurl是图片地址
        dic['imgurl']=doc.get('imgurl')
        TEXTS.append(dic)
    return render_template("result_img.html", keyword=tmp, TEXTS=TEXTS, number=len(TEXTS))


#改名启动一个本地服务器，默认情况下其地址是localhost:5000，在下面的代码中，我们使用关键字参数Port将监听端口修改为8080。
if __name__ == '__main__':
    s = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    app.run(debug=True, port=8080)
