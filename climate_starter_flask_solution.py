import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import json

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
# print(Base.classes)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

### Routes: WELCOME
#  API welcome page listing all available APIs.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
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
    app.run(debug=True)