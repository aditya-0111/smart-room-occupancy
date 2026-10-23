
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import joblib
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("MySQL connected successfully!")

app = FastAPI(title="Smart Room Occupancy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("../ml/occupancy_model.pkl")

print("Updated Random Forest model loaded successfully!")
print("Model features:", model.feature_names_in_)

# Occupancy timeout settings
NO_MOTION_TIMEOUT = timedelta(seconds=10)
last_motion_time = None
current_occupancy = None


class SensorData(BaseModel):
    temperature: float
    humidity: float
    light: float
    pir_motion: int


@app.get("/")
def home():
    return {"message": "Smart Room Occupancy API is running"}


@app.post("/predict")
def predict_occupancy(data: SensorData):
    global last_motion_time, current_occupancy

    features = pd.DataFrame(
        [[data.temperature, data.light, data.pir_motion]],
        columns=["Temperature", "Light", "PIR_Motion"]
    )

    model_prediction = int(model.predict(features)[0])
    probability = model.predict_proba(features)[0]
    confidence = float(probability[model_prediction])

    now = datetime.now()

    if data.pir_motion == 1:
        last_motion_time = now
        current_occupancy = 1
    else:
        if last_motion_time is None:
            last_motion_time = now

        if current_occupancy is None:
            current_occupancy = model_prediction

        if now - last_motion_time >= NO_MOTION_TIMEOUT:
            current_occupancy = 0

    occupancy = "Occupied" if current_occupancy == 1 else "Empty"

    cursor = db.cursor()
    try:
        query = """
            INSERT INTO sensor_data
            (temperature, humidity, light, pir_motion, occupancy, confidence)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            data.temperature,
            data.humidity,
            data.light,
            data.pir_motion,
            current_occupancy,
            confidence
        )

        cursor.execute(query, values)
        db.commit()
    finally:
        cursor.close()

    return {
        "occupancy": occupancy,
        "prediction": current_occupancy,
        "model_prediction": model_prediction,
        "confidence": confidence
    }


@app.get("/sensor-data")
def get_sensor_data():
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT *
            FROM sensor_data
            ORDER BY created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()