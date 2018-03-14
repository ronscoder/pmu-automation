import pandas as pd
import os
from utility import bcolors as col

class WhatData():
    """
    Files to deal are mixed and have different data table structure
    File characteristics: 
    Urban: 
        filename will have 'urban'
        column names will have 'urban'

    Objective:
    1. Grab the data row
    2. Grab district and block

    Go through each sheet
    Travel down index 0.
    Find district, block. slno
    
    This object corresponds to each file!
    """
    def __init__(self, file_path):
        self.file = file_path
        self.hab_type = 'unknown'
        self.filename = self.file.split(os.sep)[-1].lower()
        self.ext = self.filename.split('.')[-1].lower()
        self.error = []
        self.data=[]
        self.sheets = {processed:[], skipped:[]}
        self.squeezeButt()
        
    def sentinel(file):
        if(file == '~'): # this is temp file
            return False
        ext = file.split('.')[-1].lower()
        if(not (ext in ['xlsx', 'xlsm', 'xls'])):
            return False
        
        return True
    
    def squeezeButt(self):
        if(self.filename[0]=='~'): # this is temp file
            self.errorlog('Temp file. Skipped')
            return
        
        if(not (self.ext in ['xlsx', 'xlsm', 'xls'])):
            self.errorlog('Not excel file. Skipped')
            return
        
        print('\n\n{}'.format(('='*30).center(30)))
        self.info('File name', self.filename)
        if(not self.is_urban()):
            if(not self.is_rural()):
                self.errorlog('Could not determine the file format')
                return
                
        
    def is_urban(self):
        if(not (self.filename.find('urban') > 0)):
            # Check for 'village' in column idx 1
            df = pd.read_excel(self.file,0, index_col=None, header=None)
            if(df[df[1].str.match('town',case=False)==True].empty):
                return False            

        self.hab_type = 'urban'
        self.parent = True
        self.info('Hab type', self.hab_type)
        self.grab_butts()
        return True

    def is_rural(self):
        self.parent = True # Assume rural hab file
        if(not (self.filename.find('hab') > 0)):
            # Check for 'village' in column idx 1
            self.parent = False # Grid file it is
            df = pd.read_excel(self.file,0, index_col=None, header=None)
            if(df[df[1].str.match('village',case=False)==True].empty):
                return False

        self.hab_type = 'rural'
        self.info('Hab type', self.hab_type)
        self.grab_butts()

        return True

    def find_row(self, what, dtype, where_col, df):
        if(dtype == 'int'):
            return df[where_col] == what
        return df[where_col].str.match(what,case=False)


        """
        self.data = []
            {
                'sheetname': <sheetname>
                'district': <district>
                ...
                'data': table
                    
                }
        }
"""
    def grab_butts(self):
        self.xfile = pd.ExcelFile(self.file)
        sheets = self.xfile.book.sheets()
        for ix, sheet in enumerate(sheets):
            # print('{:20} {} {}'.format(sheet.name, sheet.visibility, sheet.sheet_visible))
            # continue
            # if(sheet.visibility == 0):
            ok, sheetdata = self.extractSheetData(sheet.name)
            if(ok):
                self.data.append(sheetdata)
        
    def extractSheetData(self, sheetname):
        print('\n')
        self.info('Reading sheet',sheetname)
        #1 District name
        df = pd.read_excel(self.xfile, sheetname, index_col = None, header=None)
        result = {}

        allowed_sheetname = ['ongoing', 'town', 'proposed', 'habitat', 'existing']
        valid = False
        for name in allowed_sheetname:
            if(not sheetname.lower().find(name) == -1):
                valid = True
                break
        if(not valid):
            self.info('Skipped','Hidden sheet')
            return False,{}
        result['sheetname'] = sheetname
        
        # DISTRICT
        row = df[0].str.match('district', case=False)

        if(df[row==True].empty):
            self.errorlog('District info (label) not found')
            return False, {}            
        self.district = df[row==True].iloc[0,1]
        result['district'] = df[row==True].iloc[0,1]
        self.info('District', self.district)

        # BLOCK
        row = df[0].str.match('block', case=False)
        if(df[row==True].empty):
            self.errorlog('Block info (label) not found')
            return False, {}             
        self.block = df[row==True].iloc[0,1]
        result['block'] = df[row==True].iloc[0,1]
        self.info('Block', self.block)

        # SL NO 1 DATAROW
        # Print first datarow
        row = df[0] == 1
        if(df[row==True].empty):
            row = df[0].str.match('1')
            if(df[row==True].empty):
                self.errorlog('Datarow sl.no 1 info not found')
                return False, {}      
        self.first_record = df[row==True].iloc[0,:]
        self.info('First record sample\n','')
        print(self.first_record[0:4])
        idx_data = df.index[row==True].tolist()[0]
        # self.data = df.iloc[idx_data:]
        result['data'] = df.iloc[idx_data:]
        self.infraCategory()

        return True,result

        
    def infraCategory(self):
        cols_df = pd.read_csv('table_columns.csv')


            
    def errorlog(self, msg):
        self.error = msg
        print(col.FAIL+ 'ERROR: ' + col.ENDC + col.WARNING + msg + col.ENDC)

    def info(self,label, msg = ''):
        print(col.BOLD+ '{:20}: '.format(label) + col.ENDC + col.OKBLUE + str(msg) + col.ENDC)
