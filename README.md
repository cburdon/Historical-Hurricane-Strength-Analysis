
# Hurricane Season Analysis

## Data Gathering

### Pseudocode
1.  import dependencies
2.  get csv file
3.  read csv file into pandas
4.  display
5.  cleanup/delete unnecessary columns


```python
import pandas as pd
from datetime import datetime, timedelta
import csv
import matplotlib.pyplot as plt
import numpy as np
file = "hurricane_data.csv"
```


```python
# Add headerrow containing storm id and storm name to data rows and create list
hurricane_data = []

storm_id = "0000000"
storm_name = "UNNAMED"
with open(file) as hurricane_file:
    hurricane_reader = csv.reader(hurricane_file)
    next(hurricane_reader, None) 
    for row in hurricane_reader:
                if 'AL' in row[0]: 
                    storm_id = row[0].strip()
                    storm_name = row[1].strip()
#                     print(f'{storm_id}: {storm_name}')
                else:
                    oldformat = row[0]+row[1]
                    datetimeobject = datetime.strptime(oldformat,'%Y%m%d %H%M%S')
                    date = datetimeobject.strftime('%m-%d-%Y %H%M%S')
                    year = row[0][:4]
                    landfall = row[2].strip()
                    status = row[3].strip()
                    latitude = row[4].strip()
                    longitude = row[5].strip()
                    wind = row[6].strip()
                    pressure = row[7].strip()
                hurricane_data.append(
                    {
                        "Storm_Id": storm_id, 
                        "Name": storm_name,
                        "Date": date,
                        "Year": year,
                        "Landfall": landfall,
                        "Status" : status,
                        "Latitude" : latitude,
                        "Longitude" : longitude,
                        "Windspeed" : wind,
                        "Pressure" : pressure
                    }
                ) 
```


```python
# Create Dataframe and reorder columns
hurricane_pd = pd.DataFrame(hurricane_data)
hurricane_pd = hurricane_pd.loc[:, ["Storm_Id", "Name", "Date", "Year", "Status", "Latitude",
                                    "Longitude", "Windspeed", "Pressure", "Landfall"]]
hurricane_pd.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Storm_Id</th>
      <th>Name</th>
      <th>Date</th>
      <th>Year</th>
      <th>Status</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Windspeed</th>
      <th>Pressure</th>
      <th>Landfall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0000000</td>
      <td>UNNAMED</td>
      <td>06-25-1851 000000</td>
      <td>1851</td>
      <td>HU</td>
      <td>28.0N</td>
      <td>94.8W</td>
      <td>80</td>
      <td>-999</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>0000000</td>
      <td>UNNAMED</td>
      <td>06-25-1851 060000</td>
      <td>1851</td>
      <td>HU</td>
      <td>28.0N</td>
      <td>95.4W</td>
      <td>80</td>
      <td>-999</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>0000000</td>
      <td>UNNAMED</td>
      <td>06-25-1851 120000</td>
      <td>1851</td>
      <td>HU</td>
      <td>28.0N</td>
      <td>96.0W</td>
      <td>80</td>
      <td>-999</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>0000000</td>
      <td>UNNAMED</td>
      <td>06-25-1851 180000</td>
      <td>1851</td>
      <td>HU</td>
      <td>28.1N</td>
      <td>96.5W</td>
      <td>80</td>
      <td>-999</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>0000000</td>
      <td>UNNAMED</td>
      <td>06-25-1851 210000</td>
      <td>1851</td>
      <td>HU</td>
      <td>28.2N</td>
      <td>96.8W</td>
      <td>80</td>
      <td>-999</td>
      <td>L</td>
    </tr>
  </tbody>
</table>
</div>



# Data Cleanup

### Pseudocode
1. Check column counts for missing data
2. Check/Change column types for type conversion
3. Limit data to only the past 35 years, only Hurricanes and Tropical Storms, and only named storms
4. Get min date (when storm became Tropical Storm) and Max Date (When storm is no longer a tropical storm)
5. Calculate the duration of storm
6. Find nearest city for storms tha reached landfall
7. Get max windspeed row and return all columns
8. Categorize storms according to Saffir-Simpson scale https://en.wikipedia.org/wiki/Maximum_sustained_wind 


```python
#Check column counts for missing data
hurricane_pd.count()
```




    Storm_Id     52150
    Name         52150
    Date         52150
    Year         52150
    Status       52150
    Latitude     52150
    Longitude    52150
    Windspeed    52150
    Pressure     52150
    Landfall     52150
    dtype: int64




```python
#Check column types for needed type conversions
hurricane_pd.dtypes
```




    Storm_Id     object
    Name         object
    Date         object
    Year         object
    Status       object
    Latitude     object
    Longitude    object
    Windspeed    object
    Pressure     object
    Landfall     object
    dtype: object




```python
#Change types for Windspeed and Pressure to numerice and Date to Datetime
hurricane_pd['Windspeed'] = pd.to_numeric(hurricane_pd['Windspeed'])
hurricane_pd['Windspeed'] = hurricane_pd['Windspeed'] *1.15078
hurricane_pd['Pressure'] = pd.to_numeric(hurricane_pd['Pressure'])
hurricane_pd['Date'] = pd.to_datetime(hurricane_pd['Date'])
```


```python
# Limit data to only the past 35 years, 
# Only Hurricanes and Tropical Storms, and 
# Only named storms

hurricane_df_clean = hurricane_pd.loc[hurricane_pd["Year"] >= "1982"]
hurricane_df_clean = hurricane_df_clean.loc[hurricane_df_clean['Status'].isin(['TS','HU'])]
hurricane_df_clean = hurricane_df_clean.loc[hurricane_df_clean['Name'] != "UNNAMED"]
hurricane_df_clean.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Storm_Id</th>
      <th>Name</th>
      <th>Date</th>
      <th>Year</th>
      <th>Status</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Windspeed</th>
      <th>Pressure</th>
      <th>Landfall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>35894</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>22.8N</td>
      <td>85.0W</td>
      <td>46.0312</td>
      <td>1001</td>
      <td></td>
    </tr>
    <tr>
      <th>35895</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>23.2N</td>
      <td>84.2W</td>
      <td>57.5390</td>
      <td>995</td>
      <td></td>
    </tr>
    <tr>
      <th>35896</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 18:00:00</td>
      <td>1982</td>
      <td>HU</td>
      <td>24.0N</td>
      <td>83.6W</td>
      <td>86.3085</td>
      <td>985</td>
      <td></td>
    </tr>
    <tr>
      <th>35897</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-04 00:00:00</td>
      <td>1982</td>
      <td>HU</td>
      <td>24.8N</td>
      <td>83.4W</td>
      <td>74.8007</td>
      <td>992</td>
      <td></td>
    </tr>
    <tr>
      <th>35898</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-04 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>24.9N</td>
      <td>84.1W</td>
      <td>63.2929</td>
      <td>998</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
# Get min date (when storm became Tropical Storm) and Max Date (When storm is no longer a tropical storm)
# Calculate the duration

storm_gb = hurricane_df_clean.groupby('Storm_Id')
storm_sgb = storm_gb['Date']
start_date = storm_sgb.min()
end_date = storm_sgb.max()
duration = end_date - start_date
```


```python
#Merge Start Date, End Date, and Duration to original dataframe. 
start_end_df = pd.DataFrame({"Start Date": start_date
                             ,"End Date": end_date
                             ,"Duration" : duration
                            }).reset_index()

merge_df = pd.merge(hurricane_df_clean, start_end_df, how="outer", on="Storm_Id")

merge_df.head(100)

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Storm_Id</th>
      <th>Name</th>
      <th>Date</th>
      <th>Year</th>
      <th>Status</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Windspeed</th>
      <th>Pressure</th>
      <th>Landfall</th>
      <th>Duration</th>
      <th>End Date</th>
      <th>Start Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>22.8N</td>
      <td>85.0W</td>
      <td>46.0312</td>
      <td>1001</td>
      <td></td>
      <td>1 days 12:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1982-06-03 06:00:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>23.2N</td>
      <td>84.2W</td>
      <td>57.5390</td>
      <td>995</td>
      <td></td>
      <td>1 days 12:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1982-06-03 06:00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 18:00:00</td>
      <td>1982</td>
      <td>HU</td>
      <td>24.0N</td>
      <td>83.6W</td>
      <td>86.3085</td>
      <td>985</td>
      <td></td>
      <td>1 days 12:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1982-06-03 06:00:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-04 00:00:00</td>
      <td>1982</td>
      <td>HU</td>
      <td>24.8N</td>
      <td>83.4W</td>
      <td>74.8007</td>
      <td>992</td>
      <td></td>
      <td>1 days 12:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1982-06-03 06:00:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-04 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>24.9N</td>
      <td>84.1W</td>
      <td>63.2929</td>
      <td>998</td>
      <td></td>
      <td>1 days 12:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1982-06-03 06:00:00</td>
    </tr>
    <tr>
      <th>5</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-04 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>24.9N</td>
      <td>84.8W</td>
      <td>51.7851</td>
      <td>1002</td>
      <td></td>
      <td>1 days 12:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1982-06-03 06:00:00</td>
    </tr>
    <tr>
      <th>6</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-04 18:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>25.0N</td>
      <td>84.2W</td>
      <td>46.0312</td>
      <td>1005</td>
      <td></td>
      <td>1 days 12:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1982-06-03 06:00:00</td>
    </tr>
    <tr>
      <th>7</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-28 18:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>13.9N</td>
      <td>22.7W</td>
      <td>40.2773</td>
      <td>1006</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>8</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-29 00:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>14.1N</td>
      <td>23.6W</td>
      <td>40.2773</td>
      <td>1005</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>9</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-29 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>14.5N</td>
      <td>24.9W</td>
      <td>46.0312</td>
      <td>1003</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>10</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-29 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>14.9N</td>
      <td>26.3W</td>
      <td>51.7851</td>
      <td>1002</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>11</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-29 18:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>15.3N</td>
      <td>27.7W</td>
      <td>51.7851</td>
      <td>1000</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>12</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-30 00:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>15.7N</td>
      <td>29.1W</td>
      <td>57.5390</td>
      <td>999</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>13</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-30 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>16.0N</td>
      <td>30.6W</td>
      <td>57.5390</td>
      <td>998</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>14</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-30 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>16.3N</td>
      <td>32.1W</td>
      <td>57.5390</td>
      <td>996</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>15</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-30 18:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>16.7N</td>
      <td>33.6W</td>
      <td>63.2929</td>
      <td>995</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>16</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-31 00:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>17.0N</td>
      <td>35.0W</td>
      <td>63.2929</td>
      <td>993</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>17</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-31 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>17.2N</td>
      <td>36.4W</td>
      <td>69.0468</td>
      <td>992</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>18</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-31 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>17.7N</td>
      <td>37.8W</td>
      <td>69.0468</td>
      <td>991</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>19</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-08-31 18:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>18.0N</td>
      <td>39.0W</td>
      <td>69.0468</td>
      <td>990</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>20</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-09-01 00:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>18.3N</td>
      <td>40.0W</td>
      <td>69.0468</td>
      <td>989</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>21</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-09-01 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>18.6N</td>
      <td>40.9W</td>
      <td>69.0468</td>
      <td>998</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>22</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-09-01 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>18.8N</td>
      <td>41.7W</td>
      <td>69.0468</td>
      <td>998</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>23</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-09-01 18:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>19.0N</td>
      <td>42.4W</td>
      <td>69.0468</td>
      <td>990</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>24</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-09-02 00:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>19.2N</td>
      <td>43.2W</td>
      <td>63.2929</td>
      <td>994</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>25</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-09-02 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>19.4N</td>
      <td>44.1W</td>
      <td>51.7851</td>
      <td>1000</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>26</th>
      <td>AL031982</td>
      <td>BERYL</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>19.7N</td>
      <td>45.1W</td>
      <td>40.2773</td>
      <td>1005</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1982-09-02 12:00:00</td>
      <td>1982-08-28 18:00:00</td>
    </tr>
    <tr>
      <th>27</th>
      <td>AL051982</td>
      <td>CHRIS</td>
      <td>1982-09-10 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>27.3N</td>
      <td>94.2W</td>
      <td>40.2773</td>
      <td>1005</td>
      <td></td>
      <td>1 days 06:00:00</td>
      <td>1982-09-11 18:00:00</td>
      <td>1982-09-10 12:00:00</td>
    </tr>
    <tr>
      <th>28</th>
      <td>AL051982</td>
      <td>CHRIS</td>
      <td>1982-09-10 18:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>27.9N</td>
      <td>94.1W</td>
      <td>51.7851</td>
      <td>1001</td>
      <td></td>
      <td>1 days 06:00:00</td>
      <td>1982-09-11 18:00:00</td>
      <td>1982-09-10 12:00:00</td>
    </tr>
    <tr>
      <th>29</th>
      <td>AL051982</td>
      <td>CHRIS</td>
      <td>1982-09-11 00:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>28.4N</td>
      <td>94.1W</td>
      <td>57.5390</td>
      <td>1000</td>
      <td></td>
      <td>1 days 06:00:00</td>
      <td>1982-09-11 18:00:00</td>
      <td>1982-09-10 12:00:00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>70</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-17 00:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>27.4N</td>
      <td>93.3W</td>
      <td>74.8007</td>
      <td>991</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>71</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-17 06:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>27.7N</td>
      <td>93.7W</td>
      <td>80.5546</td>
      <td>987</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>72</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-17 12:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>27.9N</td>
      <td>94.2W</td>
      <td>86.3085</td>
      <td>983</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>73</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-17 18:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>28.1N</td>
      <td>94.5W</td>
      <td>103.5702</td>
      <td>974</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>74</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-18 00:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>28.4N</td>
      <td>94.8W</td>
      <td>109.3241</td>
      <td>969</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>75</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-18 06:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>28.9N</td>
      <td>95.0W</td>
      <td>115.0780</td>
      <td>963</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>76</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-18 07:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>29.1N</td>
      <td>95.1W</td>
      <td>115.0780</td>
      <td>962</td>
      <td>L</td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>77</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-18 12:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>29.7N</td>
      <td>95.5W</td>
      <td>92.0624</td>
      <td>965</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>78</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-18 18:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>30.5N</td>
      <td>96.0W</td>
      <td>46.0312</td>
      <td>990</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>79</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>31.5N</td>
      <td>96.7W</td>
      <td>40.2773</td>
      <td>998</td>
      <td></td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
    </tr>
    <tr>
      <th>80</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-24 06:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>27.4N</td>
      <td>76.3W</td>
      <td>46.0312</td>
      <td>1010</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>81</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-24 12:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>28.1N</td>
      <td>76.8W</td>
      <td>57.5390</td>
      <td>1011</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>82</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-24 18:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>28.1N</td>
      <td>77.6W</td>
      <td>57.5390</td>
      <td>1011</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>83</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-25 00:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>28.1N</td>
      <td>78.9W</td>
      <td>51.7851</td>
      <td>1011</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>84</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-25 06:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>28.0N</td>
      <td>79.8W</td>
      <td>46.0312</td>
      <td>1012</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>85</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-27 12:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>25.8N</td>
      <td>91.6W</td>
      <td>40.2773</td>
      <td>1008</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>86</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-27 18:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>25.8N</td>
      <td>93.0W</td>
      <td>51.7851</td>
      <td>1002</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>87</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-28 00:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>25.7N</td>
      <td>94.5W</td>
      <td>69.0468</td>
      <td>999</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>88</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-28 06:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>25.5N</td>
      <td>95.5W</td>
      <td>69.0468</td>
      <td>998</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>89</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-28 12:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>25.5N</td>
      <td>96.4W</td>
      <td>74.8007</td>
      <td>993</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>90</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-28 17:02:05</td>
      <td>1983</td>
      <td>HU</td>
      <td>25.4N</td>
      <td>97.4W</td>
      <td>80.5546</td>
      <td>986</td>
      <td>L</td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>91</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-28 18:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>25.4N</td>
      <td>97.5W</td>
      <td>80.5546</td>
      <td>986</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>92</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>25.5N</td>
      <td>98.5W</td>
      <td>46.0312</td>
      <td>995</td>
      <td></td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
    </tr>
    <tr>
      <th>93</th>
      <td>AL051983</td>
      <td>CHANTAL</td>
      <td>1983-09-11 00:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>31.6N</td>
      <td>63.3W</td>
      <td>40.2773</td>
      <td>1005</td>
      <td></td>
      <td>3 days 18:00:00</td>
      <td>1983-09-14 18:00:00</td>
      <td>1983-09-11 00:00:00</td>
    </tr>
    <tr>
      <th>94</th>
      <td>AL051983</td>
      <td>CHANTAL</td>
      <td>1983-09-11 06:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>32.0N</td>
      <td>62.4W</td>
      <td>51.7851</td>
      <td>1000</td>
      <td></td>
      <td>3 days 18:00:00</td>
      <td>1983-09-14 18:00:00</td>
      <td>1983-09-11 00:00:00</td>
    </tr>
    <tr>
      <th>95</th>
      <td>AL051983</td>
      <td>CHANTAL</td>
      <td>1983-09-11 12:00:00</td>
      <td>1983</td>
      <td>TS</td>
      <td>32.4N</td>
      <td>61.2W</td>
      <td>63.2929</td>
      <td>996</td>
      <td></td>
      <td>3 days 18:00:00</td>
      <td>1983-09-14 18:00:00</td>
      <td>1983-09-11 00:00:00</td>
    </tr>
    <tr>
      <th>96</th>
      <td>AL051983</td>
      <td>CHANTAL</td>
      <td>1983-09-11 18:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>32.8N</td>
      <td>60.0W</td>
      <td>74.8007</td>
      <td>994</td>
      <td></td>
      <td>3 days 18:00:00</td>
      <td>1983-09-14 18:00:00</td>
      <td>1983-09-11 00:00:00</td>
    </tr>
    <tr>
      <th>97</th>
      <td>AL051983</td>
      <td>CHANTAL</td>
      <td>1983-09-12 00:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>33.1N</td>
      <td>58.9W</td>
      <td>74.8007</td>
      <td>994</td>
      <td></td>
      <td>3 days 18:00:00</td>
      <td>1983-09-14 18:00:00</td>
      <td>1983-09-11 00:00:00</td>
    </tr>
    <tr>
      <th>98</th>
      <td>AL051983</td>
      <td>CHANTAL</td>
      <td>1983-09-12 06:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>33.6N</td>
      <td>57.6W</td>
      <td>74.8007</td>
      <td>994</td>
      <td></td>
      <td>3 days 18:00:00</td>
      <td>1983-09-14 18:00:00</td>
      <td>1983-09-11 00:00:00</td>
    </tr>
    <tr>
      <th>99</th>
      <td>AL051983</td>
      <td>CHANTAL</td>
      <td>1983-09-12 12:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>34.0N</td>
      <td>56.3W</td>
      <td>74.8007</td>
      <td>994</td>
      <td></td>
      <td>3 days 18:00:00</td>
      <td>1983-09-14 18:00:00</td>
      <td>1983-09-11 00:00:00</td>
    </tr>
  </tbody>
</table>
<p>100 rows × 13 columns</p>
</div>




```python
# Filter only storms that reached Landfall and create dataframe
landfall_df = merge_df.loc[merge_df['Landfall'] == "L"]
```


```python
# Find the nearest city to the Landfall cooridinates using the Citipy
from citipy import citipy

# Strip the Direction from the Latitude and Longitude
lats = landfall_df["Latitude"].str.split("([A-Z]+)", expand=True)
lons = landfall_df["Longitude"].str.split("([A-Z]+)", expand=True)

# Grab the number from index 0
lats = lats[0]
lons = lons[0]

# Use citipy to find the nearest city
landfall_df.loc[:, "Latitude"] = lats
landfall_df.loc[:, "Longitude"] = lons

# Change the column to numeric
landfall_df["Latitude"] = pd.to_numeric(landfall_df["Latitude"])
landfall_df["Longitude"] = pd.to_numeric(landfall_df["Longitude"])

# Convert Longitude column to negative
landfall_df["Longitude"] *= -1


# Use citipy to find the nearest city
latitude = landfall_df["Latitude"]
longitude = landfall_df["Longitude"]
coordinates = zip(latitude, longitude)
cities = []
for coordinate_pair in coordinates:
    lat, lon = coordinate_pair
    cities.append(citipy.nearest_city(lat,lon))
```

    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\pandas\core\indexing.py:537: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self.obj[item] = s
    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\ipykernel_launcher.py:17: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\ipykernel_launcher.py:18: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\ipykernel_launcher.py:21: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    


```python
# Add city name column to Landfall dataframe
city_name = []
for city in cities:
    name = city.city_name
    country_code = city.country_code
    city_name.append(name+', ' + country_code)
landfall_df.loc[:, "Nearest City"] = city_name
landfall_df.head()
```

    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\pandas\core\indexing.py:357: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self.obj[key] = _infer_fill_value(value)
    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\pandas\core\indexing.py:537: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      self.obj[item] = s
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Storm_Id</th>
      <th>Name</th>
      <th>Date</th>
      <th>Year</th>
      <th>Status</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Windspeed</th>
      <th>Pressure</th>
      <th>Landfall</th>
      <th>Duration</th>
      <th>End Date</th>
      <th>Start Date</th>
      <th>Nearest City</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>76</th>
      <td>AL031983</td>
      <td>ALICIA</td>
      <td>1983-08-18 07:00:00</td>
      <td>1983</td>
      <td>HU</td>
      <td>29.1</td>
      <td>-95.1</td>
      <td>115.0780</td>
      <td>962</td>
      <td>L</td>
      <td>3 days 06:00:00</td>
      <td>1983-08-19 00:00:00</td>
      <td>1983-08-15 18:00:00</td>
      <td>santa fe, us</td>
    </tr>
    <tr>
      <th>90</th>
      <td>AL041983</td>
      <td>BARRY</td>
      <td>1983-08-28 17:02:05</td>
      <td>1983</td>
      <td>HU</td>
      <td>25.4</td>
      <td>-97.4</td>
      <td>80.5546</td>
      <td>986</td>
      <td>L</td>
      <td>4 days 18:00:00</td>
      <td>1983-08-29 00:00:00</td>
      <td>1983-08-24 06:00:00</td>
      <td>matamoros, mx</td>
    </tr>
    <tr>
      <th>163</th>
      <td>AL101984</td>
      <td>DIANA</td>
      <td>1984-09-13 07:00:00</td>
      <td>1984</td>
      <td>HU</td>
      <td>33.9</td>
      <td>-78.0</td>
      <td>92.0624</td>
      <td>979</td>
      <td>L</td>
      <td>7 days 12:00:00</td>
      <td>1984-09-16 00:00:00</td>
      <td>1984-09-08 12:00:00</td>
      <td>wilmington, us</td>
    </tr>
    <tr>
      <th>349</th>
      <td>AL021985</td>
      <td>BOB</td>
      <td>1985-07-25 03:00:00</td>
      <td>1985</td>
      <td>HU</td>
      <td>32.2</td>
      <td>-80.5</td>
      <td>74.8007</td>
      <td>1003</td>
      <td>L</td>
      <td>2 days 18:00:00</td>
      <td>1985-07-25 12:00:00</td>
      <td>1985-07-22 18:00:00</td>
      <td>hilton head island, us</td>
    </tr>
    <tr>
      <th>383</th>
      <td>AL041985</td>
      <td>DANNY</td>
      <td>1985-08-15 16:03:00</td>
      <td>1985</td>
      <td>HU</td>
      <td>29.6</td>
      <td>-92.7</td>
      <td>92.0624</td>
      <td>987</td>
      <td>L</td>
      <td>2 days 06:00:00</td>
      <td>1985-08-16 06:00:00</td>
      <td>1985-08-14 00:00:00</td>
      <td>jennings, us</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Merge landfall and original dataframe 
storm_added_fields = pd.merge(merge_df, landfall_df, how="outer", on="Storm_Id")

storm_added_fields = storm_added_fields.loc[:, ["Storm_Id", "Name_x", "Date_x", "Year_x", "Status_x", "Latitude_x", "Longitude_x"
                                    ,"Windspeed_x", "Pressure_x", "Start Date_x", "End Date_x", "Duration_x", "Landfall_y"
                                    ,"Latitude_y", "Longitude_y", "Windspeed_y", "Nearest City"]]

storm_added_fields_df = storm_added_fields.rename(columns={"Storm_Id": "Storm ID", "Name_x":"Name", "Date_x":"Date", "Year_x": "Year", "Status_x":"Status"
                                                       ,"Latitude_x" : "Max Latitude", "Longitude_x": "Max Longitude"
                                                       ,"Windspeed_x" : "Max Windspeed", "Pressure_x" : "Max Pressure"
                                                       ,"Start Date_x" : "Start Date", "End Date_x" : "End Date", "Duration_x" : "Duration"
                                                       ,"Landfall_y" : "Landfall", "Latitude_y" : "Lf Latitude", "Longitude_y" : "Lf Longitude"
                                                       ,"Windspeed_y" : "Lf Windspeed", "Nearest City": "Nearest City"})


storm_added_fields_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Storm ID</th>
      <th>Name</th>
      <th>Date</th>
      <th>Year</th>
      <th>Status</th>
      <th>Max Latitude</th>
      <th>Max Longitude</th>
      <th>Max Windspeed</th>
      <th>Max Pressure</th>
      <th>Start Date</th>
      <th>End Date</th>
      <th>Duration</th>
      <th>Landfall</th>
      <th>Lf Latitude</th>
      <th>Lf Longitude</th>
      <th>Lf Windspeed</th>
      <th>Nearest City</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>22.8N</td>
      <td>85.0W</td>
      <td>46.0312</td>
      <td>1001</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 12:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>23.2N</td>
      <td>84.2W</td>
      <td>57.5390</td>
      <td>995</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 18:00:00</td>
      <td>1982</td>
      <td>HU</td>
      <td>24.0N</td>
      <td>83.6W</td>
      <td>86.3085</td>
      <td>985</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-04 00:00:00</td>
      <td>1982</td>
      <td>HU</td>
      <td>24.8N</td>
      <td>83.4W</td>
      <td>74.8007</td>
      <td>992</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-04 06:00:00</td>
      <td>1982</td>
      <td>TS</td>
      <td>24.9N</td>
      <td>84.1W</td>
      <td>63.2929</td>
      <td>998</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Find row with max windspeed and return all columns in that row.
clean_storm_df = storm_added_fields_df.iloc[storm_added_fields_df.reset_index().groupby(['Storm ID'])["Max Windspeed"].idxmax()]
clean_storm_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Storm ID</th>
      <th>Name</th>
      <th>Date</th>
      <th>Year</th>
      <th>Status</th>
      <th>Max Latitude</th>
      <th>Max Longitude</th>
      <th>Max Windspeed</th>
      <th>Max Pressure</th>
      <th>Start Date</th>
      <th>End Date</th>
      <th>Duration</th>
      <th>Landfall</th>
      <th>Lf Latitude</th>
      <th>Lf Longitude</th>
      <th>Lf Windspeed</th>
      <th>Nearest City</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 18:00:00</td>
      <td>1982</td>
      <td>HU</td>
      <td>24.0N</td>
      <td>83.6W</td>
      <td>86.3085</td>
      <td>985</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>338</th>
      <td>AL011985</td>
      <td>ANA</td>
      <td>1985-07-19 00:00:00</td>
      <td>1985</td>
      <td>TS</td>
      <td>44.2N</td>
      <td>60.3W</td>
      <td>69.0468</td>
      <td>996</td>
      <td>1985-07-16 18:00:00</td>
      <td>1985-07-19 00:00:00</td>
      <td>2 days 06:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>586</th>
      <td>AL011986</td>
      <td>ANDREW</td>
      <td>1986-06-06 12:00:00</td>
      <td>1986</td>
      <td>TS</td>
      <td>30.7N</td>
      <td>78.0W</td>
      <td>51.7851</td>
      <td>1005</td>
      <td>1986-06-06 00:00:00</td>
      <td>1986-06-08 18:00:00</td>
      <td>2 days 18:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>854</th>
      <td>AL011988</td>
      <td>ALBERTO</td>
      <td>1988-08-07 12:00:00</td>
      <td>1988</td>
      <td>TS</td>
      <td>41.5N</td>
      <td>69.0W</td>
      <td>40.2773</td>
      <td>1002</td>
      <td>1988-08-07 12:00:00</td>
      <td>1988-08-08 06:00:00</td>
      <td>0 days 18:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1987</th>
      <td>AL011991</td>
      <td>ANA</td>
      <td>1991-07-04 06:00:00</td>
      <td>1991</td>
      <td>TS</td>
      <td>37.1N</td>
      <td>67.8W</td>
      <td>51.7851</td>
      <td>1002</td>
      <td>1991-07-04 00:00:00</td>
      <td>1991-07-05 12:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Create Bins for each storm category according to https://en.wikipedia.org/wiki/Maximum_sustained_wind
max_wind = clean_storm_df["Max Windspeed"].max()
print(max_wind)
min_wind = clean_storm_df["Max Windspeed"].min()
print(min_wind)
bins = [35, 73, 95, 110, 129, 156, 160]

# Create the names for the four bins
category_names = ['Tropical Storm', 'Category One', 'Category Two', 'Category Three', 'Category Four', 'Category Five']
category_values = [0,1, 2, 3, 4, 5]
```

    184.1248
    40.2773
    


```python
# Create new category column
storm_category = pd.cut(clean_storm_df["Max Windspeed"], bins, labels=category_names)
category_value = pd.cut(clean_storm_df["Max Windspeed"], bins, labels=category_values)
```


```python
# Add column to clean storm dataframe
clean_storm_df["Storm Category"] = storm_category
clean_storm_df["Category Value"] = category_value
clean_storm_df['Category Value'] = pd.to_numeric(clean_storm_df['Category Value'])
clean_storm_df.to_csv('CleanData.csv')
clean_storm_df.head()
```

    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\ipykernel_launcher.py:2: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      
    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\ipykernel_launcher.py:3: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      This is separate from the ipykernel package so we can avoid doing imports until
    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\ipykernel_launcher.py:4: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      after removing the cwd from sys.path.
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Storm ID</th>
      <th>Name</th>
      <th>Date</th>
      <th>Year</th>
      <th>Status</th>
      <th>Max Latitude</th>
      <th>Max Longitude</th>
      <th>Max Windspeed</th>
      <th>Max Pressure</th>
      <th>Start Date</th>
      <th>End Date</th>
      <th>Duration</th>
      <th>Landfall</th>
      <th>Lf Latitude</th>
      <th>Lf Longitude</th>
      <th>Lf Windspeed</th>
      <th>Nearest City</th>
      <th>Storm Category</th>
      <th>Category Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>AL011982</td>
      <td>ALBERTO</td>
      <td>1982-06-03 18:00:00</td>
      <td>1982</td>
      <td>HU</td>
      <td>24.0N</td>
      <td>83.6W</td>
      <td>86.3085</td>
      <td>985</td>
      <td>1982-06-03 06:00:00</td>
      <td>1982-06-04 18:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Category One</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>338</th>
      <td>AL011985</td>
      <td>ANA</td>
      <td>1985-07-19 00:00:00</td>
      <td>1985</td>
      <td>TS</td>
      <td>44.2N</td>
      <td>60.3W</td>
      <td>69.0468</td>
      <td>996</td>
      <td>1985-07-16 18:00:00</td>
      <td>1985-07-19 00:00:00</td>
      <td>2 days 06:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Tropical Storm</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>586</th>
      <td>AL011986</td>
      <td>ANDREW</td>
      <td>1986-06-06 12:00:00</td>
      <td>1986</td>
      <td>TS</td>
      <td>30.7N</td>
      <td>78.0W</td>
      <td>51.7851</td>
      <td>1005</td>
      <td>1986-06-06 00:00:00</td>
      <td>1986-06-08 18:00:00</td>
      <td>2 days 18:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Tropical Storm</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>854</th>
      <td>AL011988</td>
      <td>ALBERTO</td>
      <td>1988-08-07 12:00:00</td>
      <td>1988</td>
      <td>TS</td>
      <td>41.5N</td>
      <td>69.0W</td>
      <td>40.2773</td>
      <td>1002</td>
      <td>1988-08-07 12:00:00</td>
      <td>1988-08-08 06:00:00</td>
      <td>0 days 18:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Tropical Storm</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1987</th>
      <td>AL011991</td>
      <td>ANA</td>
      <td>1991-07-04 06:00:00</td>
      <td>1991</td>
      <td>TS</td>
      <td>37.1N</td>
      <td>67.8W</td>
      <td>51.7851</td>
      <td>1002</td>
      <td>1991-07-04 00:00:00</td>
      <td>1991-07-05 12:00:00</td>
      <td>1 days 12:00:00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Tropical Storm</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



# Quantity of Storms Over the Years


```python
# Separate max windspeed, pressure and category data by year and get the average
grouped = clean_storm_df.groupby(['Year'])

# Set variables
quantity = grouped['Duration'].count()

# Set year labels
first_year = pd.to_numeric(clean_storm_df['Year'].min())
last_year = pd.to_numeric(clean_storm_df['Year'].max())
x_labels = np.arange(first_year,last_year,2)

# Plot total quantity
quantity_line = plt.plot(quantity)
plt.xlabel('Year')
plt.ylabel('Number of Storms')
plt.title("Total Number of Storms")
plt.ylim(0,30)
plt.xlim(-1,36)
plt.xticks(x_labels,x_labels,rotation='vertical')
plt.grid()
plt.tight_layout()

# Show and save figure
plt.savefig("total_storms.png")
plt.show()
```


![png](output_23_0.png)



```python
# Create df with counts to ensure no year is left behind
count_df = grouped.count()
# Count storms category 3 or stronger
over3_count = clean_storm_df[clean_storm_df['Category Value'] >= 3].groupby(['Year']).size()
# Add count over 3 to count data frame
count_df['Over 3'] = over3_count
# Replace NaN values with zeros
count_df = count_df.fillna(0)
quantity_over3 = count_df['Over 3']

# Plot total quantity
over3_line = plt.plot(quantity_over3)
plt.xlabel('Year')
plt.ylabel('Number of Storms')
plt.title("Storms Over Category 3")
plt.ylim(-1,8)
plt.xlim(-1,36)
plt.xticks(x_labels,x_labels,rotation='vertical')
plt.grid()
plt.tight_layout()

# Show and save figure
plt.savefig("over3.png")
plt.show()
```


![png](output_24_0.png)


# Strength of Storms Over the Years


```python
# Create a line graph showing quantity of storms over time
# Separate max windspeed, pressure and category data by year and get the average
strength_df = clean_storm_df[["Year","Max Windspeed","Max Pressure","Duration"]]
strength_df['Duration'] = pd.to_numeric(strength_df['Duration'])
strength_year = strength_df.groupby(['Year'])

# Set variables
max_windspeed_avg = strength_year['Max Windspeed'].mean()
max_pressure_avg = strength_year['Max Pressure'].mean()
duration_avg = strength_year['Duration'].mean()

# Create a line graph showing windspeed of storms over time
# Plot
graph = plt.plot(max_windspeed_avg)
plt.xlabel('Year')
plt.ylabel('Average Max Windspeed (mph)')
plt.title("Average Max Windspeed")
plt.ylim(50,110)
plt.xlim(-1,36)
plt.xticks(x_labels,x_labels,rotation='vertical')
plt.grid()
 
plt.tight_layout()
plt.savefig("windspeeds.png")
plt.show()
```

    C:\Users\cburd\Anaconda3\envs\PythonData\lib\site-packages\ipykernel_launcher.py:4: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      after removing the cwd from sys.path.
    


![png](output_26_1.png)



```python
# Create a line graph showing pressure of storms over time
graph = plt.plot(max_pressure_avg)
plt.xlabel('Year')
plt.ylabel('Average Min Pressure (mbars)')
plt.title("Average Min Pressure")
plt.xlim(-1,36)
plt.xticks(x_labels,x_labels,rotation='vertical')
plt.grid()
 
plt.tight_layout()
plt.savefig("pressures.png")
plt.show()
```


![png](output_27_0.png)



```python
# Create a line graph showing duration of storms over time
# Separate max windspeed data by year and get the average
graph = plt.plot(duration_avg)
plt.xlabel('Year')
plt.ylabel('Average Max Duration (Days)')
plt.title("Average Max Duration")
plt.ylim(150000000000000.56,750000000000000.1)
plt.xlim(-1,36)
plt.xticks(x_labels,x_labels,rotation='vertical')
plt.grid()
 
plt.tight_layout()
plt.savefig("avg_duration.png")
plt.show()
```


![png](output_28_0.png)


# Most Dangerous Cities in Relationship to Storms


```python
# Bar grapth
# Filter for only cities with 3 storms of more
# Group by cities to get count and avg max winspeed of the storms that hit each city
city_count = clean_storm_df.groupby("Nearest City")['Storm ID'].count()
city_wind = clean_storm_df.groupby("Nearest City")['Max Windspeed'].mean()

# Create data frame
cities_df = pd.DataFrame({"NumberofStorms": city_count,"AvgMaxWindspeed": city_wind})
# Sort to find cities with the most storms
cities_df = cities_df.sort_values('NumberofStorms', ascending =False)
# Keep only cities with 4 storms or more
cities_df = cities_df.loc[cities_df['NumberofStorms'] >= 4,:]

#bar_chart = plt.bar(cities_df.index,cities_df['Number of Storms'])
#bar_chart.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
bar_chart = cities_df.NumberofStorms.plot(kind='bar',ec='black')
plt.xticks(np.arange(0,4,1),('Havenlock, NC','Tallahassee, FL','Port Arthur,TX','Wilmington, NC'), rotation='vertical')
plt.xlabel('')
plt.ylabel('Number of Storms')
plt.title('Cities With the Most Storms')
plt.savefig("top_cities.png", bbox_inches="tight")
plt.show()
```


![png](output_30_0.png)



```python
# Bar graph with average strength of storms
# Loop through all cities to search for the average strength of each
#top_cities = cities_df.index
#cities_wind = []

#for city in top_cities:
    #filtered = clean_storm_df.loc[clean_storm_df['Nearest City'] == city,:]
    #city_wind = filtered['Max Windspeed'].mean()
    #cities_wind.append(city_wind)
bar_chart = cities_df.AvgMaxWindspeed.plot(kind='bar',ec='black')
plt.xticks(np.arange(0,4,1),('Havenlock, NC','Tallahassee, FL','Port Arthur, TX','Wilmington, NC'), rotation='vertical')
plt.xlabel('')
plt.ylabel('Windspeed (mph)')
plt.title('Strength of Storms in Top Cities')
plt.savefig("top_strength.png", bbox_inches="tight")
plt.show()
```


![png](output_31_0.png)


# Storm Season


```python
# Get month of each storm
dates = clean_storm_df['Date']
months = dates.dt.month
# Create data frame of storm count in each month
months_df = pd.DataFrame({'Storm Count': months.value_counts()})
months_df = months_df.reset_index().rename(columns={"index":"Month"}).sort_values('Month')
# Filter for storm season (June to November)
storm_season = months_df[(months_df['Month'] >= 6) & (months_df['Month'] <= 11)]
# Plot Results
plt.bar(storm_season['Month'],storm_season['Storm Count'],ec='black')
# Aesthetics
plt.xticks(np.arange(6,12,1),['Jun','Jul','Aug','Sep','Oct','Nov'],rotation=25)
plt.title('Months with the Most Storms')
plt.xlabel('Month')
plt.ylabel('Number of Storms')
plt.savefig("months.png", bbox_inches="tight")
plt.show()
```


![png](output_33_0.png)



```python
# Pie Graaph showing distribution
labels = ['Jun','Jul','Aug','Sep','Oct','Nov']
sizes =  storm_season['Storm Count']
explode = (0,0,0,.1,0,0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes,labels=labels,explode=explode,autopct ="%1.1f%%",shadow=True,startangle=160,
        textprops=dict(color="w",weight='bold'))
ax1.axis('equal')
plt.legend(title='Months',loc='center right',bbox_to_anchor=(.6, 0, 0.5, 1))
plt.title('Storm Season Distribution')

# Aesthetics
plt.savefig("month_pie.png", bbox_inches="tight")
plt.show()
```


![png](output_34_0.png)


# Storm Duration


```python
'''How long to storms last on average? Do stronger storms last longer?
	Line graph for duration variance over time. 
Bubble plot with size and color based on category and strenght respectively.'''
# Divide data frame into the different storm categories
tropical_df = clean_storm_df.loc[clean_storm_df['Storm Category'] == 'Tropical Storm',:]
tropical_dur = tropical_df['Duration'] / np.timedelta64(1, 'D')
tropical_wind = tropical_df['Max Windspeed']
Tropical = plt.scatter(tropical_wind,tropical_dur)

one_df = clean_storm_df.loc[clean_storm_df['Storm Category'] == 'Category One',:]
one_dur = one_df['Duration']/ np.timedelta64(1, 'D')
one_wind = one_df['Max Windspeed']
One = plt.scatter(one_wind,one_dur,facecolor='red')

two_df = clean_storm_df.loc[clean_storm_df['Storm Category'] == 'Category Two',:]
two_dur = two_df['Duration']/ np.timedelta64(1, 'D')
two_wind = two_df['Max Windspeed']
Two = plt.scatter(two_wind,two_dur,facecolor='green')

Three_df = clean_storm_df.loc[clean_storm_df['Storm Category'] == 'Category Three',:]
Three_dur = Three_df['Duration']/ np.timedelta64(1, 'D')
Three_wind = Three_df['Max Windspeed']
Three = plt.scatter(Three_wind,Three_dur,facecolor='orange')

Four_df = clean_storm_df.loc[clean_storm_df['Storm Category'] == 'Category Four',:]
Four_dur = Four_df['Duration']/ np.timedelta64(1, 'D')
Four_wind = Four_df['Max Windspeed']
Four = plt.scatter(Four_wind,Four_dur,facecolor='purple')

Five_df = clean_storm_df.loc[clean_storm_df['Storm Category'] == 'Category Five',:]
Five_dur = Five_df['Duration']/ np.timedelta64(1, 'D')
Five_wind = Five_df['Max Windspeed']
Five = plt.scatter(Five_wind,Five_dur,facecolor='grey')

# Aesthetics
lgnd = plt.legend((Tropical, One, Two,Three,Four,Five),
                  ('Tropical Storm','Category One','Category Two','Category Three','Category Four','Category Five'),
           loc='center right',title="Storm Categories",bbox_to_anchor=(.89, 0, 0.5, 1))
plt.xlabel('Windspeed (mph)')
plt.ylim(-1,35)
plt.ylabel('Duration (Days)')
plt.title('Storm Duration by Category')
plt.grid()
plt.savefig("scatter.png", bbox_inches="tight")
plt.show()
```


![png](output_36_0.png)

