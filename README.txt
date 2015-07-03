1. DOWNLOADING THE WEATHER FILE

In your command window you have to go to the folder which contains weather_download.py (Python 3 needs to be installed for that). The syntax to download data from the DWD on the command line:

python weather_download.py --era=my_era --folder=my_folder


Arguments for the options (only single arguments possible):

--era:           Specify the era from which you want to download the data  
		 	excepts: 'historical','recent' or 'all' 
			default: 'all' (both recent and historical)

--folder:        Specify the folder you where you want to save the data						
			excepts: String of the whole path of the directory
			default: Current working directory


Options that don't have arguments:

--force:	   Call --force if you want to overwrite existing data of specified era(s). Otherwise, if there is already data in the 			   specified folder, an expeception will be raised.

--verbosity:       Call --verbosity to get updated on the downloading process

--help:		   Print README.txt


Example:

If you want to download the historical data into the folder with the directory (\Users\my_name\Desktop) and verbosity to be True call:

python weather_download.py --era='historical' --folder='\Users\my_name\Desktop' --verbosity






2.GETTING STATISTICS AND PLOTS

In your command window you have to go to the folder which contains plotting2.py (Python 3 is required). Example usage of the file is the following:

python plotting.py --id Berlin --startyear 1990 --endyear 2014 --measure 12
python plotting.py --help

Parameters:

--id_stat (str): Enter the name or ID of the station(s) whose data you would like to receive.

--startyear (int): Enter year that you want to begin your query.

--endyear (int): Enter year that you want to begin your query.

--measure (int): Enter the code of measure(s) you want to obtain.
	The codes for variables:
	0: Station ID
	1: Quality Level
	2: Air Temperature
	3: Vapor Pressure
	4: Degree of Coverage
	5: Air Pressure
	6: Relative Humidity
	7: Wind Speed
	8: Max Air Temperature
	9: Min Air Temperature
	10: Min Groundlvl Temp
	11: Max Wind Speed
	12: Precipitation Height
	13: Precipitation Ind
	14: Sunshine Duration
	15: Snow Height

--resolution (str): Enter the time measure that you want; 'dayofyear', 'dayofweek', 'month' or 'year'.

--function (str): Enter the function you want to use ('min' or 'max').

--average (bool) Enter if you want the average of the given data.

--plotting (bool) Enter 'True' if you want to plot results.

--weekend_comparison (bool) Enter 'True' if you want to compare between weekdays and weekend.
