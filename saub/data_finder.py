import pandas as pd
import os
from utility import bcolors as col, errorlog, info, warning
from functools import reduce
from pathlib import Path

class WhatData():
    """
    Files to deal are mixed and have different data table structure
    File characteristics: 
    Urban: 
        filename will have 'urban'
    Objective:
    1. Grab the data row
    2. Grab district and block

    Go through each sheet
    Travel down index 0.
    Find district, block. slno

    This object corresponds to each file!
        self.data = [
                'sheetname': <sheetname>
                'district': <district>
                ...
                'data':
                    'district':...
                    'block':...
                    ...
                    'data': <raw data table>
    """

    def __init__(self, file_path, checksheets=['ongoing', 'town', 'proposed', 'habitat', 'existing']):
        self.file = file_path
        self.hab_type = 'unknown'
        self.filename = self.file.name
        self.ext = self.file.suffixes[-1]
        self.district = None
        self.block = None
        self.errors = []
        self.ok = True
        self.infos = []
        self.warnings = []
        self.data = []
        self.checksheets = checksheets
        self.sheets = {'processed': [], 'skipped': []}
        self.rerun = False
        self.squeezeButt()

    def sentinel(file):
        if(file.name[0] == '~'):  # this is temp file
            return False
        ext = file.suffixes[-1]
        if(not (ext in ['.xlsx', '.xlsm', '.xls'])):
            return False

        return True

    def squeezeButt(self):
        print('\n{}'.format(('=' * 30).center(30)))
        self.info('File name', self.filename)
        if(not self.is_urban()):
            if(not self.is_rural()):
                self.errorlog('Could not determine the habitation type from file name')
                return
        self.grab_butts()

    def is_urban(self):
        if(not (self.filename.find('urban') > 0)):
            return False
        self.hab_type = 'urban'
        self.parent = True
        self.info('Hab type', self.hab_type)
        return True

    def is_rural(self):
        self.parent = True  # Assume rural hab file
        if(not (self.filename.find('hab') > 0)):
            self.parent = False  # Grid file it is
        self.hab_type = 'rural'
        self.info('Hab type', self.hab_type)
        return True

    def find_row(self, what, dtype, where_col, df):
        if(dtype == 'int'):
            return df[where_col] == what
        return df[where_col].str.match(what, case=False)

    def grab_butts(self):
        self.xfile = pd.ExcelFile(self.file)
        sheets = self.xfile.book.sheets()
        for ix, sheet in enumerate(sheets):
            self.info('Reading sheet', sheet.name.lower())
            isSheetinScope = False
            for s in self.checksheets:
                if(not sheet.name.lower().find(s) == -1):
                    isSheetinScope = True
                    break
            if(not isSheetinScope):
                self.warning('Sheet not in scope', False)
                self.sheets['skipped'].append(sheet.name)
                continue
            self.ok, sheetdata = self.extractSheetData(sheet.name)
            if(not self.ok):
                return
            self.sheets['processed'].append(sheet.name)
            self.data.append(sheetdata)

    def extractSheetData(self, sheetname):
        df = pd.read_excel(self.xfile, sheetname, index_col=None, header=None)
        result = {}
        result['sheetname'] = sheetname

        # DISTRICT
        row = df.iloc[:,0].astype(str).str.match('district', case=False)
        if(df[row == True].empty):
            self.errorlog('District info (label) not found')
            return False, {}
        district = str(df[row == True].iloc[0, 1]).strip().lower()
        if(self.district is not None and not self.district == district):
            if(self.warning('District mismatched: {}<>{}'.format(self.district, district)) == 'c'):
                self.rerun = True
                # return False
        self.district = district
        result['district'] = district
        self.info('District', district)

        # BLOCK
        row = df.iloc[:,0].astype(str).str.match('block', case=False)
        if(df[row == True].empty):
            self.errorlog('Block info (label) not found')
            return False, {}
        block = str(df[row == True].iloc[0, 1]).strip().lower()
        if(self.block is not None and not self.block == block):
            self.warning('Block mismatched: {}<>{}'.format(self.block, block))
        self.block = block
        result['block'] = block
        self.info('Block', self.block)

        # SL NO 1 DATAROW
        # Print first datarow
        row = df.iloc[:,0] == 1
        if(df[row == True].empty):
            row = df.iloc[:,0].astype(str).str.match('1')
            if(df[row == True].empty):
                self.errorlog('Datarow sl.no 1 info not found')
                return False, {}
        self.first_record = df[row == True].iloc[0, :]
        self.info('First record sample\n', '')
        print(self.first_record[0:4])
        idx_data = df.index[row == True].tolist()[0]
        result['data'] = df.iloc[idx_data:]
        # self.infraCategory()

        return True, result

    def infraCategory(self):
        cols_df = pd.read_csv('table_columns.csv')

    def errorlog(self, msg):
        self.errors.append(msg)
        return errorlog(msg) 

    def info(self, label, msg=''):
        self.infos.append([label, msg])
        return info(label,msg)
    
    def warning(self, msg, interrupt=True):
        self.warnings.append(msg)
        return warning(msg, interrupt=interrupt)
