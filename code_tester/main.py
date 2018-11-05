#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK


import os
import sys
from terminaltables import AsciiTable

from .lib.args import Args
from .lib.srbColour import Colour
from .lib.Code_tester import Code_tester

describe='''
script to check codes of cheema and other are identical or not
takes 4 arguments:

1 your file          --- your code       --- compiled to c<idd>.tester  --- gives output outc<idd>
2 tester/brute file          --- other's code    --- compiled to o<idd>.tester  --- gives output outo<idd>
3 testgen file      --- python          --- generates test<idd>
4 maxlim            --- max limit       --- not computlsory         --- default val 10000
5 idd               --- unique id       --- not compulsory          --- default val 0
6 sec               --- time in sec     --- not compulsory          --- default 10

NOTE    --- 4th, 5th and 6th argument are not necessary
        --- but please make sure to give argumensts while running the tester multiple times
        --- you can give value of maxlim to be -1 to rum infinitely

also you can clean the testing files by
code_tester --clean <idd>
'''


def main():
    parser = Args.get_parser()
    if parser.clean:
        Code_tester.clean()
        sys.exit(0)

    code1 = parser.file
    code2 = parser.other
    tester_script = parser.test
    idd = parser.id
    maxlim = parser.num
    maxtime = parser.sec

    code_tester = Code_tester(code1,code2,tester_script,maxlim,idd,maxtime)
    code_tester.test()

if(__name__=="__main__"):
    main()
