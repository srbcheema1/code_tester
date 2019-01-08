# CODE_TESTER

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.ocm/srbcheema1/code_tester/issues)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/srbcheema1/code_tester)
[![Build Status](https://travis-ci.org/srbcheema1/code_tester.svg?branch=master)](https://travis-ci.org/srbcheema1/code_tester)
[![HitCount](http://hits.dwyl.io/srbcheema1/code_tester.svg)](http://hits.dwyl.io/srbcheema1/code_tester)

Code_tester is a command-line code testing tool used to test your codes against codes of your friends/brute-force code.


### Installation

#### Build from Source

- `git clone https://github.com/srbcheema1/code_tester`
- `cd code_tester`
- `python3 setup.py install --user`

#### Install using pip

##### linux and mac users
```
python3 -m pip install --user code_tester
```
Don't forget `~/.local/bin` should be in your `PATH`. Add line `export PATH=$PATH:"~/.local/bin"` in your `~/.bashrc`

##### windows users
for windows users you should have python3 installed in your system
```
python3 -m pip install --user code_tester
```
### Usage

```
srb@srb-pc:$ code_tester --help
usage: code_tester [-h] [-f FILE] [-o OTHER] [-t TEST] [-i ID] [-n NUM]
                   [-s SEC] [-c]
                   [legacy [legacy ...]]

positional arguments:
  legacy                legacy way of args

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file name, ex: one.cpp
  -o OTHER, --other OTHER
                        Other input file name, ex: brute.cpp
  -t TEST, --test TEST  Test generator, ex: testgen.py
  -i ID, --id ID        Unique_id, ex: 111
  -n NUM, --num NUM     Maximum number of test cases, ex: 1000
  -s SEC, --sec SEC     Maximum time in seconds for a test file, ex: 4
  -c, --clean           Clean the files generated by tester

```

#### Argument `--test` may contain a testcase-generator which outputs a testcase OR a custom testcase `txt` file.

```
srb@srb-pc:$ code_tester -f one.cpp -o brute_one.cpp -t testgen.py -n 500
tested 100
tested 200
tested 300
tested 400
tested 500
passed 500 testcases

srb@srb-pc:$ code_tester wrong.cpp brute.cpp testgen.py
Difference detected in outputs
---------Failed Test Case----------
10 11 4
1 0 0 0 0 0 0 1 1 1
!?!!?!?!!!!

---------End of Test Case----------
first difference in line 3
+---+-----------+-----------+
| # | wrong.cpp | brute.cpp |
+---+-----------+-----------+
| 1 | 2         | 2         |
| 2 | 4         | 4         |
| 3 | 3         | 4         |
+---+-----------+-----------+

```

#### Smart enough

- smart enough to detect that `1` is same as `1.0`
- able to detect and ignore difference of less than 1e-6 in float values
- able to ignore trailing white spaces

```
srb@srb-pc:$ code_tester wrong.cpp brute.cpp testgen.py
Difference detected in outputs
---------Failed Test Case----------
10
5 1
13 9
15 2
11 10
16 2
18 9
17 16
13 2
16 16
19 16

---------End of Test Case----------
first difference in line 8
+----+-------------+-----------+
| #  | wrong.cpp   | brute.cpp |
+----+-------------+-----------+
| 1  | 0.33333333  | 0.3333333 |    ignore percision differences smaller than 1e-6
| 2  | 1.00000000  | 1         |    it will detect values are same in 1.0, 1.000 and 1
| 3  | 0.25000000  | 0.2500000 |
| 4  | 1.00000000  | 1         |
| 5  | 0.25000000  | 0.2500000 |
| 6  | 1.00000000  | 1         |
| 7  | 0.14285714  | 0.1428571 |    this line is not marked as diff(smart to detect negligible change)
| 8  | 0.33333333  | 0.2500000 |    this one is 7th line which actually differs
| 9  | 1.00000000  | 1         |
| 10 | 1.00000000  | 1         |
+----+-------------+-----------+

```

### Supported Languages

- c++
- c
- python3
- java
- ruby



### Contact / Social Media

[![Github](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/github.png)](https://github.com/srbcheema1/)
[![LinkedIn](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/linkedin-48x48.png)](https://www.linkedin.com/in/srbcheema1/)
[![Facebook](https://raw.githubusercontent.com/srbcheema1/CheemaFy/master/myPlugins/extra_things/png_images/social/fb.png)](https://www.facebook.com/srbcheema/)


### Developed by

Developer / Author: [Srb Cheema](https://github.com/srbcheema1/)
