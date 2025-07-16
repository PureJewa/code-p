import serial
import time
def Arduino_to_raspberry():
    try:
        arduinoSer = serial.Serial('/dev/ttyACM1', baudrate=9600, timeout=2)  # Pas poortnaam aan
        print("Verbinding geopend met Arduino.")
        time.sleep(2)  # Wacht op Arduino-opstart

        while True:
            if arduinoSer.in_waiting > 0:
                arduinoData = arduinoSer.readline().decode('utf-8').strip()
                print(f"Ontvangen van Arduino: {arduinoData}")

                if arduinoData == "Barcode":
                    print("Barcode ontvangen!")
                    arduinoSer.write("Copy\n".encode('utf-8'))
                elif arduinoData == "Programeer":
                    print("Progameer opdracht ontvangen!")
                    arduinoSer.write("Copy\n".encode('utf-8'))
            else:
                print("Wachten op data...")
                time.sleep(1)
    except Exception as e:
        print(f"Fout: {e}")
    finally:
        arduinoSer.close()
        print("Verbinding gesloten.")
Arduino_to_raspberry()