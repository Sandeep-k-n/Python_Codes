
import pandas as pd
import datetime 
import dateutil
import nltk
nltk.download('punkt')

#Data Dump
Data_Dump = "1 12:00:05 0 0 0 1 12:00:10 0 0 0 1 12:00:15 0 0 0 1 12:00:20 0 0 0 1 12:00:25 0 0 0 1 12:00:30 0 0 5 1 12:00:35 2 5 6 1 12:00:40 2 0 7 1 12:00:45 2 7 10 1 12:00:50 2 10 9 1 12:00:55 2 9 8 1 12:01:00 3 8 12 1 12:01:05 3 12 20 1 12:01:10 3 20 30 1 12:01:15 3 30 25 1 12:01:20 4 25 35 1 12:01:25 4 35 10 1 12:01:30 4 10 0 1 12:01:35 0 0 0 1 12:01:40 0 0 0 1 12:01:45 0 0 0 1 12:01:50 0 0 2 2 4:00:15 2 2 3 2 4:00:20 2 3 4 2 4:00:25 2 4 5 2 4:00:30 2 5 6 2 4:00:35 4"

# Convert the data to list
lst = nltk.word_tokenize(Data_Dump)
 
# using list comprehension
n = 5
List = [lst[i:i + n] for i in range(0, len(lst), n)]

#Convert list to Dataframe
Raw_Data = pd.DataFrame(List, columns =["Vehicle_Number","Timestamp","Mode","Speed","Unkown"])
Raw_Data = Raw_Data.fillna(0)

Columns = ["VIN","Mode/Gear","gear_start","gear_end","time_taken","avg speed","max speed", "avg_speed_with_out_zero "]

Raw_Data['Speed'] = Raw_Data['Speed'].astype('int')
# Raw_Data['Time'] = pd.to_datetime(Raw_Data['Timestamp'], format='%H:%M:%S').dt.time
Raw_Data['Time'] = pd.to_datetime(Raw_Data['Timestamp'], format='%H:%M:%S')
NonZero_Data =  Raw_Data[Raw_Data.Speed != 0]

x1 = Raw_Data.groupby(['Mode','Vehicle_Number']).agg({"Time" : ["min","max"] , "Speed": ["mean", "max"]})

x2 = NonZero_Data .groupby(['Mode','Vehicle_Number']).agg({"Speed": "mean"})
Result_Data = pd.merge(x1, x2, on=['Vehicle_Number', 'Mode'], how='left')
Result_Data.reset_index(level=1, inplace=True)
Result_Data.reset_index(level=0, inplace=True)
Result_Data.columns = ["VIN","Mode/Gear","gear_start","gear_end","avg speed","max speed", "avg_speed_with_out_zero "]

Result_Data['time_taken'] = Result_Data['gear_end'] - Result_Data['gear_start']
Result_Data['gear_start'] = Result_Data['gear_start'].dt.strftime("%H:%M:%S")
Result_Data['gear_end'] = Result_Data['gear_end'].dt.strftime("%H:%M:%S")

Result_Data['time_taken'] = Result_Data['time_taken'].dt.total_seconds()

Result = Result_Data.loc[:,Columns]

import pandas
!wget https://raw.githubusercontent.com/MicrosoftDocs/mslearn-introduction-to-machine-learning/main/graphing.py
!wget https://raw.githubusercontent.com/MicrosoftDocs/mslearn-introduction-to-machine-learning/main/m0b_optimizer.py
!wget https://raw.githubusercontent.com/MicrosoftDocs/mslearn-introduction-to-machine-learning/main/Data/seattleWeather_1948-2017.csv

# Load a file that contains weather data for Seattle
data = pandas.read_csv('seattleWeather_1948-2017.csv', parse_dates=['date'])

# Keep only January temperatures
data = data[[d.month == 1 for d in data.date]].copy()


# Print the first and last few rows
# Remember that with Jupyter notebooks, the last line of 
# code is automatically printed
data
