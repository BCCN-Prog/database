### TODO: cashing?

from ftplib import FTP
import zipfile
import io
import pandas as pd



def temporary_load_one_dataset():

    fh =  io.BytesIO()
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


    
    


def get_historical_data():
    
    '''
    DOCUMENTATION
    '''

  
    df_empty = True
    path_hist_data = '/pub/CDC/observations_germany/climate/daily/kl/historical/'
     
    ftp = FTP('ftp-cdc.dwd.de')
    ftp.login()
    listfiles = ftp.nlst(path_hist_data)  


    counter = 0    
    N = len(listfiles)    


    for zipstring in listfiles[:500]:

        
        if zipstring.endswith('.zip'):


            counter+=1
            print('working on station number', counter, '/',N,'...')
    
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
            
            current_dataframe=pd.read_csv(txtfile, sep=';')    
            current_dataframe=current_dataframe.drop('eor',1)        
            current_dataframe=current_dataframe.dropna(axis = 0)
            current_dataframe.iloc[:,0] = int(current_dataframe.iloc[0,0])
            
            if df_empty:
                historical_data = current_dataframe
                
                column_names = current_dataframe.columns
                up_col_names = [str(item).strip().upper() for item in column_names]
                
                df_empty = False
            else:
 
                current_column_names = current_dataframe.columns
                
                if (current_column_names != column_names).any() :
                    
                    print('Renaming column!')
                    
                    up_current_col_names = [str(item).strip().upper() for item \
                                            in current_column_names]
                    
                    if (up_col_names != up_current_col_names):
                        print('WARNING: different column names!!!')
                    
                    column_mapping = dict([(current_column_names[i],column_names[i]) \
                                            for i in range(len(column_names))])
                    current_dataframe = current_dataframe.rename(columns = column_mapping)
                    
                
                historical_data = historical_data.append(current_dataframe)
                
                
            del fh, myzip, list_in_zip, txtfile

    ftp.quit()
    
    historical_data = rename_columns(historical_data)
    historical_data = historical_data.sort(['Station ID', 'Date'])
    historical_data = historical_data.replace(to_replace = -999, value = float('nan'))
    historical_data['Date'] = historical_data['Date'].astype(int).astype(str)
    historical_data['Year'] = [date[0:4] for date in historical_data['Date']]
    historical_data['Month'] = [date[4:6] for date in historical_data['Date']]
    historical_data['Day'] = [date[6:8] for date in historical_data['Date']]


    return historical_data
    
    



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
                                              column_names[16]: 'Snow Depth',
    })
    return data_eng


if __name__ in '__main__':

    hist_dat = get_historical_data()
