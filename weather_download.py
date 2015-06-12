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
import getopt
import sys


class OverwriteException(Exception):
    pass

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
        raise ValueError('Input string not recognized')
        
        

def zipfilestring_to_stationID(fullzipstring, era):
    
    """
    Returns the station ID for the full string from the ftp-server.
    
    INPUT
    ------
    fullzipstring : string - a correct input should look like 
                        "<ftp_path>/<string_containing_id>.zip"
    era: string specifying the path to return, either 'recent' 
            or 'historical'
    OUTPUT
    ------
    station_ID : Station ID of type string as 5 digit number
    
    """    
    
    ftp_path =  get_ftp_path(era)
    
    if fullzipstring.startswith(ftp_path) and fullzipstring.endswith('.zip'):      
        zipstring = fullzipstring[len(ftp_path):]
        filestring = zipstring[:-4]      
    else:       
        raise ValueError('This is not the correct full zipstring!')
        
    
    if era == 'historical':        
        stationID = filestring.split('_')[1]       
    elif era == 'recent':        
        stationID = filestring.split('_')[2]        
    else:        
        raise ValueError('Requested era is not valid! It has to be historical or\
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
        raise ValueError('Input string does not start with recent or historical\
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
    
    
def set_city_files(download_path):
    
    """
    Download file with the city names and station IDs from the FTP server and 
    save it in the folder downloaded_data.
    
    INPUT
    ------
    download_path: folder path you where you want to save the data.	
    
    OUTPUT
    ------
    no output.
    
    """
    #Loading the city names' file
    fname = os.path.join('downloaded_data','DWD_City_List.txt')
    
    masterpath = download_path
    path_before = os.getcwd()
    os.chdir(masterpath)


    if not os.path.isfile(fname):
        #In case the file doesn't exist
        print('Downloading')
        file_name = 'KL_Tageswerte_Beschreibung_Stationen.txt'
        ftp = FTP('ftp-cdc.dwd.de')
        ftp.login()
        ftp.cwd("/pub/CDC/observations_germany/climate/daily/kl/historical/")
        ftp.retrbinary("RETR " + file_name ,open(fname, 'wb').write)
    
    os.chdir(path_before)



def set_up_directories(download_path, force, era='all'):
    
    """
    Delete old directories in the selected folder of the specified era(s) and 
    create new empty directories.
    
    INPUT
    ------
    download_path: folder path you where you want to save the data.
    
    force: boolean variable. True if overwriting is expected

    era: string specifying the path to return, either 'recent', 'historical' or
            'all'
    OUTPUT
    ------
    no output.
    
    """
    string_1 ='downloaded_data'
    string_1a = 'historical'
    string_1b = 'recent'
    masterpath = download_path
    path_before = os.getcwd()
    os.chdir(masterpath)
    
    if era == 'all':
        if not force:
            #Check if directory exists and raise error if so
            if os.path.isdir(string_1):
                raise OverwriteException("\n \n Some data was found in the system.\n If you would like to overwrite everything, add --force. Otherwise, specify era: 'historical' or 'recent'.")

        else:
            #Check if directory exists and dleete directory if so
            if os.path.isdir(string_1):
                import shutil
                shutil.rmtree(string_1)
            #Create directories
            os.chdir(string_1)
            os.mkdir(string_1a)
            os.mkdir(string_1b)
            os.chdir(masterpath)
            
    elif era == 'historical':
        if not force:
            #Check if directory exists and raise error if so
            if os.path.isdir(os.path.join(string_1,string_1a)):
                raise OverwriteException("\n \n Some historical data was found in the folder. \n If you would like to overwrite it, specify --force.")

        else:
            if os.path.isdir(os.path.join(string_1,string_1a)):
                import shutil
                shutil.rmtree(os.path.join(string_1,string_1a))
            #Create directories
            if not os.path.isdir(os.path.join(string_1)): 
                os.mkdir(string_1)
                
            os.chdir(string_1)
            os.mkdir(string_1a)
            os.chdir(masterpath)
                
    elif era == 'recent':
        if not force:
            #Check if directory exists and raise error if so
            if os.path.isdir(os.path.join(string_1,string_1a)):
                raise OverwriteException("\n \n Some recent data was found in the folder. \n If you would like to overwrite it, specify --force.")
        else:
            if os.path.isdir(os.path.join(string_1,string_1b)):
                import shutil
                shutil.rmtree(os.path.join(string_1,string_1b))
            #Create directories
            if not os.path.isdir(os.path.join(string_1)): 
                os.mkdir(string_1)
                
            os.chdir(string_1)
            os.mkdir(string_1b)
            os.chdir(masterpath)
            
    os.chdir(path_before)
        
        
            
def download_data_as_txt_file(zipfilename, download_path):
    
    """
    Downloading the Text-file containg all the relevant weather data from
    one zip file.
    
    INPUT   
    -----    
    zipfilename : Name of the zip-file the text-file is contained as a string
    
    download_path: folder path you where you want to save the data.
    
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

    masterpath = download_path
    
    os.chdir(os.path.join(masterpath,'downloaded_data',get_era_from_zipstring(zipfilename)))
    
    txtfile = myzip.open(txtfilename, "r")  
    
    data=pd.read_csv(txtfile, sep=';')    

    data.to_csv(savename +'.txt')

    txtfile.close()    
    os.chdir(masterpath)
            
            

def download_weather_data(download_path,era = 'all', force = False, verbose = False):
    
    """
    Downloads all the data for specified era to local directory by creating
    new directory weather_downloads.
    
    INPUT
    ------
    download_path: folder path you where you want to save the data.
    
    era: string specifying the path to return, either 'recent', 'historical' or
            'all', default is 'all'
    
    force: boolean variable. True if overwriting is expected.
    
    OUTPUT
    ------
    not output
    """    
    
    if not os.path.isdir(download_path):
        raise OSError('Download path is not valid!')
    
    set_up_directories(download_path, force, era = era)
    set_city_files(download_path)
        
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
                
                download_data_as_txt_file(zipfilename, download_path)
                
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
                
                download_data_as_txt_file(zipfilename, download_path)
                
            if verbose:
                total_time = time()-starttime
                print('The download for the '+era+' data took %5.1f s'%total_time)

    else:
        raise ValueError("Era has to be either 'recent' or 'historical' or 'all'!")


def print_readme():
    """Print README.txt"""
    
    readme_file = 'README.txt'
    
    #os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
    #                                           '..', 'README.txt'))
    with open(readme_file, 'r') as fp:
            print(fp.read())



if __name__ in '__main__':
    
    """The CLI, argv is sys.argv"""
    path = os.getcwd()
    era = 'all'
    verbose = False
    force = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['era=', 'folder=', \
                                                        'verbosity','force','help'])
    except getopt.GetoptError:
        print('Naaaaa.. i dont think so')
        print('print readme ...')
        print(('Because you obviously did not read README.txt, '
              'I will print it for you.'))
        print()
        print('------------README.txt------------')
        print_readme()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--verbosity':
            verbose = True
        elif opt == '--force':
            force = True
        elif opt == '--era':
            era = arg
        elif opt == '--folder':
            path = arg
        elif opt == '-h' or opt == '--help':
            print('------------README.txt------------')
            print_readme()
            sys.exit()
    
    if verbose:
        print('Downloading '+era+' data to '+path)
    
    download_weather_data(path, era = era, verbose = verbose, force = force)


