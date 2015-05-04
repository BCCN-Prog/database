# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:08:44 2015

@author: Oliver
"""

from ftplib import FTP
import zipfile
import io
import pandas as pd
from FTPData import rename_columns 

CORRUPT_STATIONS = ['02494_akt.zip','02532_akt.zip','04878_akt.zip']    
#These are the corrupt stations of the RECENT database. They have no 
#information (dead stations) and they break the format of the database.


def load_current_data(): 
    '''
    Load the whole
    '''    

  
    df_empty = True
    path_recent_data = '/pub/CDC/observations_germany/climate/daily/kl/recent/'
     
    ftp = FTP('ftp-cdc.dwd.de')
    ftp.login()
    listfiles = ftp.nlst(path_recent_data)  
    
    counter = 0    
    N = len(listfiles)        
    
    for zipstring in listfiles:
        corrupted = False
        for corrupt_station in CORRUPT_STATIONS:
            if zipstring.endswith(corrupt_station):
                corrupted = True
                break
        
        if corrupted:
            continue
        
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
            recent_dataframe=recent_dataframe.dropna(axis = 0)
            recent_dataframe.iloc[:,0] = int(recent_dataframe.iloc[0,0])

            #Creating a new dataframe just once at the beginning
            if df_empty:
                recent_data = recent_dataframe
                df_empty = False
                column_names = recent_dataframe.columns
                up_col_names = [str(item).strip().upper() for item in column_names]
                
                df_empty = False
            else:
 
                current_column_names = recent_dataframe.columns
                
                if (current_column_names != column_names).any() :
                    
                    print('Renaming column!')
                    
                    up_current_col_names = [str(item).strip().upper() for item \
                                            in current_column_names]
                    
                    if (up_col_names != up_current_col_names):
                        print('WARNING: different column names!!!')
                    
                    column_mapping = dict([(current_column_names[i],column_names[i]) \
                                            for i in range(len(column_names))])
                    recent_dataframe = recent_dataframe.rename(columns = column_mapping)

                
            
                recent_data = recent_data.append(recent_dataframe)
                


            
            del fh, myzip, list_in_zip, txtfile, recent_dataframe
            
    ftp.quit()
    
    recent_data=rename_columns(recent_data)
    recent_data=recent_data.sort(['Station ID', 'Date'])
    recent_data = recent_data.replace(to_replace = -999, value = float('nan'))
    recent_data['Date'] = recent_data['Date'].astype(int).astype(str)
    recent_data['Year'] = [date[0:4] for date in recent_data['Date']]
    recent_data['Month'] = [date[4:6] for date in recent_data['Date']]
    recent_data['Day'] = [date[6:8] for date in recent_data['Date']]


    return recent_data
    
    