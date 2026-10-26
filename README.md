# Real-Time Smart Room Occupancy Detection and Energy Management Using Machine Learning

An IoT and machine learning project that uses ESP32-based sensors, a Random Forest classifier, FastAPI, MySQL, and a React dashboard to estimate room occupancy and monitor environmental conditions in real time.

## Overview

This project combines IoT hardware and machine learning to estimate whether a room is occupied based on temperature, light, and motion sensor readings.

The ESP32 collects sensor data and sends it to a FastAPI backend. The backend processes the readings, estimates occupancy using a trained Random Forest model, stores the results in MySQL, and provides data to a React dashboard.

The system also implements a 10-second no-motion timeout. If motion is not detected for the configured period, the backend marks the room as unoccupied.

## Key Features

- Real-time sensor monitoring: Collects temperature, light, and PIR motion readings through ESP32.
- Machine learning-based prediction: Uses a trained Random Forest classifier to estimate room occupancy.
- Automated occupancy timeout: Marks the room unoccupied after 10 seconds without detected motion.
- REST API: Provides FastAPI endpoints for health checks, occupancy prediction, and sensor data retrieval.
- Database integration: Stores sensor readings and occupancy results in MySQL.
- Web dashboard: Displays sensor readings and occupancy information through a React interface.
- Energy management status: Supports occupancy-based monitoring through software logic.

## System Architecture

```text
       Temperature Sensor (DHT22)
       Light Sensor (LDR - Digital)
       PIR Motion Sensor
                 |
                 v
               ESP32
                 |
                 | HTTP POST
                 v
          FastAPI Backend
                 |
          +------+------+
          |             |
          v             v
   Random Forest      MySQL
       Model         Database
          |
          v
   Occupancy Estimate
          |
          v
    React Dashboard
```

## Technology Stack

| Component                       | Technology                     |
| ------------------------------- | ------------------------------ |
| Microcontroller                 | ESP32                          |
| Temperature and humidity sensor | DHT22                          |
| Light sensor                    | LDR module with digital output |
| Motion sensor                   | PIR                            |
| Programming languages           | Python, C++                    |
| Machine learning                | Scikit-learn                   |
| ML algorithm                    | Random Forest Classifier       |
| Backend framework               | FastAPI                        |
| API server                      | Uvicorn                        |
| Database                        | MySQL                          |
| Frontend                        | React                          |
| Frontend tooling                | Vite                           |
| Embedded development            | Arduino IDE                    |
| Version control                 | Git and GitHub                 |

## Hardware Requirements

- ESP32 development board
- DHT22 temperature and humidity sensor
- LDR light sensor module with digital output
- PIR motion sensor
- Breadboard and jumper wires
- USB cable and computer
- Wi-Fi network

Note: Humidity is monitored and stored but is not currently used as an input to the machine learning model. The current implementation does not physically switch lights, fans, or other appliances.

## Software Requirements

- Python and pip
- Node.js and npm
- MySQL Server
- Arduino IDE
- Git
- A modern web browser

## Project Structure

```text
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
```

This tree shows the main project files. Additional files may exist within individual directories.

## Machine Learning Model

### Dataset

The project uses the Room Occupancy Estimation dataset.

- Original dataset: 10,129 observations
- Target variable: `Occupied`
- Target definition: Occupied when `Room_Occupancy_Count > 0`
- Input features: `Temperature`, `Light`, `PIR_Motion`

Humidity is excluded from the current model inputs.

### Data Preprocessing

The selected features are prepared for the Random Forest classifier. The light feature is converted to a binary value during preprocessing to align its representation with the ESP32's digital-output LDR module.

The dataset's original light measurements and the hardware's digital output may not have identical physical meanings. This is a limitation of the current implementation.

### Model Configuration

| Parameter                           | Value                    |
| ----------------------------------- | ------------------------ |
| Algorithm                           | Random Forest Classifier |
| Number of estimators                | 100                      |
| Random state                        | 42                       |
| Test samples in reported evaluation | 2,026                    |

### Model Evaluation Results

The following results are from the current notebook evaluation on the held-out test set.

| Metric    | Unoccupied (Class 0) | Occupied (Class 1) |
| --------- | -------------------: | -----------------: |
| Precision |                 0.98 |               0.93 |
| Recall    |                 0.98 |               0.90 |
| F1-score  |                 0.98 |               0.91 |
| Support   |                1,646 |                380 |

Overall accuracy: 96.79%

### Confusion Matrix

| Actual / Predicted | Unoccupied (0) | Occupied (1) |
| ------------------ | -------------: | -----------: |
| Unoccupied (0)     |          1,619 |           27 |
| Occupied (1)       |             38 |          342 |

These metrics describe performance on the notebook's held-out dataset. Actual performance with live sensor readings may differ.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/aditya-0111/smart-room-occupancy.git
cd smart-room-occupancy
```

### 2. Create a Python Virtual Environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the following command for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again.

### 3. Install Backend Dependencies

If the project contains `backend/requirements.txt`, run:

```powershell
pip install -r backend/requirements.txt
```

If that file does not exist, install the packages required by the current backend imports and model-loading code. Do not assume a dependency file exists if it has not been created.

### 4. Configure MySQL

Start MySQL Server and create the project database:

```sql
CREATE DATABASE smart_room;
```

Configure the database connection using the environment-variable names expected by `backend/main.py`.

Keep database credentials in a local `.env` file. Do not commit real passwords, secrets, or Wi-Fi credentials to GitHub.

### 5. Start the Backend

From the project root, activate the virtual environment and run:

```powershell
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend should be accessible at:

- Health check: `http://127.0.0.1:8000/`
- Interactive API documentation: `http://127.0.0.1:8000/docs`

### 6. Start the Frontend

Open another terminal from the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite, typically:

`http://localhost:5173/`

Ensure that the frontend API configuration points to the correct backend address.

## ESP32 Configuration

1. Open `esp32/smart_room_sensors/smart_room_sensors.ino` in Arduino IDE.
2. Install the required ESP32 board support and sensor libraries.
3. Configure your Wi-Fi credentials locally.
4. Set the backend URL to your computer's reachable LAN IP address.
5. Ensure that the ESP32 and computer can communicate over the network.
6. Select the correct board and serial port.
7. Upload the sketch and check the Serial Monitor for sensor readings and HTTP responses.

Do not use `localhost` as the backend address in ESP32 firmware. The ESP32 needs the computer's reachable LAN IP address.

### Sensor Pin Connections

| Component          | ESP32 GPIO |
| ------------------ | ---------: |
| DHT22 data         |     GPIO 4 |
| PIR motion output  |    GPIO 18 |
| LDR digital output |    GPIO 19 |

Check the voltage and wiring requirements of your specific sensor modules before connecting them.

## API Documentation

The current backend exposes the following endpoints.

| Method | Endpoint       | Purpose                                                        |
| ------ | -------------- | -------------------------------------------------------------- |
| `GET`  | `/`            | Check backend availability                                     |
| `POST` | `/predict`     | Process sensor readings, estimate occupancy, and store results |
| `GET`  | `/sensor-data` | Retrieve stored sensor readings                                |

### Example Prediction Request

```json
{
  "temperature": 26.5,
  "humidity": 55.0,
  "light": 1,
  "pir_motion": 1
}
```

The exact field names and data types must match the active backend implementation.

### Example Prediction Response

```json
{
  "occupancy": "Occupied",
  "prediction": 1,
  "model_prediction": 1,
  "confidence": 0.95
}
```

This is an illustrative response. The actual occupancy result and confidence value depend on the incoming readings and backend logic.

## Occupancy Detection Logic

The current system follows this process:

1. The ESP32 collects temperature, light, humidity, and motion readings.
2. The ESP32 sends the readings to the FastAPI backend.
3. The Random Forest model estimates occupancy using temperature, light, and PIR motion.
4. When PIR motion is detected, the backend updates the last-motion timestamp and marks the room occupied.
5. If no motion is detected for 10 seconds, the backend marks the room unoccupied.
6. Sensor readings and the final occupancy state are stored in MySQL.
7. The React dashboard retrieves and displays the latest data.

Important limitation: A PIR sensor may not detect someone who remains still. Therefore, the timeout-based occupancy status is an estimate and may not always reflect actual room presence. The in-memory motion timer also resets if the backend restarts.

## Energy Management

The project supports occupancy-based energy-status monitoring through software logic and the dashboard.

The current implementation does not physically switch lights, fans, or other electrical appliances. Physical control would require additional hardware and appropriate electrical safety measures.

## Testing and Verification

The following checks can be used to verify the system:

- [ ] ESP32 reads the connected sensors correctly.
- [ ] Sensor readings reach the FastAPI backend.
- [ ] The `/predict` endpoint returns an occupancy result.
- [ ] MySQL stores sensor readings and occupancy results.
- [ ] The `/sensor-data` endpoint returns stored records.
- [ ] The dashboard displays sensor readings and occupancy status.
- [ ] The 10-second no-motion timeout behaves as expected.
- [ ] The ML evaluation results are available in the notebook.

## Limitations

- Live prediction performance may differ from offline test results.
- PIR sensors may miss stationary occupants.
- The dataset's light measurements may differ from the LDR module's digital output.
- Humidity is monitored but is not an input to the current ML model.
- Energy management is currently software-level; physical appliance switching is not implemented.
- The motion timer is stored in backend memory and resets when the server restarts.
- Multi-room occupancy state is not implemented in the current configuration.

## Future Enhancements

- Add safe, hardware-based appliance control.
- Improve occupancy estimation using additional suitable sensor inputs.
- Add historical graphs and energy-consumption analytics.
- Support multiple rooms with independent occupancy states.
- Add configurable occupancy timeouts.
- Improve deployment security and monitoring.

## Author

Aditya Kumar

B.Tech — Electronics and Communication Engineering

GitHub: [aditya-0111](https://github.com/aditya-0111)

## License

No license has been specified for this project yet. Add an appropriate open-source license if you intend to permit others to reuse or redistribute the code.
