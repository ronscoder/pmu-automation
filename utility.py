import pandas as pd
import os


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
def instruction(msg):
    print('{}\n'.format('*'*100),col.BOLD + str(msg) + col.ENDC)

def errorlog(msg, interrupt=False):
    print(col.FAIL+ 'ERROR: ' + col.ENDC + col.BOLD + str(msg) + col.ENDC)
    if(interrupt):
        return inputInterrupt()

def info(label, msg = ''):
        print(col.HEADER+ '{:20}: '.format(label) + col.ENDC + col.OKBLUE + str(msg) + col.ENDC)

def warning(msg, interrupt=False):
    print(col.WARNING+ 'Warning: ' + col.ENDC + col.BOLD + str(msg) + col.ENDC)
    if(interrupt):
        return inputInterrupt()

def action(msg):
    print(col.HEADER + msg + col.ENDC)
    return inputInterrupt('[Enter]: Make correction and continue\n[s]: Skip \n[q]: Quit\n_ ')

def inputInterrupt(prompt=':[Enter] to continue \n [q] to quit: '):
    """ signal to proceed or stop """
    accepted_input = ['', 'c','q']
    res = input(prompt)
    if(res == 'q'):
        quit()
    return res

def printList(heading = '', data=[]):
    if(not len(data) > 0):
        return
    df = pd.DataFrame(data)
    print('='*30)
    print(col.BOLD + heading + col.ENDC)
    print(df)

import datetime
def logfile(prefix, msg):
    if(not msg == ''):
        date = datetime.datetime.now().timestamp()
        with open(os.path.join('log','{}{}.txt'.format(prefix,date)), 'w+') as f:
            f.write(msg)

def logcsv(prefix, df):
    if(df.empty):
        return
    date = datetime.datetime.now().timestamp()
    path = os.path.join('log','{}{}.csv'.format(prefix,date))
    df.to_csv(path)

def df_to_file(filename, df):
    date = datetime.datetime.now().timestamp()
    path = os.path.join('output', '{}{}.xlsx'.format(filename,date))
    df.to_excel(path)
    return path
    