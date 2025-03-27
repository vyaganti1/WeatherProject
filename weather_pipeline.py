import requests
import pandas as pd
import sqlite3
from datetime import datetime

# API setup
API_KEY = "{API_KEY}"  # Replace with your OpenWeatherMap API key
CITY = input("Enter city name separated by commas (e.g., New York, London, Tokyo): ")
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

# Step 1: Fetch data
response = requests.get(URL)
data = response.json()

# Step 2: Extract and transform data
weather_data = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "city": CITY,
    "temperature_c": round(data["main"]["temp"] - 273.15, 2),  # Convert Kelvin to Celsius
    "humidity": data["main"]["humidity"],
    "wind_speed": data["wind"]["speed"]
}

# Step 3: Load into Pandas DataFrame
df = pd.DataFrame([weather_data])
print("Processed Data:")
print(df)

# Step 4: Save to SQLite
conn = sqlite3.connect("weather_data.db")
df.to_sql("weather", conn, if_exists="append", index=False)
conn.close()

# Optional: Save to CSV
df.to_csv("weather_data.csv", mode="a", header=not pd.io.common.file_exists("weather_data.csv"), index=False)

print("Data saved successfully!")
