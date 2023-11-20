# Import the dependencies.
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """All available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
# open session
# session already open

# Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# copy pcrp code from Climate
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    data_prcp = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= last_year).\
    all()

# close session
    session.close()

# Return the JSON representation of your dictionary.
# Convert list of tuples into normal list
    last_year_pcrp = list(np.ravel(data_prcp))

    return jsonify(last_year_pcrp)

@app.route("/api/v1.0/stations")
def stations():
# open session
# session already open

# Return a JSON list of stations from the dataset.
    results = session.query(station.station).all()

# close session
    session.close()

# Return the JSON representation of your dictionary.
# Convert list of tuples into normal list
    stations_json = list(np.ravel(results))

    return jsonify(stations_json)

@app.route("/api/v1.0/tobs")
def tobs():
# open session
# session already open

# Query the dates and temperature observations of the most-active station for the previous year of data.
# copy tobs code from Climate
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_obs = session.query(measurement.tobs).\
        filter(measurement.date >= last_year).\
        filter(measurement.station == 'USC00519281').\
        all()

# close session
    session.close()

# Return the JSON representation of your dictionary.
# Convert list of tuples into normal list
    tobs_json = list(np.ravel(temp_obs))

    return jsonify(tobs_json)

@app.route("/api/v1.0/<start>")
def start():
# open session
# session already open

# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# set start time
    start = dt.datetime.strptime(start, "06/01/2017")
# copy min, max, avg code from Climate
    start_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        all()

# close session
    session.close()

# Return the JSON representation of your dictionary.
# Convert list of tuples into normal list
    start_json = list(np.ravel(start_results))

    return jsonify(start_json)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
# open session
# session already open

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
# set start time
    start = dt.datetime.strptime(start, "2017-06-01")
    end = dt.datetime.strptime(end, "2017-06-30")
# copy min, max, avg code from Climate
    between_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).\
        all()

# close session
    session.close()

# Return the JSON representation of your dictionary.
# Convert list of tuples into normal list
    between_json = list(np.ravel(between_results))

    return jsonify(between_json)

if __name__ == "__main__":
    app.run(debug=True)
