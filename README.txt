In your command window you have to go to the folder which contains weather_download.py (Python 3 needs to be installed for that). The syntax to download data from the DWD:

python weather_download.py --era=my_era --folder=my_folder


Arguments for the options (only single arguments possible)

--era:           Specify the era from which you want to download the data  
		 	excepts: 'historical','recent' or 'all' 
			default: 'all' (both recent and historical)

--folder:        Specify the folder you where you want to save the data						
			excepts: String of the whole path of the directory
			default: Current working directory


Options that don't have arguments:

--verbosity:       Call --verbosity to get verbose = True (get updated on the downloading process)

--help:		   Print README.txt

If you want to download for example the historical data into the folder with the directory (\Users\my_name\Desktop) and verbosity to be True call:

python weather_download.py --era='historical' --folder='\Users\my_name\Desktop' --verbosity
