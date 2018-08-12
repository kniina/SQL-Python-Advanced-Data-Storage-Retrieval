

```python
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
```


```python
import numpy as np
import pandas as pd
```


```python
import datetime as dt
```


```python
from werkzeug.wrappers import Request, Response
```

# Reflect Tables into SQLAlchemy ORM


```python
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
```


```python
engine = create_engine("sqlite:///resources/hawaii.sqlite")
```


```python
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
```


```python
# We can view all of the classes that automap found
Base.classes.keys()
```




    ['measurement', 'station']




```python
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
```


```python
# Create our session (link) from Python to the DB
session = Session(engine)
```

# PRECIPITATION ANALYSIS


```python
# Design a query to retrieve the last 12 months of precipitation data and plot the results
# Calculate the date 1 year ago from today

yearAgo = dt.date(2017, 8 ,23)-dt.timedelta(days=365)

# Perform a query to retrieve the last 12 months of precipitation data
sel = [Measurement.date, Measurement.prcp]
precipitation = session.query(*sel).filter(Measurement.date >= yearAgo).all()

# Save the query results as a Pandas DataFrame and set the index to the date column
precipitationDF = pd.DataFrame(precipitation, columns=['Date', 'Precipitation']).set_index('Date')

# Sort the dataframe by date
precipDateDF = precipitationDF.groupby('Date').sum()
precipDateDF.head()

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
      <th>Precipitation</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-08-23</th>
      <td>2.71</td>
    </tr>
    <tr>
      <th>2016-08-24</th>
      <td>9.33</td>
    </tr>
    <tr>
      <th>2016-08-25</th>
      <td>0.54</td>
    </tr>
    <tr>
      <th>2016-08-26</th>
      <td>0.10</td>
    </tr>
    <tr>
      <th>2016-08-27</th>
      <td>0.32</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Use Pandas Plotting with Matplotlib to plot the data
precipDateDF.plot(color="lightseagreen", alpha=0.5)
plt.tight_layout()
plt.savefig('Images/precipitation.png')
plt.show()
```


![png](output_13_0.png)



```python
# Use Pandas to calcualte the summary statistics for the precipitation data
precipDateDF.describe()
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
      <th>Precipitation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>366.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.978907</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.776349</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.052500</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.405000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>1.087500</td>
    </tr>
    <tr>
      <th>max</th>
      <td>14.280000</td>
    </tr>
  </tbody>
</table>
</div>



# STATION ANALYSIS


```python
# How many stations are available in this dataset? -- ANSWER: 9
session.query(Station.station).count()
```




    9




```python
# What are the most active stations? 
# List the stations and the counts in descending order.

session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()
```




    [('USC00519281', 2772),
     ('USC00519397', 2724),
     ('USC00513117', 2709),
     ('USC00519523', 2669),
     ('USC00516128', 2612),
     ('USC00514830', 2202),
     ('USC00511918', 1979),
     ('USC00517948', 1372),
     ('USC00518838', 511)]




```python
# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature most active station?

session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).all()
```




    [(53.0, 87.0, 73.09795396419437)]



## TEMPERATURE OBSERVATIONS


```python
# Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram

# Design a query to retrieve the last 12 months of temperature observation data (tobs).
sel = [Measurement.station, Measurement.tobs]
session.query(*sel).filter(Measurement.date >= yearAgo).all()

# Filter by the station with the highest number of observations 
highObs = session.query(Measurement.station, Measurement.tobs).filter_by(station='USC00519281').filter(Measurement.date >= yearAgo).all()
highObsDF = pd.DataFrame(highObs)
highObsDF.head()

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
      <th>station</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00519281</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00519281</td>
      <td>77.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00519281</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00519281</td>
      <td>80.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00519281</td>
      <td>75.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Plot the results as a histogram with bins=12
highObsDF.plot.hist(bins=12, color="lightseagreen", alpha=0.5)
plt.savefig('Images/station-histogram.png')
plt.show()
```


![png](output_21_0.png)



```python
# Write a function called `calc_temps` that will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates

def calc_temps(start_date, end_date):
   
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all() 
```


```python
# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.

start_date = "2017-07-04"
end_date = "2017-07-14"

temps = calc_temps(start_date, end_date)

tempsDF = pd.DataFrame(temps, columns=['tmin', 'tavg', 'tmax'])
tempsDF
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
      <th>tmin</th>
      <th>tavg</th>
      <th>tmax</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>69.0</td>
      <td>77.942857</td>
      <td>82.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
tmin = tempsDF['tmin'].tolist()
tavg = tempsDF['tavg'].tolist()
tmax = tempsDF['tmax'].tolist()
```


```python
# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)

error = (tmax[0]-tmin[0])

tempsDF.plot.bar(y='tavg',yerr=error, color="lightseagreen", alpha=0.5, legend=None)

plt.title('Trip Avg Temp')
plt.ylabel('Temp (F)')
plt.xticks([])
plt.tight_layout()
plt.savefig('Images/temperature.png')
```


![png](output_25_0.png)



```python
# Calculate the rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation

rainfall = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation, func.sum(Measurement.prcp)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Station.station).order_by(func.sum(Measurement.prcp).desc()).all()

rainfallDF = pd.DataFrame(rainfall, columns = ['Station', 'Name', 'Latitude', 'Longitude', 'Elevation', 'Total Rainfall'])
rainfallDF
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
      <th>Station</th>
      <th>Name</th>
      <th>Latitude</th>
      <th>Longitude</th>
      <th>Elevation</th>
      <th>Total Rainfall</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>USC00511918</td>
      <td>HONOLULU OBSERVATORY 702.2, HI US</td>
      <td>21.31520</td>
      <td>-157.99920</td>
      <td>0.9</td>
      <td>4.16</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USC00513117</td>
      <td>KANEOHE 838.1, HI US</td>
      <td>21.42340</td>
      <td>-157.80150</td>
      <td>14.6</td>
      <td>4.16</td>
    </tr>
    <tr>
      <th>2</th>
      <td>USC00514830</td>
      <td>KUALOA RANCH HEADQUARTERS 886.9, HI US</td>
      <td>21.52130</td>
      <td>-157.83740</td>
      <td>7.0</td>
      <td>4.16</td>
    </tr>
    <tr>
      <th>3</th>
      <td>USC00516128</td>
      <td>MANOA LYON ARBO 785.2, HI US</td>
      <td>21.33310</td>
      <td>-157.80250</td>
      <td>152.4</td>
      <td>4.16</td>
    </tr>
    <tr>
      <th>4</th>
      <td>USC00517948</td>
      <td>PEARL CITY, HI US</td>
      <td>21.39340</td>
      <td>-157.97510</td>
      <td>11.9</td>
      <td>4.16</td>
    </tr>
    <tr>
      <th>5</th>
      <td>USC00518838</td>
      <td>UPPER WAHIAWA 874.3, HI US</td>
      <td>21.49920</td>
      <td>-158.01110</td>
      <td>306.6</td>
      <td>4.16</td>
    </tr>
    <tr>
      <th>6</th>
      <td>USC00519281</td>
      <td>WAIHEE 837.5, HI US</td>
      <td>21.45167</td>
      <td>-157.84889</td>
      <td>32.9</td>
      <td>4.16</td>
    </tr>
    <tr>
      <th>7</th>
      <td>USC00519397</td>
      <td>WAIKIKI 717.2, HI US</td>
      <td>21.27160</td>
      <td>-157.81680</td>
      <td>3.0</td>
      <td>4.16</td>
    </tr>
    <tr>
      <th>8</th>
      <td>USC00519523</td>
      <td>WAIMANALO EXPERIMENTAL FARM, HI US</td>
      <td>21.33556</td>
      <td>-157.71139</td>
      <td>19.5</td>
      <td>4.16</td>
    </tr>
  </tbody>
</table>
</div>



## CLIMATE APP


```python
# Design a Flask API based on the queries that you have just developed.
# Use FLASK to create your routes.

from flask import Flask, jsonify

app = Flask(__name__)
```


```python
### Routes: WELCOME
#  API welcome page listing all available APIs.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Climate App: Available Routes:<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"List of prior year rain totals<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"List of all stations in dataset<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"List of prior year temperature observations<br/>"
        f"<br/>"
        f"<a href='/api/v1.0/<start>'>/api/v1.0/<start></a><br/>"
        f"List of the minimum, average and max temperatures for a given start date<br/>"
         f"<br/>"       
        f"<a href='/api/v1.0/<start>/<end>'>/api/v1.0/<start>/<end></a><br/>"
        f"List of the minimum, average and max temperatures for a given date start-end range<br/>"
    )

### Routes: PRECIPITATION
#   Query for the dates and precipitation from the last year.
#   Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#   Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    yearAgo = dt.date.today()-dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= yearAgo).all()
    all_results = []
    for r in results:
        results_dict = {}
        results_dict["date"]= r.date
        results_dict["prcp"] = r.prcp
        all_results.append(results_dict)
    return jsonify(all_results)

### Routes:STATIONS
#   Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station, Station.name).all()
    return jsonify(stations)

### Routes: TEMPERATURE OBSERVATIONS
#   Return a JSON list of Temperature Observations (tobs) for the previous year

@app.route("/api/v1.0/tobs")
def temperature():
    yearAgo = dt.date.today()-dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= yearAgo).all()
    all_results = []
    for r in results:
        results_dict = {}
        results_dict["date"]= r.date
        results_dict["tobs"] = r.tobs
        all_results.append(results_dict)
    return jsonify(all_results)

### Routes: START 
#   Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

@app.route("/api/v1.0/<start>")
def start(start):
    start = "2017-07-04"
    end = "2017-07-14"
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    print(results)
    all_results = list(np.ravel(results))
    return(jsonify(all_results))

### Routes: START & END
#   When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start = "2017-07-04"
    end = "2017-07-14"
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    all_results = list(np.ravel(results))
    return(jsonify(all_results))

# Runs the application
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)
```

     * Running on http://localhost:9000/ (Press CTRL+C to quit)

