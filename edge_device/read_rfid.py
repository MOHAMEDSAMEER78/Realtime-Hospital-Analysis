import serial
def read_rfid():
    try:
        #ser = serial.Serial('/dev/ttyUSB0', 9600)
        #if ser.in_waiting > 0:
        #    return ser.readline().decode('utf-8').strip()

        # Simulate RFID reading
        return "RFID_TAG_12345"  # Placeholder for actual RFID reading
        
    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    return None