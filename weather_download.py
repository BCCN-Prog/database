#!/usr/bin/env python3

"""
Documentation
"""
from ftplib import FTP
import zipfile
import io
import pandas as pd
from FTPData import rename_columns


def get_ftp_path(era):
    
    """
    Returns the path to the ftp server for given timeperiod.    
    
    INPUT
    -----
    era: string specifying the path to return, either 'recent' or 'historical'
    
    OUTPUT
    -----
    path: string specifying the webpath to the desired online data
    """
    
    if era == 'historical':
        return '/pub/CDC/observations_germany/climate/daily/kl/historical/'
    elif era == 'recent':
        return '/pub/CDC/observations_germany/climate/daily/kl/recent/'
    else:
        raise NameError('Input string not recognized')
        
        

def zipfilestring_to_stationID(fullzipstring, era):
    
    """
    Returns the station ID for the full string from the ftp-server.
    
    INPUT
    ------
    fullzipstring : string - a correct input should look like 
                        "<ftp_path>/<string_containing_id>.zip"
    
    OUTPUT
    ------
    station_ID : Station ID of type string as 5 digit number
    
    """    
    
    ftp_path =  get_ftp_path(era)
    
    if fullzipstring.startswith(ftp_path) and fullzipstring.endswith('.zip'):      
        zipstring = fullzipstring[len(ftp_path):]
        filestring = zipstring[:-4]      
    else:       
        raise NameError('This is not the correct full zipstring!')
        
    
    if era == 'historical':        
        stationID = int(filestring.split('_')[1])        
    elif era == 'recent':        
        stationID = filestring.split('_')[2]        
    else:        
        raise NameError('Requested era is not valid! It has to be historical or\
                                                                    recent.')
    
    return stationID

    
def get_era_from_zipstring(fullzipstring):

    """
    Extracts the era from a given zipstring.

    INPUT
    ------
    fullzipstring:   string of type '<ftp_path>/<string_containing_id>.zip'
    
    OUTPUT
    ------
    era:     string with either 'historical' or 'recent'
         
    """
    
    if fullzipstring.startswith(get_ftp_path('historical')):      
        return 'historical'
    elif  fullzipstring.startswith(get_ftp_path('recent')):        
        return 'recent'        
    else:
        raise NameError('Input string does not start with recent or historical\
                            ftp-path!')




def get_txtfile_savename(fullzipstring):
    
    """
    Returns the string needed to save data given by fullzipstring as .txt.
    
    INPUT
    ------
    fullzipstring:  string of type '<ftp_path>/<string_containing_id>.zip'

    OUTPUT
    ------
    txtsavename:  the name of the txt file that will contain the data

    """    
    
    era = get_era_from_zipstring(fullzipstring)
                            
    stationID = zipfilestring_to_stationID(fullzipstring, era)
    
    txtsavename = era+'_'+stationID
    
    return txtsavename
    
    
    
def get_all_zipfile_names(path):    
    
    """
    Return the list of zipfiles for given ftp-path.
    
    INPUT
    ------
    path : String specifying the webpath to the desired online data
    
    OUTPUT
    ------
    zipfile_names : list of strings with all the zipfile names 
                    with the station number and full ftp-path
    """
    
    ftp = FTP('ftp-cdc.dwd.de')
    ftp.login()
    zipfile_names = ftp.nlst(path)  
    
    return zipfile_names
    
    

#if __name__ in '__main__':    