import os
import pandas as pd


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
    ID_to_citynames, citynames_to_ID = get_cities()
    df['City'] = [ID_to_citynames[str(ID).zfill(5)] for ID in df['Station ID']]

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
        raise OSError("There is no 'downloaded_data' directory.\n You either have to download\
            the weather data using 'download_weather_data' or move to the right\
            directory.' ")
            
    else:   
        if not os.path.isdir('downloaded_data/'+era):
            raise OSError('You dont have the '+era+' data, download it first.')
            
        else:
            if os.listdir(os.getcwd()+'/downloaded_data/'+era) == []:
                raise OSError('You dont have the '+era+' data, download it first.')




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
        raise ValueError('There is no station '+ID+' in the '+era+' data.')



def get_txtfilename(ID, era):
    """ Return the txtfilename given by station ID and era in correct format."""
    
    return era+'_'+ID+'.txt'



def load_station(ID,era):
    """
    Loads the data from one station for given era into a dataframe.
    
    INPUT
    -----
    ID   :  string with 5 digits of specifying station ID
    era  :  string specifying the path to return, either 'recent', 'historical'
    
    OUPUT
    -----
    df   :   dataframe containing all the data from that station  
    
    """
    
    check_for_weather_data(era)
    check_for_station(ID,era)
    
    txtfilename = get_txtfilename(ID,era)
    
    df = pd.read_csv('downloaded_data/'+era+'/'+txtfilename)
    df = df.drop(df.columns[0], axis = 1)
    
    return df
    
    

def get_timerange(df):

    """
    INPUT
    ------
    df: a single dataframe

    OUTPUT
    ------
    list with the first and last dates of the data frame [time_from, time_to]"""


    timerange = [df.iloc[0,1], df.iloc[-1,1]]
    return(timerange)



def merge_eras(df_hist, df_rec):
    """
    Merges historical with recent data and removes overlapping entries.
    
    INPUT
    ------
    df_hist:  Historical data, loaded into a pandas daraframe
    df_rec: Recent data, loaded into a pandas daraframe
    
    OUTPUT
    ------
    df_no_overlap: Retuns one timecontinuous datafrom, without duplicates.
    
    """
    df_merged = pd.concat([df_hist,df_rec], axis=0)
    df_no_overlap = pd.DataFrame.drop_duplicates(df_merged)
    return df_no_overlap
    
    

def extract_times(df,  time_from, time_to):
    
    df_to = df[df['Date'] <= str(time_to)]
    df_from_to = df_to[df_to['Date'] >= str(time_from)]
    
    return df_from_to
    
def get_cities(filename = 'downloaded_data/DWD_City_List.txt'):
    """
    Reads cities and ids from textfile 
    
    INPUT
    -----
    filename: Filename of the txt-File, where all cities and station IDs are
              inside
    
    OUTPUT
    ------
    ID_to_citynames:  Dictionary that maps station IDs to citynames
    
    citynames_to_ID: Dictionary that maps citynames to station IDs
    """
    
    # Attention! The textfile given by the DWD is encoded in Latin-1.
    # Python3 uses utf-8 by default, so we have to specify it here.
    # In Python2 none of this will work, the open() function doesn't
    # even accept encode= as a parameter.
    with open(filename, 'rt', encoding='Latin-1') as text_file:
        # Read the first two lines, which we don't need.        
        text_file.readline()
        text_file.readline()
        
        ID_to_citynames = {}
        citynames_to_ID = {}
        
        for line in text_file:
            try:
                ID = int(line[:11])
                city_name = line[67:108].strip()
                ID = str(ID).zfill(5)
                ID_to_citynames[ID] =  city_name
                citynames_to_ID[city_name] = ID
            except ValueError:
                pass
    
        return ID_to_citynames, citynames_to_ID





def load_dataframe(Cities_or_IDs, time_from, time_to):
    
    """
    Loops through the list of station IDs and loads the historical and recent
    data into dataframes.    
    
    
    
    INPUT
    -----
    IDs       :  list of station IDs (5 digit strings) or corresponding list of cities 
    time_from :  lower bound of the timespan to be returned string format 'yyyymmdd'
    time_to   :  upper bound of the timespan to be returned string format 'yyyymmdd'
    
    OUTPUT
    ------
    dictionary of time series
    
    """
    if not isinstance( Cities_or_IDs, list):
        Cities_or_IDs = [Cities_or_IDs]
        
    
    ID_to_citynames, citynames_to_ID = get_cities()
    #print(citynames_to_ID)
    IDs=[]
    
    for string in Cities_or_IDs:
    #Getting the mapping dictionaries
        #print(string)
        
        #If Cities_or_IDs is the ID 
        if string.isdigit():
            IDs.append(string)
            
        
        #If Cities_or_IDs is the the city name, mapping to the ID
        elif string.isalpha():
            ID = citynames_to_ID[string]
            IDs.append(ID)
            
        else:
            raise TypeError('You did not enter a correct ID or City. Call the function get_cities() \
            to see the mapping dictionaries')
    

    

    dict_of_stations = {}
    
    for ID in IDs:
        
        current_df_rec = load_station(ID, 'recent')
        current_df_hist = load_station(ID, 'historical')
        
        current_df_rec = clean_dataframe(current_df_rec)
        current_df_hist = clean_dataframe(current_df_hist)
        
        timerange_rec =  get_timerange(current_df_rec)
        timerange_hist = get_timerange(current_df_hist)
        
        
        if str(time_from) < timerange_hist[0] or str(time_to) > timerange_rec[1]:
            raise ValueError('Dates are either too far in the past or the future, '
            'the valid timerange is from %s to %s' %(timerange_hist[0],timerange_rec[1]))
            
        if str(time_from) > str(time_to):
            raise ValueError('The time_from (%s) is later than the time_to (%s)!'\
                                %(str(time_from), str(time_to)))

        current_df = merge_eras(current_df_hist, current_df_rec)
        current_df = extract_times(current_df, time_from, time_to)

        #indices = pd.Timestamp(current_df.loc[''])
        #date_form =  current_df.index.values.astype(str)

        current_df['Date'] = pd.to_datetime(current_df['Date'])
        current_df = current_df.set_index('Date')

        dict_of_stations[ID] = current_df
    return dict_of_stations
'''
if __name__ == '__main__':
    df = load_dataframe(['02712','00003'], '20140101', '20150101')
'''