def _check_ints(a,b):
    try:
        a,b = int(a),int(b)
        if a == b: return True
        else: return False
    except:
        return False

def _check_floats(a,b):
    try:
        a,b = float(a),float(b)
        diff = abs(a - b)
        if(diff < 1.0/1e6): return True
        else: return False
    except:
        return False


'''
returns two values diff_line_num and size_diff
function returns -1 as diff_line_num if files are identical
returns line number if difference is there
'''
def comp_files(file1,file2):
    file1 = open(file1)
    file2 = open(file2)

    file1 = file1.read().strip().split('\n')
    file2 = file2.read().strip().split('\n')

    l1 = sum(1 for line in file1)
    l2 = sum(1 for line in file2)

    isIdentical = True
    size_diff = False
    if(l1 != l2):
        size_diff=True
        isIdentical = False

    l,i = min(l1,l2),0
    for i in range(l):
        a = file1[i].strip().lower()
        b = file2[i].strip().lower()
        # check ints
        if(_check_ints(a,b)):
            continue
        if(_check_floats(a,b)):
            continue
        if(a != b):
            isIdentical = False
            break

    if(isIdentical):
        return -1,size_diff
    else:
        return i+1,size_diff
