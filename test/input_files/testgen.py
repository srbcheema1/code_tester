from random import randint

t = 10

print(t)
for _ in range(t):
    b = randint(1,4)
    if(b==1):
        a = randint(1,int(1e1))
    if(b==2):
        a = randint(1,int(1e3))
    if(b==3):
        a = randint(1,int(1e8))
    if(b==4):
        a = randint(1,int(1e10))
    print(a)
