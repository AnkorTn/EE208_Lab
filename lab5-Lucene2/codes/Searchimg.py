# SJTU EE208

INDEX_DIR = "IndexFiles.index"


import jieba

import sys, os, lucene

from java.io import File
from java.nio.file import Path
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

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
def parseCommand(command):
    '''
    input: C title:T author:A language:L
    output: {'contents':C, 'title':T, 'author':A, 'language':L}

    Sample:
    input:'contenance title:henri language:french author:william shakespeare'
    output:{'author': ' william shakespeare',
                   'language': ' french',
                   'contents': ' contenance',
                   'title': ' henri'}
    '''
    #allowed_opt = ['title', 'author', 'language']
    allowed_opt = ['site']
    command_dict = {}
    opt = 'contents'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + value
                #command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + i
            #command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    content = command_dict['contents']
    content = jieba.cut(content, cut_all=False)
    content = " ".join(content)
    command_dict['contents'] = content
    print(command_dict)
    return command_dict

def run(searcher, analyzer):
    while True:
        print()
        print ("Hit enter with no input to quit.")
        command = input("Query:")
        command = jieba.cut(command, cut_all=False)
        command = " ".join(command)
        # command = unicode(command, 'GBK')
        if command == '':
            return

        print()
        print ("Searching for:", command)
        query = QueryParser("data", analyzer).parse(command)
        scoreDocs = searcher.search(query, 100000).scoreDocs
        print("%s total matching documents." % len(scoreDocs))
        cnt = 0
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
##            explanation = searcher.explain(query, scoreDoc.doc)
            print('imgurl:', doc.get("imgurl"))
            print('url:', doc.get("url"))
            print(doc.get('data').replace(' ',''))
            print("\n------------------------")
            cnt += 1
            if(cnt >= 20):
                break
##            print explanation


if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene', lucene.VERSION)
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR).toPath())
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer()
    run(searcher, analyzer)
    del searcher
