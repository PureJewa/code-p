import time

import serial

#from GUI import App


# Commandos voor het apparaat
COMMAND_SERIAL = b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'
COMMAND_PRESSURE = b'\x01\x47\x32\x38\x02\x03\xB7\xA0'
COMMAND_PUSHSERIE = b'\x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D\x46\x4E\x30\x38\x36\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03\x80D\xA0'
#commi = b'x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D\SERRIENUMMER\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03\LOWBYTECHECK\xA0'
#port = "COM19"
result = {'serial_number': "Onbekend", 'pressure_value': "Onbekend", 'temperature_value': "Onbekend"}
def send_command(serial_conn, command):
    """
    Stuurt een commando naar het apparaat via de seriele verbinding.

    Args:
        serial_conn: De seriele verbinding.
        command (bytes): Het commando dat gestuurd moet worden.
    """
    serial_conn.write(command)
    serial_conn.flush()


def read_response(serial_conn, duration):
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
        if serial_conn.in_waiting > 0:
            response += serial_conn.read(serial_conn.in_waiting)

        if b"\n" in response:  # Aannemen dat een nieuwe regel de respons afsluit
            break
    print(response)
    return response.decode(errors="replace").strip() if response else None


def Diver_Read_Unit():
    # Zoek naar beschikbare poorten
    port = '/dev/ttyACM0'
    baud_rate = 9600
    duration = 2  # Timeout in seconden


    try:
        with serial.Serial(port, baud_rate, timeout=1) as serial_conn:
            # Lees het serienummer
            send_command(serial_conn, COMMAND_SERIAL)
            serial_response = read_response(serial_conn, duration)
            if serial_response and "-" in serial_response:
                result["serial_number"] = serial_response.split("-")[1][:5]

            # Lees druk en temperatuur
            send_command(serial_conn, COMMAND_PRESSURE)
            pressure_response = read_response(serial_conn, duration)
            if pressure_response:
                if "G28" in pressure_response:
                    result["pressure_value"] = pressure_response[5:12]
                    result["temperature_value"] = pressure_response[15:22]

    except Exception as e:
        print(f"Fout bij seriele communicatie: {e}")
    return result
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

def calculate_checksum(command):
    total = sum(command)  # Som van alle bytewaarden
    checksum = total & 0xFF  # Houd alleen de laatste 8 bits
    return checksum
def send_command(serial_conn, command):
    """
    Stuurt een commando naar het apparaat via de seriele verbinding.

    Args:
        serial_conn: De seriele verbinding.
        command (bytes): Het commando dat gestuurd moet worden.
    """
    serial_conn.write(command)
    serial_conn.flush()


def read_response(serial_conn, duration):
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
        if serial_conn.in_waiting > 0:
            response += serial_conn.read(serial_conn.in_waiting)

        if b"\n" in response:  # Aannemen dat een nieuwe regel de respons afsluit
            break
    print(response)
    return response.decode(errors="replace").strip() if response else None


def create_command(serienummer):
    """
    Creëert een commando dat naar het apparaat gestuurd kan worden.

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
"""
def get_user_serial_number():
    while True:
        serial = input("Voer een geldig serienummer in (bijv. AB001): ").upper()
        if valid_serial_number(serial):
            return serial
        print("Ongeldig serienummer. Probeer opnieuw.")
"""
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



def Prog_Diver(start_serial, num_devices):
    try:
        with serial.Serial('/dev/ttyACM0', 9600, timeout=1) as serial_conn:
            current_serial = start_serial
            for _ in range(num_devices):
                print(f"Programmeren van apparaat met serienummer: {current_serial}")
                command = create_command(current_serial)
                send_command(serial_conn, command)
                response = read_response(serial_conn, 2)
                print(f"Respons: {response if response else 'Geen respons'}")
                current_serial = increment_serial_number(current_serial)
    except Exception as e:
        print(f"Fout: {e}")
