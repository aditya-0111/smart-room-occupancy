# Real-Time Smart Room Occupancy Detection and Energy Management Using Machine Learning



A smart-room monitoring system that uses ESP32-based sensors, a Random Forest machine learning model, FastAPI, MySQL, and a React dashboard to estimate room occupancy and monitor environmental conditions in real time.



## Overview



The project combines IoT hardware and machine learning to estimate whether a room is occupied based on temperature, light, and motion sensor readings. The system collects sensor data using an ESP32, sends it to a FastAPI backend, predicts occupancy, stores readings in MySQL, and displays the latest information on a web dashboard.



The backend also implements a 10-second no-motion timeout to mark the room as unoccupied when no motion is detected for the configured period.



## Key Features



\- \*\*Real-time sensor monitoring:\*\* Collects temperature, light, and PIR motion readings through ESP32.

\- \*\*Machine learning-based prediction:\*\* Uses a trained Random Forest classifier to estimate occupancy.

\- \*\*Automated occupancy timeout:\*\* Marks the room unoccupied after 10 seconds without detected motion.

\- \*\*REST API:\*\* FastAPI endpoints for health checks, occupancy prediction, and sensor data retrieval.

\- \*\*Database integration:\*\* Stores sensor readings and occupancy results in MySQL.

\- \*\*Web dashboard:\*\* React-based interface for viewing sensor readings and occupancy information.

\- \*\*Energy management status:\*\* Supports dashboard-level monitoring and occupancy-based status logic.



## System Architecture



```text

Temperature Sensor (DHT22)

Light Sensor (LDR - Digital Output)

PIR Motion Sensor

&#x20;         |

&#x20;         v

&#x20;       ESP32

&#x20;         |

&#x20;         | HTTP POST

&#x20;         v

&#x20;   FastAPI Backend

&#x20;         |

&#x20;         +------> Random Forest Model

&#x20;         |             |

&#x20;         |             v

&#x20;         |       Occupancy Estimate

&#x20;         |

&#x20;         +------> MySQL Database

&#x20;         |

&#x20;         v

&#x20;   React Dashboard

&#x20;         |

&#x20;         v

&#x20;Sensor Data and Occupancy Status

```



## Technology Stack



| Component | Technology |

|---|---|

| IoT hardware | ESP32 |

| Temperature and humidity | DHT22 |

| Light detection | LDR module with digital output |

| Motion detection | PIR sensor |

| Programming language | Python |

| Machine learning | Scikit-learn |

| ML algorithm | Random Forest Classifier |

| Backend framework | FastAPI |

| API server | Uvicorn |

| Database | MySQL |

| Database connectivity | Python MySQL connector |

| Frontend | React |

| Frontend tooling | Vite |

| Embedded programming | Arduino IDE / C++ |

| Version control | Git and GitHub |



## Hardware Requirements



\- ESP32 development board

\- DHT22 temperature and humidity sensor

\- LDR light sensor module with digital output

\- PIR motion sensor

\- Breadboard and jumper wires

\- USB cable and a computer

\- Wi-Fi network



\*\*Note:\*\* Humidity is collected for monitoring and storage but is not used as an input to the current machine learning model. The current implementation does not include a CO₂ sensor or physical appliance-switching hardware.



## Software Requirements



\- Python and pip

\- Node.js and npm

\- MySQL Server

\- Arduino IDE

\- Git

\- A compatible web browser



## Project Structure



```text

smart-room-occupancy/

│

├── backend/

│   ├── main.py

│   └── .env

│

├── data/

│   ├── Occupancy\_Estimation.csv

│   └── occupancy\_ml\_dataset.csv

│

├── docs/

│   └── Project\_Report.pdf

│

├── esp32/

│   └── smart\_room\_sensors/

│       └── smart\_room\_sensors.ino

│

├── frontend/

│   ├── src/

│   ├── package.json

│   └── vite.config.ts

│

├── ml/

│   ├── 01\_dataset\_analysis.ipynb

│   └── occupancy\_model.pkl

│

├── .gitignore

└── README.md

```



\*The structure above represents the main project files; individual folders may contain additional files.\*



## Machine Learning Model



### Dataset



The model uses the Room Occupancy Estimation dataset, stored in `data/Occupancy\_Estimation.csv`.



\- Original dataset size: 10,129 observations.

\- Target variable: `Occupied`.

\- Occupancy is defined as occupied when `Room\_Occupancy\_Count > 0`.

\- Selected model features: `Temperature`, `Light`, and `PIR\_Motion`.

\- Light readings are converted to binary values during preprocessing to align their representation with the digital light sensor used by the ESP32.



### Algorithm



The project uses a Random Forest Classifier with the following configuration:



\- Number of estimators: 100

\- Random state: 42

\- Evaluation: held-out test set

\- Metrics: accuracy, precision, recall, F1-score, and confusion matrix



### Model Evaluation Results



The current notebook evaluation produced the following results:



| Metric | Result |

|---|---:|

| Accuracy | 96.79% |

| Unoccupied precision | 0.98 |

| Unoccupied recall | 0.98 |

| Occupied precision | 0.93 |

| Occupied recall | 0.90 |

| Occupied F1-score | 0.91 |

| Test samples | 2,026 |



Confusion matrix:



```text

&#x20;                Predicted

&#x20;                0       1

Actual 0       1619     27

Actual 1         38    342

```



These results correspond to the evaluation shown in the project notebook. They measure performance on the held-out dataset and do not guarantee identical accuracy with live sensor readings.



## Backend Setup



### 1. Clone the Repository



```bash

git clone https://github.com/aditya-0111/smart-room-occupancy.git

cd smart-room-occupancy

```



### 2. Create and Activate a Virtual Environment



On Windows PowerShell:



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

```



### 3. Install Backend Dependencies



Install the dependencies used by your backend, including FastAPI, Uvicorn, scikit-learn, pandas, joblib if required by the model-loading code, python-dotenv, and the MySQL connector.



If a `backend/requirements.txt` file is available, use:



```powershell

pip install -r backend/requirements.txt

```



Otherwise, install the packages listed in your backend imports and model-loading requirements.



### 4. Configure Environment Variables



Create `backend/.env` and configure the database connection and other required settings.



```env

PORT=8000

MONGO\_URI=

JWT\_SECRET=

JWT\_EXPIRES\_IN=

OTP\_EXPIRY\_SECONDS=

CLIENT\_ORIGIN=http://localhost:5173



DB\_HOST=localhost

DB\_USER=your\_mysql\_username

DB\_PASSWORD=your\_mysql\_password

DB\_NAME=smart\_room

```



Use the exact database variable names expected by your current backend code. The MongoDB and authentication variables are only needed if they are used by the active implementation; they are not required for the described MySQL occupancy pipeline.



\*\*Security:\*\* Never commit real passwords, API secrets, or Wi-Fi credentials to GitHub.



### 5. Prepare the MySQL Database



Create the database if it does not already exist:



```sql

CREATE DATABASE smart\_room;

```



Ensure that the sensor table and its columns match the schema expected by `backend/main.py`.



### 6. Start the Backend



```powershell

cd backend

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```



Backend health check:



\- `http://127.0.0.1:8000/`



Interactive API documentation:



\- `http://127.0.0.1:8000/docs`



## Frontend Setup



Open a separate terminal from the project root:



```powershell

cd frontend

npm install

npm run dev

```



Open the local URL printed by Vite, typically:



`http://localhost:5173/`



Ensure the frontend API configuration points to the correct backend address. The browser-based dashboard normally uses `http://127.0.0.1:8000` when both services run on the same computer.



## ESP32 Setup



1\. Open `esp32/smart\_room\_sensors/smart\_room\_sensors.ino` in Arduino IDE.

2\. Install the required ESP32 board support and sensor libraries.

3\. Configure your local Wi-Fi credentials.

4\. Set the backend IP address to your computer's LAN IP address.

5\. Confirm that the ESP32, computer, and backend can communicate over the same network.

6\. Select the correct ESP32 board and serial port.

7\. Upload the sketch and open the Serial Monitor to check sensor readings and HTTP responses.



The current firmware uses these sensor connections:



| Component | ESP32 GPIO |

|---|---:|

| DHT22 data | GPIO 4 |

| PIR motion output | GPIO 18 |

| LDR digital output | GPIO 19 |



Use the correct voltage and wiring specifications for your sensor modules. Do not use `localhost` as the backend address in ESP32 firmware; it must use the computer's reachable LAN IP.



## API Endpoints



| Method | Endpoint | Purpose |

|---|---|---|

| GET | `/` | Check backend availability |

| POST | `/predict` | Receive sensor readings, estimate occupancy, and store results |

| GET | `/sensor-data` | Retrieve stored sensor readings |



### Example Prediction Request



```json

{

&#x20; "temperature": 26.5,

&#x20; "humidity": 55.0,

&#x20; "light": 1,

&#x20; "pir\_motion": 1

}

```



The exact JSON field names and data types must match the active backend implementation.



### Example Response



```json

{

&#x20; "occupancy": "Occupied",

&#x20; "prediction": 1,

&#x20; "model\_prediction": 1,

&#x20; "confidence": 0.95

}

```



This is an illustrative response. Actual confidence and prediction values depend on the incoming readings and the backend implementation.



## Occupancy Logic



The system combines machine learning predictions with a motion-based timeout:



1\. The ESP32 reads temperature, light, and PIR motion.

2\. The backend passes the model features to the Random Forest classifier.

3\. When motion is detected, the backend records the latest motion time and marks the room occupied.

4\. If no further motion is detected for 10 seconds, the backend marks the room unoccupied.

5\. The sensor readings and final occupancy state are stored in MySQL.

6\. The React dashboard retrieves and displays the latest data.



\*\*Limitation:\*\* A PIR sensor may not detect a person who remains completely still. Therefore, the timeout-based status is an estimate and may not always reflect the actual presence of a person.



## Energy Management



The project uses occupancy status to support energy-management monitoring. The dashboard can show whether the room is occupied or unoccupied and represent the corresponding energy mode.



The current implementation provides software-level monitoring and status logic. It does not physically switch lights, fans, or other appliances.



## Testing and Verification



The following checks are relevant to validating the current system:



\- \[ ] ESP32 reads temperature, light, and motion sensor values.

\- \[ ] ESP32 sends readings successfully to the FastAPI backend.

\- \[ ] The `/predict` endpoint returns an occupancy result.

\- \[ ] MySQL stores sensor readings and occupancy results.

\- \[ ] The `/sensor-data` endpoint returns stored records.

\- \[ ] The dashboard displays updated sensor readings and occupancy status.

\- \[ ] The 10-second no-motion timeout behaves as expected.

\- \[ ] The model evaluation results are available in the notebook.



## Limitations



\- Occupancy detection depends on the available sensors and their placement.

\- PIR sensors may miss stationary occupants.

\- The model was evaluated on a prepared dataset; live sensor performance can differ.

\- The digital LDR module and the dataset's original light measurements may have different semantics despite binary preprocessing.

\- Humidity is monitored but is not a model input.

\- The current energy-management implementation does not perform physical appliance control.

\- The backend's in-memory motion timer resets when the server restarts and is not designed for multiple independent rooms without additional state management.



## Future Enhancements



\- Add physical appliance control through a suitable relay and safe electrical interface.

\- Improve occupancy detection by combining additional appropriate sensors.

\- Add historical graphs and energy-consumption analytics.

\- Support multiple rooms and persistent room-specific occupancy state.

\- Add configurable occupancy timeout settings.

\- Improve deployment security, authentication, and monitoring.



## Author



\*\*Aditya Kumar\*\*



B.Tech — Electronics and Communication Engineering



GitHub: \[aditya-0111](https://github.com/aditya-0111)



## License



No license has been specified yet. If you intend to allow others to reuse this project, add an appropriate open-source license.




