#import Flask
from flask import Flask, jsonify
import mumpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite://Resources/hawii.sqlite")

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
        
    )





if __name__ = "main":
    app.run(debug=True)