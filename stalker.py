import os
from saub.data_finder import WhatData
from saub.sensible import Give
from utility import *
import datetime
class FileSniffer:
    def __init__(self):
        pass
    
    def all_files_in(self, path):
        """ Get all files in the path 
        Returns list of file paths
        """
        path = path.strip()
        pathe = path.split(os.sep)
        # path = os.path.join(*pathe)
        
        print('Path exists: {}'.format(os.path.exists(path)))
        print('-{}-'.format(path))
        all_files = []

        for folderName, folders, files in os.walk(path):
            # print('Current folder: '.format(folderName))
            # print('Files: ')
            for file in files:
                # print(file)
                all_files.append(os.path.join(folderName, file))
        return all_files
    
    def build_butts(self, files):
        ok = True
        all_butts = []
        for file in files:
            if(not WhatData.sentinel(file)):
                print('skipping ' + file)
                continue
            whatData = WhatData(file)
            if(len(whatData.error) > 0):
                continue    
            all_butts.append(whatData)
        return ok, all_butts
        


if(__name__ == '__main__'):
    looping = ''
    while(looping == ''):
        stalker = FileSniffer()
        files = stalker.all_files_in(input('Enter directory path: \n'))
        # print(files)
        ok, all_butts = stalker.build_butts(files)
        if(ok):
            give = Give(all_butts)
            dfhhTot = give.hh()
            path = 'x'
            if(len(dfhhTot) > 0):
                date = datetime.datetime.now()
                saveFilename = 'hh_totalism-{}.xlsx'.format(date.timestamp())
                dfhhTot.to_excel(saveFilename)
                info('Save directory for', saveFilename) 
                path = input('>> ')
            if(not path == 'x'):
                saveFilepath = os.path.join(path + saveFilename)
                dfhhTot.to_excel(saveFilepath)
            looping = input('Run again. Enter for yes: ')