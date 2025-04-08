import serial
def read_rfid():
    try:
        #ser = serial.Serial('/dev/ttyUSB0', 9600)
        #if ser.in_waiting > 0:
        #    return ser.readline().decode('utf-8').strip()

        # Simulate RFID reading
        rfid_datas = ["RFID_TAG_12345", "RFID_TAG_67890", "RFID_TAG_54321", "RFID_TAG_09876", "RFID_TAG_11223", "RFID_TAG_44556", "RFID_TAG_77889", "RFID_TAG_99000", "RFID_TAG_12321", "RFID_TAG_45654", "RFID_TAG_78987"]
        print("Enter RFID tag index:")  # Changed the prompt to be clearer
        while True:
            rfid_index_str = input()
            try:
                rfid_index = int(rfid_index_str)
                if rfid_index < len(rfid_datas):
                    return rfid_datas[rfid_index]
                else:
                    print("Invalid RFID tag index. Please enter a number within the valid range.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    return None