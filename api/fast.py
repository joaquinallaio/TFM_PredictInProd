from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pytz
from TaxiFareModel.params import PATH_TO_LOCAL_MODEL
from predict import get_model
from datetime import datetime
import pytest as pyts




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],)  # Allows all headers

@app.get("/")
def index():
    return {"greeting": "Hello world"}

@app.get("/predict")
def predict(pickup_datetime,
pickup_longitude,
pickup_latitude,
dropoff_longitude,
dropoff_latitude,
passenger_count):

       # create a datetime object from the user provided datetime
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")

    # localize the user datetime with NYC timezone
    localized_pickup_datetime = pytz.timezone("US/Eastern").localize(pickup_datetime, is_dst=None)

    X_pred = pd.DataFrame({
        "key": [localized_pickup_datetime.astimezone(pytz.utc).strftime("%Y-%m-%d %H:%M:%S UTC")],
        "pickup_datetime": [localized_pickup_datetime],
        "pickup_longitude": [pickup_longitude],
        "pickup_latitude": [pickup_latitude],
        "dropoff_longitude": [dropoff_longitude],
        "dropoff_latitude": [dropoff_latitude],
        "passenger_count": [passenger_count]})

    model = get_model(PATH_TO_LOCAL_MODEL)

    pred = model.predict(X_pred)

    print(pred)

    return {'fare_amount': pred[0]}

"""key                     object
pickup_datetime         object
pickup_longitude        float64
pickup_latitude         float64
dropoff_longitude       float64
dropoff_latitude        float64
passenger_count         int64"""
