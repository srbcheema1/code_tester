from sys import argv , exit

def show(*args):
    for arg in args:
        if(type(arg)==list):
            for item in arg:
                print(item,end=' ')
        else:
            print(arg,end = ' ')
    print()
    return


def reader():
    return argv[1:]
