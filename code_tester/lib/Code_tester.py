import os
import platform
import sys
from sys import argv,exit
from terminaltables import AsciiTable
import subprocess as sp

from .srbColour import Colour
from .util import Util
from .comp_files import comp_files

class Code_tester:
    def __init__(self,code1,code2,tester_script,maxlim = 10000,idd="0",timeout = "10"):
        self.idd = '_' + str(idd)

        self.os = Util.get_os_name()
        if self.os == 'windows':
            self.timeout = ''
        else:
            self.timeout = 'timeout ' + str(timeout) + 's '

        self.code1 = code1
        self.code2 = code2
        self.base1 = code1.split('/')[-1].split('\\')[-1].split('.')[0]
        self.base2 = code2.split('/')[-1].split('\\')[-1].split('.')[0]
        self.out1 = '.'+self.base1+self.idd+'.tester'
        self.out2 = '.'+self.base2+self.idd+'.tester'

        self.tester_script = tester_script
        self.maxlim = int(maxlim)
        if not Code_tester.check_exception(code1,code2,tester_script):
            sys.exit(0)

        self.exec1 = self.compile_code(self.code1)
        self.exec2 = self.compile_code(self.code2)
        self.exec3 = self.compile_code(self.tester_script)

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

                p = sp.Popen(self.timeout + self.exec3 + ' > .case' + self.idd + '.tester',shell=True)
                p.wait()
                status = p.returncode
                if status == 124:
                    Colour.print('test_gen timed out',Colour.RED)
                    sys.exit(0)
                if status != 0:
                    Colour.print('test_gen runtime_error',Colour.RED)
                    sys.exit(0)

                p = sp.Popen(self.timeout + self.exec1 + ' < .case'+self.idd+'.tester > ' + self.out1,shell=True)
                p.wait()
                status = p.returncode
                if status == 124:
                    Colour.print(self.code1 + ' timed out',Colour.RED)
                    self.print_failed_test()
                    sys.exit(0)
                if status != 0:
                    Colour.print(self.code1 + ' runtime_error',Colour.RED)
                    self.print_failed_test()
                    sys.exit(0)

                p = sp.Popen(self.timeout + self.exec2 + ' < .case'+self.idd+'.tester > ' + self.out2,shell=True)
                p.wait()
                status = p.returncode
                if status == 124:
                    Colour.print(self.code2 + ' timed out',Colour.RED)
                    self.print_failed_test()
                    sys.exit(0)
                if status != 0:
                    Colour.print(self.code2 + ' runtime_error',Colour.RED)
                    self.print_failed_test()
                    sys.exit(0)


                output1 = Code_tester.get_ouput(self.out1)
                output2 = Code_tester.get_ouput(self.out2)

                ret,size_diff = comp_files(self.out1,self.out2)
                if size_diff:
                    Colour.print('Output files differ in size',Colour.PURPLE)
                if ret > -1 or size_diff:
                    Colour.print('Difference detected in outputs',Colour.PURPLE)
                    self.print_failed_test()
                    Colour.print("first difference in line "+str(ret),Colour.PURPLE)
                    self.print_outputs(output1,output2,ret)
                    self.git_diff()
                    sys.exit(0)

                times += 1
                if(self.maxlim > 0 and times>self.maxlim):
                    Colour.print("passed "+str(self.maxlim)+" testcases ",Colour.GREEN)
                    break

        except KeyboardInterrupt:
            Colour.print("tested "+str(times),Colour.GREEN)
            Colour.print('exiting safely',Colour.GREEN)


    def print_failed_test(self):
        failed_test = Code_tester.get_ouput('.case'+self.idd+'.tester')
        if(len(failed_test.split('\n')) < 30):
            Colour.print('---------Failed Test Case----------',Colour.YELLOW)
            print(failed_test)
            Colour.print('')
            Colour.print('---------End of Test Case----------',Colour.YELLOW)
        else:
            Colour.print('Testcase file having more than 30 lines',Colour.YELLOW)

    def git_diff(self):
        '''
        TODO: to be implemented
        '''
        return

    def print_outputs(self,output1,output2,ret):
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
            # Only print the bad line
            if(len(output1.split('\n')) > ret and len(output2.split('\n')) > ret):
                table_data = [[self.code1, self.code2],
                        [output1.split('\n')[ret-1], output2.split('\n')[ret-1]]]
                print(AsciiTable(table_data).table)


    @staticmethod
    def clean():
        os.system('rm .*.tester') # tester files clean

    @staticmethod
    def get_ouput(file_path):
        with open(file_path) as out_handler:
            output = out_handler.read().strip().split('\n')
            output = '\n'.join(
                [line.strip() for line in output])
            return output

    def compile_code(self,code):
        base,ext = code.split('\\')[-1].split('/')[-1].split('.')


        if self.os == 'windows':
            if not ext in ['c', 'cpp', 'java', 'py', 'rb','exe']:
                Colour.print('Supports only C, C++, Python, Java, Ruby and cpp-binary as of now.',Colour.RED)
                sys.exit(1)
            compiler = {
                'py': None,
                'rb': None,
                'exe': None,
                'c': 'gcc -DONLINE_JUDGE -o .' + base + '.tester',
                'cpp': 'g++ -DONLINE_JUDGE -std=c++14 -o .' + base + '.tester',
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
                'exe': code,
                'c': '.' + base + '.tester',
                'cpp': '.' + base + '.tester',
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
                'c': 'gcc -static -DONLINE_JUDGE -g -fno-asm -lm -s -O2 -o .' + base + '.tester',
                'cpp': 'g++ -static -DONLINE_JUDGE -g -lm -s -x c++ -O2 -std=c++14 -o .' + base + '.tester',
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
                'out': './' + code,
                'c': './.' + base + '.tester',
                'cpp': './.' + base + '.tester',
                'java': 'java -DONLINE_JUDGE=true -Duser.language=en -Duser.region=US -Duser.variant=US ' + base
            }[ext]

        return execute_command

