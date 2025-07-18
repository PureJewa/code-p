# import serial
# import serial.tools.list_ports
#
# def find_adafruit_scanner():
#     # Zoek alle seriële poorten en probeer de Adafruit scanner te herkennen
#     ports = list(serial.tools.list_ports.comports())
#     for port in ports:
#         # Vaak herken je de scanner aan de naam, fabrikant of productomschrijving
#         if "" in port.description or "USB Serial Device" in port.description or "FTDI" in port.description:
#             print(f"Gevonden Adafruit scanner op: {port.device}")
#             return port.device
#     print("Adafruit scanner niet gevonden. Controleer verbinding.")
#     return None
#
# def main():
#     port_name = find_adafruit_scanner()
#     if port_name is None:
#         return
#
#     try:
#         while True:
#             input("Druk op Enter en scan de barcode...")
#             print("Wachten op barcode...")
#             # Probeer verbinding te maken met de poort
#             barcodeSer = serial.Serial(port_name, baudrate, timeout=5)
#             print(f"Verbonden met {port_name}. Wachten op gegevens...")
#
#             # Wachten op data van de scanner
#             barcodeData = barcodeSer.readline().decode('utf-8').strip()
#             barcodeSer.close()
#
#             if data:
#                 print(f"Barcode gescand op : {barcodeData}")
#                 return True
#             else:
#                 print(f"Geen gegevens ontvangen van .")
#     except Exception as e:
#         print("Fout bij : ")
#
#
# if __name__ == "__main__":
#     main()
# import serial
# import time
#
#
# def barcode_to_raspberry(port='COM9', baudrate=9600, timeout=5):
#     try:
#         # Maak verbinding met de scanner
#         with serial.Serial(port, baudrate, timeout=timeout) as barcodeSer:
#             print(f"Verbonden met {port}. Wacht op barcode scan...")
#
#             # Wacht tot gebruiker aangeeft dat scan start (optioneel)
#             input("Druk op Enter om te scannen...")
#
#             # Lees een regel barcode data
#             barcodeData = barcodeSer.readline().decode('utf-8').strip()
#
#             if barcodeData:
#                 print(f"Barcode gescand op {port}: {barcodeData}")
#                 return True
#             else:
#                 print(f"Geen barcode ontvangen op {port}. Probeer opnieuw.")
#                 return False
#     except serial.SerialException as e:
#         print(f"Fout bij verbinden met {port}: {e}")
#         return False
#     except Exception as e:
#         print(f"Onverwachte fout: {e}")
#         return False
#
#
# if __name__ == "__main__":
#     # Pas poort hier aan indien nodig
#     success = barcode_to_raspberry()
#     if not success:
#         print("Scan niet gelukt.")
import serial
import serial.tools.list_ports
def find_adafruit_scanner():
    # Zoek alle seriële poorten en probeer de Adafruit scanner te herkennen
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        # Vaak herken je de scanner aan de naam, fabrikant of productomschrijving
        if "Adafruit" in port.description or "" in port.description or "FTDI" in port.description:
            print(f"Gevonden Adafruit scanner op: {port.device}")
            return port.device
    print("Adafruit scanner niet gevonden. Controleer verbinding.")
    return None
#

def read_barcode():
    port = find_adafruit_scanner()
    # Open de seriële poort (pas de poortnaam aan als nodig)
    ser = serial.Serial('COM19', baudrate=9600, timeout=1)

    print("Wachten op barcode...")

    try:
        while True:
            if ser.in_waiting > 0:  # Controleer of er gegevens zijn
                data = ser.readline().decode('utf-8').strip()  # Lees de gegevens
                print(f"Barcode gescand: {data}")
    except KeyboardInterrupt:
        print("\nProgramma gestopt.")
    finally:
        ser.close()


if __name__ == "__main__":
    read_barcode()
