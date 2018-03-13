class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

col = bcolors
def errorlog(msg):
    print(col.FAIL+ 'ERROR: ' + col.ENDC + col.WARNING + msg + col.ENDC)

def info(label, msg = ''):
        print(col.BOLD+ '{:20}: '.format(label) + col.ENDC + col.OKBLUE + msg + col.ENDC)