# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:08:44 2015

@author: Oliver
"""

from ftplib import FTP
import zipfile
import io
import pandas as pd
from FTPData_python3 import rename_columns 


def load_current_data():
    
    '''
    DOCUMENTATION
    '''

  
    df_empty = True
    path_recent_data = '/pub/CDC/observations_germany/climate/daily/kl/recent/'
     
    ftp = FTP('ftp-cdc.dwd.de')
    ftp.login()
    listfiles = ftp.nlst(path_recent_data)  
    
    counter = 0    
    N = len(listfiles)    
    
    for zipstring in listfiles:
        
        counter+=1
        print('working on station number', counter, '/',N,'...')
        
        if zipstring.endswith('.zip'):
    
            fh =  io.BytesIO()
            ftp.retrbinary('RETR %s' % zipstring, fh.write)
            fh.seek(0) # rewind pseudo-file
            
            myzip = zipfile.ZipFile(fh) # open zip-file      
            list_in_zip = myzip.namelist() # list names 
            
            # determine the name of our txt-file
            txtfilename = ''
            for name in list_in_zip:
                # the txt-file we need starts with 'produkt_klima_...'
                if name.startswith('produkt_klima_Tageswerte'):
                    txtfilename = name
                    break        
            
            # open txt file
            txtfile = myzip.open(txtfilename)
            
            recent_dataframe=pd.read_csv(txtfile, sep=';')    
            recent_dataframe=recent_dataframe.drop('eor',1)  
            
            date_name = list(recent_dataframe)[1]
            recent_dataframe = recent_dataframe.dropna(subset = [date_name])
            
            #Creating a new dataframe just once at the beginning
            if df_empty:
                recent_data = recent_dataframe
                df_empty = False
                column_names = list(recent_dataframe)
                
            else:
                recent_data = recent_data.append(recent_dataframe)
                
                recent_column_names = list(recent_dataframe)
                if recent_column_names != column_names:
                    print(zipfile, 'has different column names!')
                
            del fh, myzip, list_in_zip, txtfile, recent_dataframe

    ftp.quit()
    
    recent_data=rename_columns(recent_data)
    recent_data=recent_data.sort(['Station ID', 'Date'])

    return recent_data
    
    