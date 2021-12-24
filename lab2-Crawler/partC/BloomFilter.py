import math
from Bitarray import Bitarray
#import GeneralHashFunctions

def BKDRHash(key, j):
    base = [31, 131, 1313, 13131, 131313, 1313131, 13131313, 131313131]
    seed = base[j]# 31 131 1313 13131 131313 etc..
    hash = 0
    for i in range(len(key)):
      hash = (hash * seed) + ord(key[i])
    return hash

#bitarray_obj = Bitarray(size)
#bitarray_obj.set(n_th)
#bitarray_obj.get(n_th)

def clear(word):
    i = len(word)
    while(i>0 and word[i-1:i].isalpha()==0):
        i-=1
    if(i==0):
        return ""
    return word[0:i]

words = []
f = open("random.txt", 'r')
for line in f.readlines():
    for word in line.strip().split(' '):
        word = clear(word)
        if(word):
            words.append(word)
f.close()

#k = ln(2)* m/n (the number of hash functions is k)
#where m=1500000 and n=100000
bitarray_obj = Bitarray(1500000)
cnt = 0
for i in words:
    tmp, flag = 0, 0
    for j in range(0, 8):
        tmp = BKDRHash(i,j) % 1499999
        if bitarray_obj.get( tmp ) :
            flag += 1
        bitarray_obj.set( tmp )
    if flag != 8:
        cnt += 1
print(cnt)
