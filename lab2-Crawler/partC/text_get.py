#This file is to collect all the words from a text.





def clear(word):
    i = len(word)
    #print("{}:{}".format(i,word))
    #7:halfway
    #print(word[1:2])
    #a
    while(i>0 and word[i-1:i].isalpha()==0):
        i-=1
    if(i==0):
        return ""
    return word[0:i]
    




#def text_get(func, size, filename):
def text_get(filename):
#func:需要测试的函数  size:bucket数目  filename:文件名
    words = []
    f = open(filename, 'r')
    for line in f.readlines():
        for word in line.strip().split(' '):
            word = clear(word)
            if(word):
                words.append(word)
    #pay attention to the word ended with ',' or '.'
    f.close()
    print(words)
    #results = [0]*size
    #words_used = []
    #for word in words:
    #    if word not in words_used:
    #        bucket = func(word,size)
    #        results[bucket] += 1
    #        words_used.append(word)
    #return results

text_get("random.txt")