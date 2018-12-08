from code_tester import rand, show, reader, randomize

n_ = 100000

t = rand(1,10)
print(t)

for _ in range(t):
    n = rand(300,n_)
    m = rand(1,100)
    print(n,m)

    a = [int(x) for x in range(1,n+1)]
    a = randomize(a)
    for i in range(m):
        print(a[i],end=" ")
    print()

    a = randomize(a)
    for i in range(1,n):
        temp = rand(0,i-1)
        print(a[temp],a[i])
