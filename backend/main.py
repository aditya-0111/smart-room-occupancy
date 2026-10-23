
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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
    features = pd.DataFrame(
        [[data.temperature, data.light, data.pir_motion]],
        columns=["Temperature", "Light", "PIR_Motion"]
    )

    prediction = int(model.predict(features)[0])
    probability = model.predict_proba(features)[0]

    occupancy = "Occupied" if prediction == 1 else "Empty"
    confidence = float(probability[prediction])

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
            prediction,
            confidence
        )

        cursor.execute(query, values)
        db.commit()
    finally:
        cursor.close()

    return {
        "occupancy": occupancy,
        "prediction": prediction,
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
        data = cursor.fetchall()
        return data
    finally:
        cursor.close()
