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

PATTERN =  "ho.a"
PATTERN =  r"(ho.a)"

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


pattern = re.compile(PATTERN)
for i in pattern.finditer(file_str):
    #print(re.sub("(ho.a)",bcolors.OKBLUE+ "\g<0>"+ bcolors.ENDC, file_str))
#    import pdb; pdb.set_trace()
    res = get_preceding(i.start()-1,file_str) + bcolors.OKBLUE+ i[0] + bcolors.ENDC + get_successor(i.end(), file_str) 
    print(res)
