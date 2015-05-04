import pandas as pd
import numpy as np

def load_data(path):
    '''
    (str) -> (pandas.DataFrame)
    Loads the database and cleans the whitespace in STATIONS_ID.
    
    IMPORTANT: This function assumes you have the database stored in a text file in the directory.
    '''
    data = pd.read_csv(path, index_col = 2)
    data["STATIONS_ID"] = data["STATIONS_ID"].str.replace(' ', '')
    data["STATIONS_ID"] = data["STATIONS_ID"].convert_objects(convert_numeric=True)
    return data


def get_data(data, station_id, category = 3):
    """
    (pandas.Dataframe, int, list) -> (pandas.DataFrame)
    Returns desired information from the database about requested city and categories. Index is based on and sorted by date.
    
    station_id: The code for the requested city/station
    
    category: Can be an int or a list of desired variable(s). By default gets the air temperature.
    
        The codes for variables:
        0: Numerical Index
        1: STATIONS_ID
        2: QUALITAETS_NIVEAU
        3: Air Temperature / LUFTTEMPERATUR
        4: DAMPFDRUCK
        5: BEDECKUNGSGRAD
        6: LUFTDRUCK_STATIONSHOEHE
        7: REL_FEUCHTE
        8: WINDGESCHWINDIGKEIT
        9: Max Air Temperature
        10: Min Air Temperature
        11: LUFTTEMP_AM_ERDB_MINIMUM (?)
        12: Max Wind Speed / WINDSPITZE_MAXIMUM
        13: Precipitation Height / NIEDERSCHLAGSHOEHE (?)
        14: NIEDERSCHLAGSHOEHE_IND (?)
        15: Sunshine Duration
        16: Snow Height
    """
    rlv_station = data[data.iloc[:, 1] == station_id]
    selected = rlv_station.iloc[:, category]
    return selected
