import pandas as pd
import os
from pathlib import Path
from utility import *

class DDUGHY:
    def __init__(self):
        self.files = []
    
    def readFiles(directory):
        # Walk
        path = Path(directory)
        if(not path.exists()):
            
        if(path.is_file):
            self.files.append(directory)
        else:
            for dir, dirs, files in os.walk(directory):
                for file in files:
                    filePath = os.path.join(dir, file)
                    self.files.append(filePath)
        if(len(self.files) == 0):
            # No files
            errorlog('No files in {}'.format(directory))

    def parseFile(raw_df):
        return None
    
    def getVillageDetails():
        return None
