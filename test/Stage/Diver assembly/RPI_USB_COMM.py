import serial
import time
from Globals import *


def Prog_Diver(startSerieNummer, aantalSensoren):

    try:
        readUnitSer = serial.Serial(ReadingUnitPort, baudrate, timeout)
        current_serial = startSerieNummer
        for _ in range(aantalSensoren):
            print(f"Programmeren van apparaat met serienummer: {current_serial}")
            command = create_command(current_serial)
            send_command(readUnitSer, command)
            response = read_response(readUnitSer, 2)
            print(f"Respons: {response if response else 'Geen respons'}")
            # Voeg het huidige serienummer toe en increment
            serieNummerLijst.append(current_serial)
            current_serial = increment_serial_number(current_serial)

    except Exception as e:
        print(f"Fout: {e}")
    return True
def Diver_Read_Unit_to_raspberry():
    global result
    try:
            readUnitSer = serial.Serial(ReadingUnitPort, baudrate, timeout)
            # Lees het serienummer
            send_command(readUnitSer, COMMAND_SERIAL)
            serial_response = read_response(readUnitSer, timeout)
            if serial_response and "-" in serial_response:
                result["serial_number"] = serial_response.split("-")[1][:5]

            # Lees druk en temperatuur
            send_command(readUnitSer, COMMAND_PRESSURE)
            pressure_response = read_response(readUnitSer, timeout)
            if pressure_response:
                if "G28" in pressure_response:
                    result["pressure_value"] = pressure_response[5:12]
                    result["temperature_value"] = pressure_response[15:22]

    except Exception as e:
        print(f"Fout bij seriele communicatie: {e}")
def Barcode_to_raspberry():
    try:
        # Probeer verbinding te maken met de poort
        barcodeSer = serial.Serial(ScannerPort, baudrate, timeout)
        print(f"Verbonden met {portScanner}. Wachten op gegevens...")

        # Wachten op data van de scanner
        barcodeData = barcodeSer.readline().decode('utf-8').strip()
        barcodeSer.close()

        if data:
            print(f"Barcode gescand op {ScannerPort}: {barcodeData}")
            return True
        else:
            print(f"Geen gegevens ontvangen van {ScannerPort}.")
    except Exception as e:
        print(f"Fout bij {ScannerPort}: {e}")


def create_command(serienummer):
    """
    Cre�ert een commando dat naar het apparaat gestuurd kan worden.

    Args:
        serienummer (str): Het serienummer dat geprogrammeerd moet worden.

    Returns:
        bytes: Het commando dat verstuurd moet worden.
    """
    serienummer_bytes = serienummer.encode()  # Converteer naar bytes
    base_command = (
        b'\x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D'
        + serienummer_bytes
        + b'\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03'
    )
    checksum = calculate_checksum(base_command)
    return base_command + bytes([checksum]) + b'\xA0'
def send_command(readUnitSer, command):
    """
    Stuurt een commando naar het apparaat via de seriele verbinding.

    Args:
        serial_conn: De seriele verbinding.
        command (bytes): Het commando dat gestuurd moet worden.
    """
    readUnitSer.write(command)
    readUnitSer.flush()


def read_response(readUnitSer, duration):
    """
    Leest de respons van het apparaat via de seriele verbinding.

    Args:
        serial_conn: De seriele verbinding.
        duration (float): De maximale tijd in seconden om te wachten op de respons.

    Returns:
        str: De respons als string, of None als er geen respons is.
    """
    start_time = time.time()
    response = b""
    while time.time() - start_time < duration:
        if readUnitSer.in_waiting > 0:
            response += readUnitSer.read(readUnitSer.in_waiting)

        if b"\n" in response:  # Aannemen dat een nieuwe regel de respons afsluit
            break
    return response.decode(errors="replace").strip() if response else None
def calculate_checksum(command):
    total = sum(command)  # Som van alle bytewaarden
    checksum = total & 0xFF  # Houd alleen de laatste 8 bits
    return checksum

def increment_serial_number(serial):
    """
    Verhoogt het serienummer met 1. Als het getal van 999 naar 001 gaat,
    wordt de tweede letter aangepast. Als de tweede letter 'Z' bereikt,
    wordt de eerste letter verhoogd.

    Args:
        serial (str): Het huidige serienummer, bijvoorbeeld 'FZ999'.

    Returns:
        str: Het volgende serienummer, bijvoorbeeld 'GA001'.
    """
    if not valid_serial_number(serial):
        raise ValueError(f"Invalid serial number: {serial}")

    prefix = serial[:2]  # De eerste twee tekens (letters)
    number = int(serial[2:])  # De laatste drie cijfers als integer

    if number == 999:
        # Reset de cijfers naar 001
        number = 1

        # Verhoog de tweede letter
        second_letter = prefix[1]
        second_letter = chr(ord(second_letter) + 1)

        # Sla de verboden letters over
        while second_letter in "IOQ":
            second_letter = chr(ord(second_letter) + 1)

        if second_letter > 'Z':
            # Als de tweede letter voorbij 'Z' gaat, verhoog de eerste letter
            second_letter = 'A'  # Reset de tweede letter
            first_letter = prefix[0]
            first_letter = chr(ord(first_letter) + 1)

            # Sla de verboden letters over
            while first_letter in "IOQ":
                first_letter = chr(ord(first_letter) + 1)

            # Controleer of we het alfabet overschreden hebben
            if first_letter > 'Z':
                raise ValueError("Het serienummerbereik is uitgeput.")

            prefix = first_letter + second_letter
        else:
            prefix = prefix[0] + second_letter
    else:
        # Verhoog alleen het nummer
        number += 1

    # Stel het nieuwe serienummer samen
    new_serial = f"{prefix}{number:03}"
    return new_serial

def valid_serial_number(serial):
    """
    Controleert of een serienummer geldig is.

    Args:
        serial (str): Het serienummer, bijvoorbeeld 'FN123'.

    Returns:
        bool: True als het serienummer geldig is, anders False.
    """
    if len(serial) != 5:
        return False
    if not serial[:2].isalpha() or any(letter in "IOQ" for letter in serial[:2]):
        return False
    if not serial[2:].isdigit() or int(serial[2:]) == 0:
        return False
    return True