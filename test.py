#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 01:15:24 2018

@author: ronsair
"""

from saub.data_finder import WhatData
import pandas as pd

file = 'bish_urban.xlsm'
whatdata = WhatData(file)

xfile = pd.ExcelFile(file)

sheets = xfile.book.sheets()
df = pd.read_excel(xfile, sheets[3].name, index_col=None, header=None)

row = df[0].str.match('district',case=False)
df[row==True].empty


'this '.center(10)