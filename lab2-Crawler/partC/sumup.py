from randomtext import new_text
import math
from Bitarray import Bitarray

def BKDRHash(key, j):
    # use "list" to make it easy when calling the function BKDRHash
    # j is the j_th base collect to calculate the hash value
    base = [31, 131, 1313, 13131, 131313, 1313131, 13131313, 131313131]
    seed = base[j]# 31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
        hash = (hash * seed) + ord(key[i])
    return hash


false_rate = []
try_time = 10
try_scale= 5000000

while(try_time):
    #create a new random text
    new_text(try_scale)

    #The first is to operate the random text I produce and collect all the words.
    words = []
    f = open("random.txt", 'r')
    for line in f.readlines():
        for word in line.strip().split(' '):
            words.append(word)
    f.close()



    #Firstly, this is a method using the easiet way to record words only once

    #Before operation
    before = len(words)
    dic = {}
    for i in words:
        if i not in dic:
            dic[i] = 1
    std = len(dic)


    #k = ln(2)* m/n (the number of hash functions is k)
    #where k=8, m=1500000 and n=scale
    #Secondly, we use the bloomfilter to try:
    m = int(20*try_scale)
    bitarray_obj = Bitarray(m+5)
    cnt = 0
    for i in words:
        tmp, flag = 0, 0
        for j in range(0, 8):
            # use the mod calculation to avoid the set being overflowed
            tmp = BKDRHash(i,j) % (m+4)
            # to check whether this url:tmp is in this array
            if bitarray_obj.get( tmp ) :
                flag += 1
            bitarray_obj.set( tmp )
        # if it isn't in it, record it.
        if flag != 8:
            cnt += 1
    

    false_rate.append(1.0-cnt*1.0/std)

    print("Now it's {0} to try, and the scale is {1}, the rate is {2}".format(try_time,try_scale,1.0-cnt*1.0/std))

    #try_scale*=2
    try_time -=1
    
average = 0.0
for i in false_rate:
    average += i
average/=(1.0*len(false_rate))
print(average)







#If it's for an exact text, which means it has some strange characters like"," , "." and so on
#Then we should do something to make it a real word, it should be like this:

#def clear(word):
#    i = len(word)
#    while(i>0 and word[i-1:i].isalpha()==0):
#        i-=1
#    return word[0:i]
#
#words = []
#f = open("random.txt", 'r')
#for line in f.readlines():
#    for word in line.strip().split(' '):
#        word = clear(word)
#        if(word):
#            words.append(word)
#f.close()


