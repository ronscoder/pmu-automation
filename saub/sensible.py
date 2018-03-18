#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 02:11:06 2018

@author: ronsair
"""
import pandas as pd
from utility import errorlog, info, printList, df_to_file
import datetime
import os


class Give:
    """
    Buttback format:
        Series indexed with District, Block, and the butt values

    def: splitRuralData ->habdf, proposeddf, existing, ongoing df
    """
    def __init__(self, list_butts):
        self.butts = list_butts
        self.info = []
        self.error = []

    def GroupRuralData(self, butts):
        #: returns habdf1, proposed, existing, ongoingdf1
        if(len(butts) == 0):
            errorlog('Butts not provided. Build butts first')
            return None,None,None,None

        info('Running', 'Creating rural masters')

        habdf1 = pd.DataFrame()
        proposed = pd.DataFrame()
        existing = pd.DataFrame()
        ongoingdf1 = pd.DataFrame()

        for butt in butts:
            # Check only rural
            if(not butt.hab_type == 'rural'):
                continue
            for sheetdata in butt.data:
                sheetname = sheetdata['sheetname']
                data = sheetdata['data']
                data['district'] = sheetdata['district']
                data['block'] = sheetdata['block']
                data['filename'] = butt.filename
                if(not sheetname.lower().find('habitat') == -1):
                    info(butt.filename, sheetname)
                    habdf1 = pd.concat([habdf1, data])
                elif(not sheetname.lower().find('ongoing') == -1):
                    info(butt.filename, sheetname)
                    ongoingdf1 = pd.concat([ongoingdf1, data])
                elif(not sheetname.lower().find('proposed') == -1):
                    info(butt.filename, sheetname)
                    proposed = pd.concat([proposed, data])
        return habdf1, proposed, existing, ongoingdf1

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

        date = datetime.datetime.now().timestamp()
        info('\nSAUB Habitats hh {}'.format('*'*30))
        file = 'hh_totalism-{}.xlsx'.format(date)
        info('Saved to: output/{}'.format(file))
        df.to_excel(os.path.join('output',file))
        return df

    def makeMaster(self):

        habdf1, pro, ex, ongoingdf1 = self.GroupRuralData(self.butts)

        habdf = pd.DataFrame()
        ongoingdf = pd.DataFrame()

        date = datetime.datetime.now().timestamp()
        try:
            if(not habdf1.empty):
                """ Master habitat data """
                habdf['district'] = habdf1.loc[:,'district']
                habdf['block'] = habdf1.loc[:,'block']
                habdf['village'] = habdf1.loc[:,1]
                habdf['census'] = habdf1.loc[:,2]
                habdf['habitat'] = habdf1.loc[:,3]
                habdf['is_main_hab'] = habdf1.loc[:,4]
                habdf['status'] = habdf1.loc[:,5]

                info('\nSAUB Habitats all {}'.format('*'*30))
                file = 'main_habs-{}.xlsx'.format(date)
                info('Saved to: output/{}'.format(file))
                habdf.to_excel(os.path.join('output',file))

                """ Unelectrified main habitat """
                status_un = 'Un-electrified'
                yes = 'Yes'
                un_haddf_main = habdf[(habdf['is_main_hab'] == yes) & (habdf['status'] == status_un)]
                info('\nSAUB HAB MAIN UNELECTRIFIED {}'.format('*'*30))
                file = 'saub_habitat_main_unelectrified-{}.xlsx'.format(date)
                info('Saved to: output/{}'.format(file))
                un_haddf_main.to_excel(os.path.join('output',file))

            if(not ongoingdf1.empty):
                ongoingdf['district'] = ongoingdf1.loc[:,'district']
                ongoingdf['block'] = ongoingdf1.loc[:,'block']
                ongoingdf['village'] = ongoingdf1.loc[:,1]
                ongoingdf['census'] = ongoingdf1.loc[:,2]
                ongoingdf['habitat'] = ongoingdf1.loc[:,3]
                info('\nOngoing  {}'.format('*'*30))
                file = 'ongoing-{}.xlsx'.format(date)
                info('Saved to: output/{}'.format(file))
                ongoingdf.to_excel(os.path.join('output',file))
        except Exception as ex:
            print(ex.args)

    def verify_rural_hab_data(self):
        #: Apply only to rural
        
        habdf, pro, ex, ongoingdf1 = self.GroupRuralData(self.butts)
        info('Task', 'verify rural habitation details')
        info('rule #1', 'unelectrified grid hhs fall under category II.')
        info('', 'significant infra required.')
        info('Rule #2', 'electrified grid hhs has electrified hhs')
        info('', 'fall under either I or III, not II.')
        # print(habdf1.head())
        
        COL_STATUS_IDX = 5
        GRID_ELECTRIFIED = 'Electrified through grid'
        UNELECTRIFIED = 'Un-electrified'

        COL_CATEGORY_IDX = 6
        # I,II,III

        COL_GRID_IDX = 16
        GRID = 'Grid'

        #: unelectrified and grid, and not II
        ifrows1 = habdf[COL_STATUS_IDX] == UNELECTRIFIED
        ifrows2 = habdf[COL_GRID_IDX] == GRID
        notrows = habdf[COL_CATEGORY_IDX] == 'II'
        errdf1 = habdf[ifrows1 & ifrows2 & (notrows == False)]
        errdf1 = errdf1.rename(columns={COL_CATEGORY_IDX:'Category', COL_STATUS_IDX: 'Status', COL_GRID_IDX:'Grid'})
        # printList('Data error: check status, category, and proposal cols', errdf1.values)
        filename = df_to_file('error-category-status',errdf1)
        info('No of records', len(errdf1))
        info('Check details in', filename)

        ifrow1 = habdf[COL_STATUS_IDX] == GRID_ELECTRIFIED
        electrified_df = habdf[ifrow1]
        electrified_df = electrified_df.rename(columns={COL_CATEGORY_IDX:'Category', COL_STATUS_IDX: 'Status', COL_GRID_IDX:'Grid'})
        filename = df_to_file('electrified-through-grid',electrified_df)
        info('No of records', len(electrified_df))
        info('Check details in', filename)
        #and

    def  habitat_with_propose(self):
        #! for rural hh only
        habdf, pro, ex, ongoingdf1 = self.GroupRuralData(self.butts)
        
        if(habdf.empty):
            errorlog('Habitation information is missing')
            return
        if(pro.empty):
            errorlog('Proposed Infra information missing')
            return
        #: common column ids
        hab_on_cols = [1,2,3]
        # pro_on_cols = hab_on_cols.copy()
        #: combine hab and grid
        combineddf = pd.merge(habdf, pro, how='outer', on=hab_on_cols)
        filename = df_to_file('Hab_on_proposed', combineddf)
        info('No of records', len(combineddf))
        info('Filename', filename)


            
        
            
