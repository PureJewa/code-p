import serial

from usbcomtest import Prog_Diver

global serial_number
global aantal_sensors
def readBarcode():
    try:
        portScanner = '/dev/ttyACM2'
        # Probeer verbinding te maken met de poort
        ser = serial.Serial(portScanner, baudrate=9600, timeout=1)
        print(f"Verbonden met {portScanner}. Wachten op gegevens...")

        # Wachten op data van de scanner
        data = ser.readline().decode('utf-8').strip()
        ser.close()

        if data:
            print(f"Barcode gescand op {portScanner}: {data}")
            return True
        else:
            print(f"Geen gegevens ontvangen van {portScanner}.")
    except Exception as e:
        print(f"Fout bij {portScanner}: {e}")
    return False

def raspberry_to_arduino():
    try:
        """ 
        # Open seriele verbinding met Arduino
        serARD = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
        time.sleep(2)  # Wacht tot Arduino klaar is
        print("Verbonden met Arduino!")
"""
        while True:
            # Lees data van de Arduino
            if serARD.in_waiting > 0:
                data = serARD.readline().decode('utf-8').strip()
                print(f"Arduino: {data}")
                if data == 'Barcode':
                 try :
                     readBarcode()
                     message2 = "Copy"
                     serARD.write(message2.encode('utf-8'))
                     print(message2)
                 finally:
                    #ser.close()
                    message = 'thanks'
                    serARD.write(message.encode('utf-8'))

                if data == 'Programeer':
                 try:
                     Prog_Diver(serial_number, aantal_sensors)

                 finally:
                    #ser.close()
                    message = 'thanks'
                    serARD.write(message.encode('utf-8'))

    except serial.SerialException as e:
        print(f"Verbindingsfout: {e}")
    except KeyboardInterrupt:
        print("Programma gestopt door gebruiker.")
    finally:

        print("Seriele poort gesloten.")
raspberry_to_arduino()