import os
from saub.data_finder import WhatData
from utility import *
import datetime
import pickle
from pathlib import Path

class FileSniffer:
    def __init__(self):
        self.files = {'processed':[], 'skipped':[]}
        self.sheets = []
    
    def all_files_in(self, path):
        """ Get all files in the path 
        Returns list of file paths
        """
        all_files = []

        for folderName, folders, files in os.walk(path):
            for file in files:
                all_files.append(os.path.join(folderName, file))
        return all_files
    
    def build_butts(self, files):
        ok = True
        all_butts = []
        for file in files:
            file = Path(file)
            if(not WhatData.sentinel(file)):
                print('skipping ' + file.name)
                self.files['skipped'].append(file.name)
                continue
            whatData = None
            while(True):
                whatData = WhatData(file)
                if(not whatData.ok):
                    info('\n{}\nFix the following error(s)\n{}'.format(*['#'*30]*2))
                    info('File',file)
                    for error in whatData.errors:
                        errorlog(error, False)
                    ans = action('Make correction')
                    if(ans == 's'):
                        info('Ignoring the errors...')
                        break
                else:
                    self.files['processed'].append(file.name)
                    self.sheets.append({'file': file.name, 'processed': whatData.sheets['processed'], 'skipped': whatData.sheets['skipped']})
                    all_butts.append(whatData)
                    break

        printList('Files processed', self.files['processed'])
        printList('Files skipped', self.files['skipped'])
        # logcsv('files',pd.DataFrame(self.files))
        # logcsv('sheets',pd.DataFrame(self.sheets))
        for sheet in self.sheets:
            printList('Sheets skipped [{}]'.format(sheet['file']), sheet['skipped'])
        return ok, all_butts