import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def prcp_data():
    """Return precipitation data"""
    # Query for the dates and temperature observations from the last year.
    precip_last_year = dt.date.today()-dt.timedelta(days=365)
    
    prcp_data = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date >= precip_last_year).all()
    
    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    prcp_json = {date: prcp for date, prc in prcp_data}
    # Return the json representation of your dictionary.
    return jsonify(prcp_json)

@app.route("/api/v1.0/stations")
def stations_data():
    """Return all stations"""
    # Return a json list of stations from the dataset.
    station_data = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations_json = list(np.ravel(station_data))

    return jsonify(stations_json)

@app.route("/api/v1.0/tobs")
def temp_data():
    """Return temperature data for the last year"""
    # Return a json list of Temperature Observations (tobs) for the previous year
    precip_last_year = dt.date.today()-dt.timedelta(days=365)
    
    temp_data = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date >= precip_last_year).all()
        
    temp_json = {date: tobs for date, tobs in temp_data}

    return jsonify(temp_json)

@app.route("/api/v1.0/<start>")
def start_temp_stats():
    """Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range"""
     """When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""

    start_date_entry = input('Enter a start date in YYYY-MM-DD format')
    year, month, day = map(int, date_entry.split('-'))
    start_date = datetime.date(year, month, day)
    
    query = session.query(Measurement, Station).join(Station)
    # https://stackoverflow.com/questions/6044309/sqlalchemy-how-to-join-several-tables-by-one-query
    
    start_temp_data = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date >= start_date).all()
        
    TMIN = start_temp_data.min().all()
    TAVG = start_temp_data.mean().all()
    TMAX = start_temp_data.max().all()
    
    start_temp_stats_json = {date: TMIN : TAVG: TMAX for date in start_temp_data}

    return jsonify()


@app.route("/api/v1.0/<start>/<end>")
def start_end_temp_stats():
    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""


    return jsonify()

if __name__ == '__main__':
    app.run(debug=True)
