import subprocess as sp
import os

os.system('g++ --std=c++11 wrong_hello.cpp')
command = 'timeout 2 ./Input.txt < Input.txt'
try:
    p = sp.Popen(command,shell=True)
    p.wait()
    code = p.returncode
    '''
    timeout return codes
    124 timeout
    123 internal error
    126 error executing job
    127 couldn't find the job
    http://git.savannah.gnu.org/cgit/coreutils.git/tree/src/timeout.c
    '''
    '''
    discovered ones
    139 recursive seg-fault
    '''
    print(code)
    print('done')
except KeyboardInterrupt:
    print('got KeyboardInterupt')

