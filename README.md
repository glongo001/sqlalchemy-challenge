# Unit 10 Homework: Surf’s Up
I decided to do a climate analysis before going on a trip to Honolulu,Hawaii.

## Part 1: Analyze and Explore the Climate Data
1. First, I created a SQLAlchemy engine to connect to my SQLite database(hawaii.sqlite).
2. I connected to the database and saved references to the 'station' and 'measurements' tables.
3. I found the most recent date in the dataset (it was 2017-08-23) and obtained the precipitation data for the last 12 months of data.
4. I loaded the results onto a dataframe and created a plot to display those results:

![alt text](https://github.com/glongo001/sqlalchemy-challenge/blob/main/SurfsUp/precipitation_analysis.png)

5. I displayed the summary statistics for the precipitation data. The summary showed:
    - The count of datapoints was: 2015.00
    - The mean inches of precipitation were: 0.18
    - The standard deviation was: 0.46
    - The minimum inches of precipitation were: 0.00
    - The 25% inches of precipitation were: 0.00
    - The 50% inches of precipitation were: 0.02
    - The 75% inches of precipitation were: 0.13
    - The maximum inches of precipitation were: 6.70
6. Then, I obtained the total number of stations in the dataset (they were 9) and listed the stations and the number of entries from each station in the dataset in descending order:
    - USC00519281: 2772 entries
    - USC00519397: 2724 entries
    - USC00513117: 2709 entries
    - USC00519523: 2669 entries
    - USC00516128: 2612 entries
    - USC00514830: 2202 entries
    - USC00511918: 1979 entries
    - USC00517948: 1372 entries
    - USC00518838: 511 entries
7. I obtained the lowest, highest and average temperatures for the most active station:
    - Most active station: USC00519281 
    - Minimum temperature: 54.0 
    - Maximum temperature: 85.0 
    - Average temperature: 71.66

![alt text](https://github.com/glongo001/sqlalchemy-challenge/blob/main/SurfsUp/station_analysis.png)

## Part 2: Design Your Climate App
1. I created a Flask API. In the homepage I displayed all the available routes:
    - /api/v1.0/precipitation
    - /api/v1.0/stations
    - /api/v1.0/tobs
    - /api/v1.0/start
    - /api/v1.0/start/end
        - Where the 'start' and 'end' date should be in the YYYY-MM-DD format.
2. In /api/v1.0/precipitation, I displayed the last 12 months of precipitation data.
3. In /api/v1.0/stations I displayed a list of the 9 stations in the dataset.
4. In /api/v1.0/tobs I displayed the temperature observations for the most active station 'USC00519281' during the last 12 months of data.
5. In /api/v1.0/start & /api/v1.0/start/end, I displayed a list that calculated the minimumm temperature, the average temperature and the maximum temperature for the 'start' and 'end' dates entered in the url by the user.