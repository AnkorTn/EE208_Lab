import random
#The file is to create a random text to be operated
#l is the length of a random word
#k = ln(2)* m/n (the number of hash functions is k)
#where m=1500000 and n=100000
def new_text(n):
    # written in the file:"random.txt"
    f = open("random.txt","w")
    while(n):
        l = random.randint(1,12)
        word=""
        while(l):
            # choose a random word from a to z, which is 1 to 26 in the rank
            tmp=random.randint(1,26)
            # change the integer number 1 to 26 to the character number 'a' to 'z'
            word+=chr(tmp+96)
            l-=1
        f.write(word+" ")
        n -= 1
    f.close()