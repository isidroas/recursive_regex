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

PATTERN = "ho.a"

with open('example.txt', 'rt') as file:
    file_str = file.read()

pattern = re.compile(PATTERN)
for i in pattern.finditer(file_str):
    # TODO: elimina otras lineas
    print(re.sub("(ho.a)",bcolors.OKBLUE+ "\g<0>"+ bcolors.ENDC, file_str))
