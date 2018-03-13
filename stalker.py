import os
from saub.data_finder import WhatData
from sensible import Give
from utility import *
class FileSniffer:
    def __init__(self):
        pass
    
    def all_files_in(self, path):
        """ Get all files in the path 
        Returns list of file paths
        """
        path = path.strip().replace('\\', '') # will be a cross platform issue
        
        print('Path exists: {}'.format(os.path.exists(path)))
        print('-{}-'.format(path))
        all_files = []

        for folderName, folders, files in os.walk(path):
            # print('Current folder: '.format(folderName))
            # print('Files: ')
            for file in files:
                # print(file)
                all_files.append(os.path.join(path, file))
        return all_files
    
    def build_butts(self, files):
        all_butts = []
        for file in files:
            if(not WhatData.sentinel(file)):
                continue
            whatData = WhatData(file)
            if(not whatData.error==None):
                break    
            all_butts.append(whatData)
        return all_butts
        


if(__name__ == '__main__'):
    stalker = FileSniffer()
    files = stalker.all_files_in(input('Enter directory path: \n'))
    all_butts = stalker.build_butts(files)
    give = Give(all_butts)
    hhTot = give.hh()
    saveFilename = 'hh_totalism.xlsx'
    info('Save directory for', saveFilename)
    path = input('>> ')
    saveFilepath = os.path.join(path + saveFilename)
    hhTot.to_excel(saveFilepath)
    