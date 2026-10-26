Smart Room Occupancy Detection and Energy Management

An IoT and Machine Learning Project

A real-time room monitoring system that combines ESP32 sensors, a Random Forest classifier, FastAPI, MySQL, and a React dashboard to estimate room occupancy and monitor environmental conditions.

Overview

The system collects temperature, light, and motion readings from an ESP32. A FastAPI backend processes the sensor data, estimates occupancy using a trained Random Forest model, stores readings in MySQL, and provides data to a web dashboard.

A 10-second no-motion timeout is implemented to mark the room as unoccupied when motion is no longer detected within the configured period.

Key Features

Real-time monitoring: Collects temperature, light, and PIR motion readings.

ML-based occupancy estimation: Uses a trained Random Forest classifier.

Occupancy timeout: Marks the room unoccupied after 10 seconds without detected motion.

REST API: Provides health-check, prediction, and sensor-data endpoints.

MySQL integration: Stores sensor readings and occupancy results.

Web dashboard: Displays sensor information and occupancy status.

Energy-management status: Supports occupancy-based monitoring through software logic.

System Architecture

DHT22 + LDR + PIR Sensors
           |
           v
          ESP32
           |
           | HTTP POST
           v
     FastAPI Backend
           |
           +------> Random Forest Model
           |                 |
           |                 v
           |          Occupancy Estimate
           |
           +------> MySQL Database
           |
           v
     React Dashboard

Technology Stack

Layer

Technology

Microcontroller

ESP32

Temperature and humidity

DHT22

Light detection

LDR digital-output module

Motion detection

PIR sensor

Programming

Python, C++

Machine learning

Scikit-learn

ML algorithm

Random Forest Classifier

Backend

FastAPI, Uvicorn

Database

MySQL

Frontend

React, Vite

Embedded development

Arduino IDE

Version control

Git, GitHub

Hardware Requirements

ESP32 development board

DHT22 temperature and humidity sensor

LDR module with digital output

PIR motion sensor

Breadboard and jumper wires

USB cable and computer

Wi-Fi network

Note: Humidity is monitored but is not currently used as an ML input. The project does not currently implement physical appliance switching.

Project Structure

smart-room-occupancy/
├── backend/
│   ├── main.py
│   └── .env
├── data/
│   ├── Occupancy_Estimation.csv
│   └── occupancy_ml_dataset.csv
├── docs/
│   └── Project_Report.pdf
├── esp32/
│   └── smart_room_sensors/
│       └── smart_room_sensors.ino
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── ml/
│   ├── 01_dataset_analysis.ipynb
│   └── occupancy_model.pkl
├── .gitignore
└── README.md

This shows the main project files; additional files may exist in individual folders.

Machine Learning

The model uses the Room Occupancy Estimation dataset.

Original dataset: 10,129 observations

Target: Occupied

Target definition: Occupied when Room_Occupancy_Count > 0

Input features: Temperature, Light, PIR_Motion

Algorithm: Random Forest Classifier

Number of estimators: 100

Random state: 42

The light feature is converted to a binary value during preprocessing to align its representation with the digital-output LDR module. The sensor's digital output and the original dataset's light measurements may not have identical physical meanings.

Evaluation Results

The following results are from the current notebook evaluation on 2,026 test samples.

Metric

Unoccupied (0)

Occupied (1)

Precision

0.98

0.93

Recall

0.98

0.90

F1-score

0.98

0.91

Support

1,646

380

Overall accuracy: 96.79%

Confusion matrix:

Actual / Predicted

Unoccupied (0)

Occupied (1)

Unoccupied (0)

1,619

27

Occupied (1)

38

342

These results describe the notebook's held-out test set. Live sensor performance may differ.

Backend Setup

1. Clone the repository

git clone https://github.com/aditya-0111/smart-room-occupancy.git
cd smart-room-occupancy

2. Create a Python virtual environment

On Windows PowerShell:

python -m venv venv
.\venv\Scripts\Activate.ps1

3. Install dependencies

If backend/requirements.txt exists:

pip install -r backend/requirements.txt

Otherwise, install the dependencies required by your backend imports and model-loading code.

4. Configure MySQL

Create the database:

CREATE DATABASE smart_room;

Configure your MySQL connection using the environment-variable names expected by backend/main.py. Keep credentials in a local .env file and out of GitHub.

5. Start the backend

cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

API health check: http://127.0.0.1:8000/

Interactive API documentation: http://127.0.0.1:8000/docs

Frontend Setup

Open another terminal from the project root:

cd frontend
npm install
npm run dev

Open the local URL shown by Vite, usually http://localhost:5173/.

Ensure the frontend API base URL points to the correct backend address.

ESP32 Setup

Open esp32/smart_room_sensors/smart_room_sensors.ino in Arduino IDE.

Install the required ESP32 board support and sensor libraries.

Configure your local Wi-Fi credentials.

Set the backend URL to your computer's reachable LAN IP address.

Connect the ESP32 and computer to a network that allows communication between them.

Select the correct board and serial port, then upload the sketch.

Check the Serial Monitor for sensor readings and HTTP responses.

Sensor Connections

Component

ESP32 GPIO

DHT22 data

GPIO 4

PIR output

GPIO 18

LDR digital output

GPIO 19

Check your sensor modules' voltage and wiring requirements before connecting them.

API Endpoints

Method

Endpoint

Purpose

GET

/

Backend health check

POST

/predict

Process readings, estimate occupancy, and store results

GET

/sensor-data

Retrieve stored sensor readings

Example Request

{
  "temperature": 26.5,
  "humidity": 55.0,
  "light": 1,
  "pir_motion": 1
}

The request fields must match the active backend implementation.

Example Response

{
  "occupancy": "Occupied",
  "prediction": 1,
  "model_prediction": 1,
  "confidence": 0.95
}

The response is illustrative; actual predictions and confidence values depend on the sensor readings and backend logic.

Occupancy Logic

The ESP32 collects sensor readings.

Readings are sent to the FastAPI backend.

The Random Forest model estimates occupancy.

Detected PIR motion updates the last-motion timestamp and marks the room occupied.

If no motion is detected for 10 seconds, the backend marks the room unoccupied.

Readings and the final occupancy state are stored in MySQL.

The dashboard retrieves and displays the data.

Limitation: A PIR sensor may not detect someone who remains still. The timeout-based status is an estimate, not a guarantee of actual room occupancy.

Energy Management

The system supports occupancy-based energy-status monitoring in software. Physical switching of lights, fans, or other appliances is not currently implemented.

Verification Checklist

ESP32 reads the connected sensors.

Sensor readings reach the FastAPI backend.

The prediction endpoint returns an occupancy result.

MySQL stores sensor readings and occupancy results.

The sensor-data endpoint returns stored records.

The dashboard displays updated readings and occupancy status.

The 10-second timeout behaves as expected.

Limitations

Live prediction performance may differ from offline test results.

PIR sensors may miss stationary occupants.

Binary LDR values may not be semantically equivalent to the original dataset's light measurements.

Humidity is monitored but is not used by the current ML model.

Energy management is software-level; physical appliance control is not implemented.

The current motion timer is held in backend memory and resets when the server restarts.

Future Improvements

Add safe, hardware-based appliance control.

Improve occupancy detection using additional sensor inputs.

Add historical visualizations and energy-consumption analytics.

Support multiple rooms with independent occupancy states.

Add configurable timeouts and deployment security improvements.

Author

Aditya Kumar

B.Tech, Electronics and Communication Engineering

GitHub: aditya-0111

License

No license has been specified. Add an open-source license if you intend to permit reuse or redistribution.