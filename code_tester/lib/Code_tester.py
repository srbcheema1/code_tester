import os
import platform
import sys
from sys import argv,exit
from terminaltables import AsciiTable

from .srbColour import Colour
from .util import Util
from .comp_files import comp_files

class Code_tester:
    def __init__(self,code1,code2,tester_script,maxlim = 10000,idd="0",timeout = "10"):
        self.idd = '_' + str(idd)

        self.code1 = code1
        self.code2 = code2
        self.base1 = code1.split('.')[0]
        self.base2 = code2.split('.')[0]
        self.out1 = self.base1+self.idd+'_tester'
        self.out2 = self.base2+self.idd+'_tester'

        self.tester_script = tester_script
        self.maxlim = int(maxlim)
        if not Code_tester.check_exception(code1,code2,tester_script):
            sys.exit(0)

        self.os = Util.get_os_name()
        self.exec1 = self.compile_code(self.code1)
        self.exec2 = self.compile_code(self.code2)
        self.exec3 = self.compile_code(self.tester_script)
        if self.os == 'windows':
            self.timeout = ''
        else:
            self.timeout = 'timeout ' + str(timeout) + 's '

    def check_exception(file1,file2,tester_script):
        if(not os.path.exists(file1)):
            print('no file of name '+file1)
            return False
        if(not os.path.exists(file2)):
            print('no file of name '+file2)
            return False
        if(not os.path.exists(tester_script)):
            print('no file of name '+tester_script)
            return False
        return True


    def test(self):
        times = 0
        try:
            while(True):
                if(times%100==0 and times > 0):
                    Colour.print("tested "+str(times),Colour.CYAN)
                elif(times%10==0):
                    Colour.print("tested "+str(times),Colour.GREEN,end='\r')

                status = os.system(self.timeout + self.exec3 + ' > tester_case' + self.idd) # tester_exec
                if status == 31744:
                    Colour.print('test_gen timed out',Colour.RED)
                    sys.exit(1)
                if status != 0:
                    Colour.print('test_gen runtime_error',Colour.RED)
                    sys.exit(1)

                status = os.system(self.timeout + self.exec1 + ' < tester_case' + self.idd + ' > ' + self.out1)
                if status == 31744:
                    Colour.print(self.code1 + ' timed out',Colour.RED)
                    sys.exit(1)
                if status != 0:
                    Colour.print(self.code1 + ' runtime_error',Colour.RED)
                    sys.exit(1)

                status = os.system(self.timeout + self.exec2 + ' < tester_case' + self.idd + ' > ' + self.out2)
                if status == 31744:
                    Colour.print(self.code2 + ' timed out',Colour.RED)
                    sys.exit(1)
                if status != 0:
                    Colour.print(self.code2 + ' runtime_error',Colour.RED)
                    sys.exit(1)

                output1 = Code_tester.get_ouput(self.out1)
                output2 = Code_tester.get_ouput(self.out2)
                failed_test = Code_tester.get_ouput('tester_case'+self.idd)

                ret,size_diff = comp_files(self.out1,self.out2)
                if size_diff:
                    Colour.print('Output files differ in size',Colour.PURPLE)
                if ret > -1 or size_diff:
                    Colour.print('Difference detected in outputs',Colour.PURPLE)
                    if(len(failed_test.split('\n')) < 30):
                        Colour.print('---------Failed Test Case----------',Colour.YELLOW)
                        print(failed_test)
                        Colour.print('')
                        Colour.print('---------End of Test Case----------',Colour.YELLOW)

                    Colour.print("first difference in line "+str(ret),Colour.PURPLE)
                    printed_output = False
                    if(len(output1.split('\n')) < 30 and len(output2.split('\n')) < 30):
                        table_data = [['#',self.code1, self.code2]]
                        output1 = output1.split('\n')
                        output2 = output2.split('\n')
                        l1 = len(output1)
                        l2 = len(output2)
                        for i in range(max(l1,l2)):
                            o1,o2 = '',''
                            if i < l1: o1 = output1[i]
                            if i < l2: o2 = output2[i]
                            table_data.append([str(i+1),o1,o2])

                        print(AsciiTable(table_data).table)
                        printed_output = True

                    if(not printed_output):
                        if(len(output1.split('\n')) > ret and len(output2.split('\n')) > ret):
                            table_data = [[self.code1, self.code2],
                                    [output1.split('\n')[ret],output2].split('\n')[ret]]
                            print(AsciiTable(table_data).table)

                    # git diff

                    sys.exit(0)

                times += 1
                if(self.maxlim > 0 and times>self.maxlim):
                    Colour.print("passed "+str(self.maxlim)+" testcases ",Colour.GREEN)
                    break
        except KeyboardInterrupt:
            Colour.print("tested "+str(times),Colour.GREEN)
            Colour.print('exiting safely',Colour.GREEN)

    @staticmethod
    def clean():
        os.system("rm tester_case*") # testcase
        os.system('rm *.tester') # executables
        os.system('rm *_tester') # outputs

    @staticmethod
    def get_ouput(file_path):
        with open(file_path) as out_handler:
            output = out_handler.read().strip().split('\n')
            output = '\n'.join(
                [line.strip() for line in output])
            return output

    def compile_code(self,code):
        base,ext = code.split('.')


        if self.os == 'windows':
            if not ext in ['c', 'cpp', 'java', 'py', 'rb','exe']:
                Colour.print('Supports only C, C++, Python, Java, Ruby and cpp-binary as of now.',Colour.RED)
                sys.exit(1)
            compiler = {
                'py': None,
                'rb': None,
                'exe': None,
                'c': 'gcc -DONLINE_JUDGE -o ' + base + '.tester',
                'cpp': 'g++ -DONLINE_JUDGE -std=c++14 -o ' + base + '.tester',
                'java': 'javac -d .'
            }[ext]

            # COMPILE
            if not compiler is None:
                compile_status = os.system(compiler + ' "' + code + '"') #spaces in path
                if compile_status != 0:
                    Colour.print('Compilation error.', Colour.RED)
                    os.system(compiler + ' "' + code + '"') #spaces in path
                    sys.exit(1)

            execute_command = {
                'py': 'python "' + code + '"',
                'rb': 'ruby "' + code + '"',
                'exe': '' + base + '.exe',
                'c': '' + base + '.tester',
                'cpp': '' + base + '.tester',
                'java': 'java -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ' + base
            }[ext]

        else:
            if not ext in ['c', 'cpp', 'java', 'py', 'rb', 'out']:
                Colour.print('Supports only C, C++, Python, Java, Ruby and cpp-binary as of now.',Colour.RED)
                sys.exit(1)
            compiler = {
                'py': None,
                'rb': None,
                'out': None,
                'c': 'gcc -static -DONLINE_JUDGE -g -fno-asm -lm -s -O2 -o ' + base + '.tester',
                'cpp': 'g++ -static -DONLINE_JUDGE -g -lm -s -x c++ -O2 -std=c++14 -o ' + base + '.tester',
                'java': 'javac -d .'
            }[ext]

            # COMPILE
            if not compiler is None:
                compile_status = os.system(compiler + ' \'' + code + '\'') #spaces in path
                if compile_status != 0:
                    Colour.print('Compilation error.', Colour.RED)
                    os.system(compiler + ' \'' + code + '\'') #spaces in path
                    sys.exit(1)

            execute_command = {
                'py': 'python3 \'' + code + '\'',
                'rb': 'ruby \'' + code + '\'',
                'out': './' + base + '.out',
                'c': './' + base + '.tester',
                'cpp': './' + base + '.tester',
                'java': 'java -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ' + base
            }[ext]

        return execute_command

