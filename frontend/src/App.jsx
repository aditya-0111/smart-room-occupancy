import { useEffect, useState } from "react"
import "./App.css"

function App() {
  const [sensorData, setSensorData] = useState(null)

 useEffect(() => {
  const fetchSensorData = () => {
    fetch("http://127.0.0.1:8000/sensor-data")
      .then((response) => response.json())
      .then((data) => {
        setSensorData(data[0])
      })
      .catch((error) => {
        console.error("Error fetching sensor data:", error)
      })
  }

  fetchSensorData()

  const interval = setInterval(fetchSensorData, 5000)

  return () => clearInterval(interval)
}, [])

  if (!sensorData) {
    return <h1>Loading sensor data...</h1>
  }
  let energyMode = ""
let energyMessage = ""

if (sensorData.occupancy === 1 && sensorData.pir_motion === 1) {
  energyMode = "Normal Mode"
  energyMessage = "Room occupied and motion detected"
} else if (sensorData.occupancy === 1 && sensorData.pir_motion === 0) {
  energyMode = "Monitoring Mode"
  energyMessage = "Room occupied but no motion detected"
} else {
  energyMode = "Energy Saving Mode"
  energyMessage = "Room appears empty"
}

return (
  <div className="dashboard">

    <div className="dashboard-header">
      <h1>Smart Room Occupancy Dashboard</h1>
      <p>Real-time room monitoring and occupancy prediction</p>
    </div>

    <div className="status-card">
      <h2>Room Status</h2>

      <div
        className={`status ${
          sensorData.occupancy === 1 ? "occupied" : "empty"
        }`}
      >
        {sensorData.occupancy === 1
          ? "🟢 Occupied"
          : "🔴 Empty"}
      </div>
    </div>

     <div className="status-card">
       <h2>⚡ Energy Management</h2>

     <div className="status">
       {energyMode}
      </div>

     <p>{energyMessage}</p>
    </div>

    <div className="cards">

      <div className="card">
        <div className="card-title">🌡️ Temperature</div>
        <div className="card-value">
          {sensorData.temperature} °C
        </div>
      </div>

      <div className="card">
        <div className="card-title">💧 Humidity</div>
        <div className="card-value">
          {sensorData.humidity} %
        </div>
      </div>

      <div className="card">
        <div className="card-title">💡 Light Level</div>
        <div className="card-value">
          {sensorData.light}
        </div>
      </div>

      <div className="card">
        <div className="card-title">🚶 Motion</div>
        <div className="card-value">
          {sensorData.pir_motion === 1
            ? "Detected"
            : "Not Detected"}
        </div>
      </div>

      <div className="card">
        <div className="card-title">🎯 ML Confidence</div>
        <div className="card-value">
          {sensorData.confidence * 100} %
        </div>
      </div>

    </div>

    <div className="last-updated">
      🕐 Last Updated: {sensorData.created_at}
    </div>

  </div>
)
}

export default App