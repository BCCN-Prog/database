from ftplib import FTP
import zipfile
import StringIO
import pandas as pd

def temporary_load_one_dataset():

    fh =  StringIO.StringIO()
    ftp = FTP('ftp-cdc.dwd.de')
    ftp.login()
    ftp.retrbinary('RETR %s' % '/pub/CDC/observations_germany/climate/daily/kl/recent/tageswerte_KL_00044_akt.zip', fh.write)
    ftp.quit()
    
    fh.seek(0)  # rewind the 
    
    myzip = zipfile.ZipFile(fh)
    
    mylist = myzip.namelist()
    
    accessfile = ''
    for name in mylist:
        if name.startswith('produkt_klima_Tageswerte'):
            accessfile = name
            break
    
    textfile = myzip.open(accessfile)
        
    data=pd.read_csv(textfile, sep=';')    
    data=data.drop('eor',1)
        
    del fh, myzip, mylist, textfile
    
    return data