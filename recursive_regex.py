import re
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

PATTERN =  r"ho(.)a"
SUB = 'hola'
ASK_BEFORE = True
DRY_RUN = True

with open('example.txt', 'rt') as file:
    file_str = file.read()

def get_preceding(start:int, text_str:str):
    preceding = ''
    while(start >=0 and text_str[start]!='\n'):
        preceding = text_str[start] + preceding 
        start = start - 1 
    return preceding

def get_successor(end:int, text_str:str):
    successor = ''
    while(end <len(text_str) and text_str[end]!='\n'):
        successor = successor +text_str[end]
        end = end + 1 
    return successor

#pattern = re.compile(PATTERN)
#for i in pattern.finditer(file_str):

def sub_func(i):
        pre = get_preceding(i.start()-1,i.string)
        suc = get_successor(i.end(), i.string) 
        res = pre + bcolors.WARNING+ i[0] + bcolors.ENDC + suc
        print(res)
        print(' '* len(pre) + bcolors.OKBLUE + i.expand(SUB) + bcolors.ENDC)
        if ASK_BEFORE:
            skip = input('Do this substitution? [Y/n]')=='n'
            if skip: 
                return i.group(0)

        return i.expand(SUB)

res_sub = re.sub(PATTERN, sub_func, file_str)
print(res_sub)
if not DRY_RUN:
    with open('example.txt', 'wt') as file:
        file.write(res_sub)
