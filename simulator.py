import pandas as pd
import requests
import time

CSV_FILE = 'intelligent_indoor_environment_dataset.csv'
API_URL = 'http://localhost:5000/api/ingest'
REAL_DELAY = 1

def start_simulation():
    print(f"--- Loading dataset: {CSV_FILE} ---")
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print(f"Can't find the file {CSV_FILE}")
        return

    print("--- START DEMO (Smart Ventilation) ---")

    for index, row in df.iterrows():
        payload = {
            "timestamp": str(row['timestamp']),
            "temp": float(row['room_temperature']),
            "hum": float(row['room_humidity']),
            "co2": float(row['room_CO2']),
            "people": int(row['room_occupancy']),
            "power": float(row['energy_consumption']) * 1000,
            "hvac": float(row['HVAC_temperature']),
            "cost": float(row['energy_cost']),
            "is_eco": int(row['energy_efficiency']),
            "lux": float(row['lighting_intensity']),
            "dimmer": float(row['lighting_control']),
            "fan_speed": float(row['air_quality_control']) 
        }

        try:
            requests.post(API_URL, json=payload)
            print(f"Fan: {payload['fan_speed']:.0f}% | CO2: {payload['co2']:.0f}")
        except:
            print("Backend offline")
        
        time.sleep(REAL_DELAY)

if __name__ == "__main__":
    start_simulation()