#include <WiFi.h>
#include <DHT.h>
#include <HTTPClient.h>

// Wi-Fi credentials
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// FastAPI endpoint: update this if your computer's IP changes
const char* serverUrl = "http://192.168.43.167:8000/predict";

// Sensor pin assignments
#define DHT_PIN 4
#define DHT_TYPE DHT22
#define PIR_PIN 18
#define LDR_PIN 19

DHT dht(DHT_PIN, DHT_TYPE);

void connectToWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to Wi-Fi");

  int attempts = 0;

  while (WiFi.status() != WL_CONNECTED && attempts < 40) {
    delay(500);
Serial.print(".");
Serial.print(" Status: ");
Serial.println(WiFi.status());
    attempts++;
  }

  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("Wi-Fi connected successfully!");
    Serial.print("ESP32 IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.print("Wi-Fi connection failed. Status code: ");
    Serial.println(WiFi.status());
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(PIR_PIN, INPUT);
  pinMode(LDR_PIN, INPUT);
  dht.begin();

  Serial.println();
  Serial.println("ESP32 Sensor Monitoring Started");
  Serial.println("--------------------------------");

  connectToWiFi();

  Serial.println("--------------------------------");
  delay(2000);
}

void loop() {
  // Reconnect if Wi-Fi is disconnected
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi disconnected. Retrying...");
    WiFi.disconnect();
    connectToWiFi();
  }

  // Read sensors
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  int motion = digitalRead(PIR_PIN);
  int lightState = digitalRead(LDR_PIN);

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("DHT22: Reading failed!");
    delay(5000);
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("Motion: ");
  Serial.println(motion == HIGH ? "DETECTED" : "Not detected");

  Serial.print("LDR digital output: ");
  Serial.println(lightState == HIGH ? "HIGH" : "LOW");

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.setConnectTimeout(5000);
    http.setTimeout(5000);

    if (http.begin(serverUrl)) {
      http.addHeader("Content-Type", "application/json");

      // Digital LDR output mapped to 0 or 1.
      // This is not a calibrated light measurement.
      int lightValue = (lightState == HIGH) ? 1 : 0;

      String json = "{";
      json += "\"temperature\":" + String(temperature, 2) + ",";
      json += "\"humidity\":" + String(humidity, 2) + ",";
      json += "\"light\":" + String(lightValue) + ",";
      json += "\"pir_motion\":" + String(motion == HIGH ? 1 : 0);
      json += "}";

      Serial.println("Sending data to FastAPI:");
      Serial.println(json);

      int httpResponseCode = http.POST(json);

      Serial.print("HTTP response code: ");
      Serial.println(httpResponseCode);

      if (httpResponseCode > 0) {
        Serial.println("API response:");
        Serial.println(http.getString());
      } else {
        Serial.println("FastAPI request failed.");
        Serial.println(http.errorToString(httpResponseCode));
      }

      http.end();
    } else {
      Serial.println("Could not initialize HTTP connection.");
    }
  } else {
    Serial.println("Wi-Fi unavailable; data not sent.");
  }

  Serial.println("--------------------------------");
  delay(5000);
}