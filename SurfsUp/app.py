
import numpy as np
import sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
@app.route("/")
def welcome ():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )
#################################################
# Flask Routes
#################################################

app.route("/api/vi.0/precipitation")
def precipitation():
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    start_date = dt.date(2017, 8, 23 ) - dt.timedelta(days = 355)
    precipitation = session.query(measurement.date, measurement.prcp).all()
    return jsonify(dict(precipitation))

#Return a JSON list of stations from the datase

app.route("/api/v1.0/stations")
def station():
    session = session(engine)
    stations_query = session.query(station.station,station.id).all()

    station_lists = []
    for station, id in stations_query:
        station_lists_values = {}
        station_lists_values['station'] = station
        station_lists_values['id'] = id
        station_lists.append(stations_lists_values)
    return jsonify (station_lists)

#Query the dates and temperature observations of the most-active station for the previous year of data.
#Return a JSON list of temperature observations for the previous year.

def tobs():
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    start_date = dt.date(2017, 8, 23 ) - dt.timedelta(days = 355)
    active_station = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()[0]
    temp = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date >= start_date).filter(measurement.station == active_station).all()
    return jsonify(temp)
    


#Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>")
def start_date(start):
    start_result = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
#TMIN,TAVG,TMAX
    TMIN = start_result[0[0]]
    TMAX = start_result[0[1]]
    TAVG = start_result[0[2]]
    return jsonify(start_result)
                                 
@app.route("/api/v1.0/<start>")
def start_end_date(start, end):
    start_result = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.data <= end).all()
#TMIN,TAVG,TMAX
    TMIN = start_result[0[0]]
    TMAX = start_result[0[1]]
    TAVG = start_result[0[2]]
    return jsonify(start_end_date)
  

if __name__ == "__main__":
    app.run(debug=True)










