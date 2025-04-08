import requests
import time
from read_sensors import read_sensors
from read_rfid import read_rfid

FOG_API_URL = "http://127.0.0.1:8000/data_aggregator/receive_data/" # Replace with actual Fog URL

def send_data_to_fog(data):
    try:
        response = requests.post(FOG_API_URL, json=data)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print("Data sent to Fog successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Fog: {e}")

def main():
    while True:
        rfid_tag = read_rfid()
        sensor_data = read_sensors()
        if rfid_tag or sensor_data:
            data = {
                "rfid_tag": rfid_tag,
                "temperature": sensor_data.get("temperature"),
                "heart_rate": sensor_data.get("heart_rate")
            }
            print(data)
            send_data_to_fog(data)
        time.sleep(5)

if __name__ == "__main__":
    main()