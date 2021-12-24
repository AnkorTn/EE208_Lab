import time
import copy
def make_hashtable(b):
    table = []
    for i in range(0,b):
        table.append([])
    return table

def hashtable_get_bucket(table,keyword):
    return table[ord(keyword[0])%len(table)]

def hash_string(keyword,buckets):
    if keyword!='':
        return ord(keyword[0])%buckets
    else:
        return 0

def hashtable_add(table,keyword):
    table[ord(keyword[0])%len(table)].append(keyword)

def hashtable_lookup(table,keyword):
    if keyword in table[ord(keyword[0])%len(table)]:
        return True
    return False
    
def get_random_string():
    import random
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 6))

tocrawl = [get_random_string() for i in range(10**4)]
tocrawl_copy = copy.deepcopy(tocrawl)	
#print(tocrawl)
#tocrawl.pop()会将tocrawl中的元素全部去掉，需要多复制一份

def time_execution(code):
    start = time.clock()
    result = eval(code)
    run_time = time.clock() - start
    return run_time, result

def crawl(tocrawl):
    crawled = []
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            #crawl page
            crawled.append(page)
    return crawled

def crawl_hashtable(tocrawl):
    table = make_hashtable(100)
    while tocrawl:
        page = tocrawl.pop()
        if not hashtable_lookup(table,page):
            #crawl page
            hashtable_add(table, page)
    return table

[time_crawl, crawled] = time_execution('crawl(tocrawl)')
[time_crawl_hashtable, table] = time_execution('crawl_hashtable(tocrawl_copy)')
print(time_crawl)
print(time_crawl_hashtable)
