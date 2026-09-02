import { useEffect, useState } from "react"

function App() {
  const [sensorData, setSensorData] = useState(null)

  useEffect(() => {
    fetch("http://127.0.0.1:8000/sensor-data")
      .then((response) => response.json())
      .then((data) => {
        setSensorData(data[0])
      })
      .catch((error) => {
        console.error("Error fetching sensor data:", error)
      })
  }, [])

  if (!sensorData) {
    return <h1>Loading sensor data...</h1>
  }

  return (
    <div>
      <h1>Smart Room Occupancy Dashboard</h1>

      <div>
        <h2>Room Status</h2>
        <p>
          Occupancy:{" "}
          {sensorData.occupancy === 1 ? "Occupied" : "Empty"}
        </p>
        <p>Temperature: {sensorData.temperature} °C</p>
        <p>Humidity: {sensorData.humidity} %</p>
        <p>Light: {sensorData.light}</p>
        <p>
          Motion: {sensorData.pir_motion === 1 ? "Detected" : "Not Detected"}
        </p>
        <p>Confidence: {sensorData.confidence * 100} %</p>
      </div>
    </div>
  )
}

export default App
