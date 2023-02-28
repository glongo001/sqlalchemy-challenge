#Import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#Create app
app = Flask(__name__)

#start session
session = Session(engine)

#Define homepage route
@app.route("/")
def index():
    return (
        f"Welcome to the climate analysis of Hawaii<br/><br/>"
        f"All Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"'start' and 'end' date should be in the YYYY-MM-DD format.</p>"
    )

#Define precipitation route, display date and precipitation of the last 12 months of data
@app.route("/api/v1.0/precipitation")
def precipitation():
    #First get the last 12 months
    most_recent = dt.datetime(2017, 8, 23)
    one_year_before = most_recent - dt.timedelta(days=365)
    #Get precipitation data for last 12 months
    precipitation = session.query(measurement.date, measurement.prcp).\
                    filter(measurement.date >= one_year_before).all()
    
    #Close session
    session.close()
    
    #Create dictionary with date as the key and prcp as the value
    prcp = {}
    for date, value in precipitation:
        prcp[date] = value

    # Return the JSON representation of the precipitation data
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    #Get stations
    all_stations = session.query(station.station).all()
    
    #Close session
    session.close()
    
    #Convert all_stations query reults to list using numpy
    station_list = list(np.ravel(all_stations))
    
    #Return JSON representation
    return jsonify(station_list)
    
@app.route("/api/v1.0/tobs")
def tobs():
    #First get the initial date to look at
    most_recent = dt.datetime(2017, 8, 23)
    one_year_before = most_recent - dt.timedelta(days=365)
    #Find the active stations
    active_stations = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()
    #Get the most active station
    most_active = active_stations[0][0]
    #Get dates and temperature observations for the most-active station during last 12 months
    most_active_12_months = session.query(measurement.date, measurement.tobs).filter(measurement.date >= one_year_before, measurement.station == most_active).all()
    
    #Close session
    session.close()
    
    #Convert most_active_12_months query reults to list using numpy
    most_active_list = list(np.ravel(most_active_12_months))
    
    #Return JSON representation
    return jsonify(most_active_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start=None, end=None):
    try:
        #If no end date is provided, use the last date of available data
        if end is None:
            end = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
            
        #Convert start and end dates to datetime objects
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
        end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    
    except ValueError:
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD."}), 400
    
    #Query for the minimum, average, and maximum temperatures
    range_tobs = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date, measurement.date <= end_date).all()

    #Close session
    session.close()

    #Convert all_stations query reults to list using numpy
    tobs_list =  list(np.ravel(range_tobs))

    #Return JSON representation of temperature values
    return jsonify(tobs_list)
    
if __name__ == '__main__':
    app.run(debug=True)
