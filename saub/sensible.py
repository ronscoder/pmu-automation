#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 02:11:06 2018

@author: ronsair
"""
import pandas as pd
from utility import *
class Give:
    """
    Buttback format:
        Series indexed with District, Block, and the butt values
    """
    def __init__(self, list_butts):
        self.butts = list_butts
        
    def hh(self):
        """
        Extract from village or town details
        columns of interest:
            urban: hab_type = urban, read: town
        """
        ok = True
        cols_urban = dict(
                hh_total = 4,
                hh_bal = 7,
                bpl_total = 8,
                bpl_bal = 11
                )
        cols_rural = dict(
                hh_total = 9,
                hh_bal = 12,
                bpl_total = 13,
                bpl_bal = 16            
                )
        
        data = []
        for butt in self.butts:
            # Skip the grid file
            if(not butt.parent):
                continue
            cols = cols_urban
            if(butt.hab_type == 'rural'):
                cols = cols_rural
                
            if(not ok):
                return []
            habdf = butt.data[0]['data'] # Hoping its always the first, or it's bad butt
            sums = [habdf.iloc[:,col-1].sum() for col in cols.values()]
            data.append([butt.district, butt.block, butt.hab_type] + sums)
            
                
        out_cols = ['district', 'block', 'hab type','total hh','hh bal','total bpl', 'bpl bal']
        df = pd.DataFrame(data,columns=out_cols)
        df.index = df.index + 1
        return df
    
    
        