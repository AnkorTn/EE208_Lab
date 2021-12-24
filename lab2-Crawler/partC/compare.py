def clear(word):
    i = len(word)
    while(i>0 and word[i-1:i].isalpha()==0):
        i-=1
    return word[0:i]

words = []
f = open("random.txt", 'r')
for line in f.readlines():
    for word in line.strip().split(' '):
        word = clear(word)
        if(word):
            words.append(word)
f.close()

#Before operation
before = len(words)
print(before)

#This is a method using the easiet way to record words only once
dic = {}
for i in words:
    if i not in dic:
        dic[i] = 1
#print(len(dic))
std = len(dic)
print(std)