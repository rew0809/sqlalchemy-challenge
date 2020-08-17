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
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Available api routes:"""
    return (
        f"Welcome to the Rob's Homework API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/end/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Daily Precipitation Amounts"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23')
    
    session.close()

    # Convert results to dict and jsonify
    daily_prcp = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        daily_prcp.append(precip_dict)


    return jsonify(daily_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Unique Station List"""
    # Query all passengers
    results = session.query(Measurement.station).distinct().all()

    session.close()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Daily Temps at Most Active Station - USC00519281"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').filter(Measurement.station == 'USC00519281').all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/start/<start>")
def temp_stats_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs) ).\
        filter(Measurement.date == start).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/start/end/<start>/<end>")
def temp_stats_start_end(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
