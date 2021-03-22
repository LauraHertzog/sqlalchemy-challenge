#import Flask
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect = True)

Base.classes.keys()

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

#create app
app = Flask(__name__)

#flask routes 

@app.route("/")
def Home():
    """List all available routes."""
    return (
        f"Welcome to Climate Analysis<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
@app.route("/api/v1.0/precipitation")
def Precipitation():
    # Calculate the date one year from the last date in data set.
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    scores_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Save the query results as a Pandas DataFrame and set the index to the date column
    scores_df = pd.DataFrame(scores_data, columns=['date', 'precipitation'])

    #Sort the dataframe by date
    scores_df.set_index('date', inplace = True)
    scores_df = scores_df.sort_index()

    scores_dictionary = scores_df.to_dict()
    return jsonify(scores_dictionary)

@app.route("/api/v1.0/stations")
def Stations():

    all_stations = session.query(Station.station).all()
    
    all_stations_list = list(np.ravel(all_stations))
    return jsonify(all_stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    #create variable observations
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days = 365)

    observations = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter((Measurement.date >= one_year_ago)).all()

    observations_list = list(np.ravel(observations))
    return jsonify(observations_list)

@app.route("/api/v1.0/<start>")
def start():

    temperatures = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date > start).all()

    temperatures_list = list(np.ravel(temperatures))
    return jsonify(temperatures_list)

@app.route("/api/v1.0/<start>/<end>")
def stop():

    temperatures_start_stop = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date > start).filter(Measurement.date < stop).all()

    temperatures_start_stop_list = list(np.ravel(temperatures_start_stop))
    return jsonify(temperatures_start_stop_list)


if __name__ == "__main__":
    app.run(debug=True)