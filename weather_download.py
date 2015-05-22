#!/usr/bin/env python3

"""
Documentation
"""
from ftplib import FTP
import zipfile
import io
import pandas as pd
import os
from time import time 


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
        stationID = filestring.split('_')[1]       
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
    zipfile_names = [fname for fname in zipfile_names if fname.endswith('.zip')]
    
    return zipfile_names
    
    
    

def set_up_directories(era='all'):
    
    """
    Delete old directories in the selected folder of the specified era(s) and 
    create new empty directories.
    
    INPUT
    ------
    era: string specifying the path to return, either 'recent', 'historical' or
            'all'
    OUTPUT
    ------
    no output.
    
    """
    string_1 ='downloaded_data'
    string_1a = 'historical'
    string_1b = 'recent'
    masterpath = os.getcwd()
    
    if era == 'all':
        #Check if directory exists and delete it if so
        if os.path.isdir('downloaded_data'):
            import shutil
            shutil.rmtree('downloaded_data')
        #Create directories
        os.mkdir(string_1)
        os.chdir(string_1)
        os.mkdir(string_1a)
        os.mkdir(string_1b)
        os.chdir(masterpath)
        
    elif era == 'historical':
        #Check if directory exists and delete it if so
        if os.path.isdir('downloaded_data/'+era):
            import shutil
            shutil.rmtree('downloaded_data/'+era)
        #Create directories
        if os.path.isdir('downloaded_data/'):
            os.chdir(string_1)
            os.mkdir(string_1a)
            os.chdir(masterpath)
        else:
            os.mkdir(string_1)
            os.chdir(string_1)
            os.mkdir(string_1a)
            os.chdir(masterpath)

    elif era == 'recent':
        #Check if directory exists and delete it if so
        if os.path.isdir('downloaded_data/'+era):
            import shutil
            shutil.rmtree('downloaded_data/'+era)
        #Create directories
        if os.path.isdir('downloaded_data/'):
            os.chdir(string_1)
            os.mkdir(string_1b)
            os.chdir(masterpath)
        else:
            os.mkdir(string_1)
            os.chdir(string_1)
            os.mkdir(string_1b)
            os.chdir(masterpath)
        
        
            
def download_data_as_txt_file(zipfilename):
    
    """
    Downloading the Text-file containg all the relevant weather data from
    one zip file.
    
    INPUT   
    -----    
    zipfilename : Name of the zip-file the text-file is contained as a string
    
    OUTPUT
    ------
    No output
    
    """
    ftp = FTP('ftp-cdc.dwd.de')
    ftp.login()
    
    fh = io.BytesIO()
    ftp.retrbinary('RETR %s' % zipfilename, fh.write)
    fh.seek(0) # rewind pseudo-file
    myzip = zipfile.ZipFile(fh)

    list_in_zip = myzip.namelist() # list names 
    
    txtfilename = ''
    for name in list_in_zip:
        # the txt-file we need starts with 'produkt_klima_...'
        if name.startswith('produkt_klima_Tageswerte'):
            txtfilename = name
            break   
            
    savename = get_txtfile_savename(zipfilename)

    masterpath = os.getcwd()
    os.chdir('downloaded_data/% s' % get_era_from_zipstring(zipfilename))
    
    txtfile = myzip.open(txtfilename, "r")  
    
    data=pd.read_csv(txtfile, sep=';')    

    data.to_csv(savename +'.txt')

    txtfile.close()    
    os.chdir(masterpath)
            
            

def download_weather_data(era = 'all', verbose = False):
    
    """
    Downloads all the data for specified era to local directory by creating
    new directory weather_downloads.
    
    INPUT
    ------
    era: string specifying the path to return, either 'recent', 'historical' or
            'all', default is 'all'
    
    OUTPUT
    ------
    not output
    """    
    
    
    
    set_up_directories(era)

    if era == 'all':
        
        for e in ['recent', 'historical']:
            
            if verbose:
                print('downloading '+e+' data..')
                starttime = time()
            
            ftp_path = get_ftp_path(e)
            
            listfiles = get_all_zipfile_names(ftp_path)
            
            count = 0                 
            for zipfilename in listfiles:
                
                if verbose:
                    print(count+1,'/',len(listfiles))
                    count +=1
                
                download_data_as_txt_file(zipfilename)
                
            if verbose:
                total_time = time()-starttime
                print('The download for the '+e+' data took %5.1f s'%total_time)
                
                   
    elif era == 'historical' or era == 'recent':
        
            if verbose:
                print('downloading '+era+' data..')
                starttime = time()

            ftp_path = get_ftp_path(era)
            
            listfiles = get_all_zipfile_names(ftp_path)
            
            count = 0
            for zipfilename in listfiles:
                
                if verbose:
                    print(count+1,'/',len(listfiles))
                    count +=1
                
                download_data_as_txt_file(zipfilename)
                
            if verbose:
                total_time = time()-starttime
                print('The download for the '+era+' data took %5.1f s'%total_time)

    else:
        raise NameError("Era has to be either 'recent' or 'historical' or 'all'!")





def rename_columns(data_ger):
    
    column_names = data_ger.columns.values
    data_eng = data_ger.rename(columns = {column_names[0]: 'Station ID',
                                          column_names[1]: 'Date',
                                          column_names[2]: 'Quality Level',
                                          column_names[3]: 'Air Temperature',
                                          column_names[4]: 'Vapor Pressure',
                                          column_names[5]: 'Degree of Coverage',
                                          column_names[6]: 'Air Pressure',
                                          column_names[7]: 'Rel Humidity',
                                          column_names[8]: 'Wind Speed',
                                          column_names[9]: 'Max Air Temp',
                                          column_names[10]: 'Min Air Temp',
                                          column_names[11]: 'Min Groundlvl Temp',
                                          column_names[12]: 'Max Wind Speed',
                                          column_names[13]: 'Precipitation',
                                          column_names[14]: 'Precipitation Ind',
                                          column_names[15]: 'Hrs of Sun',                                          
                                          column_names[16]: 'Snow Depth', })
                                          
    return data_eng





def clean_dataframe(df):
    """
    Cleans the raw weather data (i.e. dropping the eor column, dropping the na 
    row, making the 'Station ID' type int, replace -999 values by nan, 
    sorting the dataframe by 'Station ID' and 'Date', making the 'Date' type
    string, adding a 'Year', 'Month' and 'Day' column) in the dataframe and 
    renames the German column to their English equivalent.
    
    INPUT   
    -----    
    df : Raw dataframe
    
    OUTPUT
    ------
    df : Clean dataframe
    
    """
    
    if 'eor' in df:
        df=df.drop('eor', 1)   
    
    df=df.dropna(axis = 0)
    df.iloc[:,0] = int(df.iloc[0,0])    
         
    df=rename_columns(df)
    df=df.sort(['Station ID', 'Date'])
    df=df.replace(to_replace = -999, value = float('nan'))
    df['Date']=df['Date'].astype(int).astype(str)
    df['Year']=[date[0:4] for date in df['Date']]
    df['Month']=[date[4:6] for date in df['Date']]
    df['Day']=[date[6:8] for date in df['Date']]

    return df
    
    



def check_for_weather_data(era):
    
    """
    Check if there is data in the 'era' directory below directories 'downloaded_weather'.
    
    INPUT
    ------
    era: string specifying the path to return, either 'recent', 'historical'
    
    OUTPUT
    ------
    not output  
    """

    if not os.path.isdir('downloaded_data'):
        raise NameError("There is no 'downloaded_data' directory.\n You either have to download\
            the weather data using 'download_weather_data' or move to the right\
            directory.' ")
            
    else:   
        if not os.path.isdir('downloaded_data/'+era):
            raise NameError("You don't have the ",era," data, download it first.")
            
        else:
            if os.listdir(os.getcwd()+'/downloaded_data/'+era) == []:
                raise NameError("You don't have the ",era," data, download it first.")




def check_for_station(ID, era):
    
    """
    Check if there is a station specified by ID for given era.
    
    INPUT
    -----
    ID   :  string with 5 digits of specifying station ID
    era  : string specifying the path to return, either 'recent', 'historical'
    
    OUPUT
    -----
    no output
    """

    txtfilename = get_txtfilename(ID,era)
    
    if txtfilename not in os.listdir(os.getcwd()+'/downloaded_data/'+era):
        raise NameError("There is no station ",ID," in the ",era," data.")



def get_txtfilename(ID, era):
    """ Return the txtfilename given by station ID and era in correct format."""
    
    return era+'_'+ID+'.txt'





#if __name__ in '__main__':    