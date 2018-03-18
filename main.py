from stalker import FileSniffer
from saub.sensible import Give
from pathlib import Path
import os
import utility as ut

def get_butts():
    sniffer = FileSniffer()
    dataPath = Path(input('Enter data directory path: \n'))
    if(not dataPath.exists()):
        quit()
    files = sniffer.all_files_in(dataPath)
    ok, all_butts = sniffer.build_butts(files)
    return ok, all_butts

def run_stalker():
    looping = ''
    while(looping == ''):
        # ut.instruction('Enter the habitation folder path')
        ut.instruction('Enter the habitation and grid folder path')
        ok, butts = get_butts()
        if(ok):
            give = Give(butts)
            # give.hh()
            # give.makeMaster()
            # give.verify_rural_hab_data()
            give.habitat_with_propose()

        looping = input('Run again. Enter for yes: ')

def application_config():
    #: output folder
    opath = Path('output')
    opath.mkdir(exist_ok=True)

    #: log folder
    logpath = Path('log')
    logpath.mkdir(exist_ok=True)

if(__name__ == '__main__'):
    application_config()
    run_stalker()