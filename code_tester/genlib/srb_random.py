from random import randint as randd

# A function to generate a random permutation of arr[]
def randomize(arr):
    n = len(arr)
    for i in range(0,n-1):
        j = randint(i,n-1)
        arr[i],arr[j] = arr[j],arr[i]
    for i in range(n-1,0,-1):
        j = rand(0,i)
        arr[i],arr[j] = arr[j],arr[i]
    return arr

def rand(l,r=-1):
    if(r==-1):
        r=l
        l=1
    return randd(l,r)

def rand_arr(s,l,r=-1):
    arr = []
    for i in range(s):
        arr.append(rand(l,r))
    return arr
