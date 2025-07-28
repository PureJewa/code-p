import serial
import serial.tools.list_ports
#
# def find_usb_device(vid, pid):
#     """Zoek naar het USB-apparaat op basis van VID en PID."""
#     ports = serial.tools.list_ports.comports()
#     for port in ports:
#         # Controleer op VID en PID
#         if port.vid == vid and port.pid == pid:
#             print(f"Apparaat gevonden: {port.description}, op {port.device}")
#             return port.device
#     print("Geen apparaat gevonden")
#     return None
#
# def read_barcode(port, baudrate=9600, timeout=2):
#     """Lees de barcode van de opgegeven seriële poort."""
#     try:
#         with serial.Serial(port, baudrate, timeout=timeout) as ser:
#             print(f"Verbonden met {port}. Wachten op barcode...")
#             while True:
#                 # Lees de barcode en verwijder ongewenste witruimtes
#                 data = ser.readline().decode('utf-8').strip()
#                 if data:
#                     print(f"Barcode gescand: {data}")
#                     return data
#                 else:
#                     print("Wachten op barcode...")
#     except serial.SerialException as e:
#         print(f"Fout bij het openen van de seriële poort: {e}")
#         return None
#     except Exception as e:
#         print(f"Onverwachte fout: {e}")
#         return None
#
# if __name__ == "__main__":
#     # Definieer VID en PID van de barcodescanner
#     vid_barcodescanner = 0x0483  # Vervang door jouw VID voor de barcodescanner
#     pid_barcodescanner = 0x5740  # Vervang door jouw PID voor de barcodescanner
#
#     # Definieer VID en PID voor de Arduino Due
#     vid_arduino_due = 0x2a03  # VID voor Arduino Due
#     pid_arduino_due = 0x003d  # PID voor Arduino Due
#
#     # Zoek naar de barcodescanner
#     port_barcodescanner = find_usb_device(vid_barcodescanner, pid_barcodescanner)
#
#     # Zoek naar de Arduino Due
#     port_arduino_due = find_usb_device(vid_arduino_due, pid_arduino_due)
#
#     # Lees de barcode van de barcodescanner als gevonden
#     if port_barcodescanner:
#         read_barcode(port_barcodescanner)
#
#     # Lees van de Arduino Due als gevonden (meestal gebruikt voor seriële communicatie)
#     if port_arduino_due:
#         print(f"Verbonden met Arduino Due op {port_arduino_due}. Wachten op data...")
#         # read_barcode(port_arduino_due)  # Dit kan aangepast worden, afhankelijk van de Arduino sketch

# import re
#
#
# def zoek_commando_combinaties(bestandspad):
#     with open(bestandspad, "rb") as f:
#         data = f.read()
#
#     # Converteer naar string van leesbare ASCII-tekens (alles tussen 32 en 126)
#     tekst = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
#
#     # Maak alle mogelijke commando’s aan: A00 tot Z99
#     mogelijke_commandos = [f"{chr(letter)}{i:02}" for letter in range(ord('A'), ord('Z')+1) for i in range(100)]
#
#     gevonden = set()
#     for cmd in mogelijke_commandos:
#         if cmd in tekst:
#             gevonden.add(cmd)
#
#     print("Gevonden commando’s in de vorm X00 - X99:")
#     for cmd in sorted(gevonden):
#         print(f" - {cmd}")
#
# def zoek_commando_bytes(bestandspad):
#     with open(bestandspad, "rb") as f:
#         data = f.read()
#
#     mogelijke_commandos = [f"{chr(letter)}{i:02}" for letter in range(ord('A'), ord('Z')+1) for i in range(100)]
#
#     gevonden = set()
#     for cmd in mogelijke_commandos:
#         cmd_bytes = cmd.encode('ascii')
#         if cmd_bytes in data:
#             gevonden.add(cmd)
#
#     print("Gevonden commando’s in binaire data:")
#     for cmd in sorted(gevonden):
#         print(f" - {cmd}")
#
# def zoek_commando_pakketten(bestandspad):
#     with open(bestandspad, "rb") as f:
#         data = f.read()
#
#     # Zoek patronen als: \x01X00..\x03
#     patroon = re.compile(rb'\x01([A-Z]\d{2})\x02.*?\x03', re.DOTALL)
#
#     gevonden = set()
#     for match in patroon.finditer(data):
#         commando = match.group(1).decode('ascii')
#         gevonden.add(commando)
#
#     print("Commando’s gevonden in communicatie-pakketten:")
#     for cmd in sorted(gevonden):
#         print(f" - {cmd}")
#
# # Voorbeeld aanroep
# zoek_commando_combinaties("C:/Users/Jelle/PycharmProjects/post.exe")
# zoek_commando_bytes("C:/Users/Jelle/PycharmProjects/post.exe")
# zoek_commando_pakketten("C:/Users/Jelle/PycharmProjects/post.exe")

# def create_command(serienummer):
#     """
#     Cre�ert een commando dat naar het apparaat gestuurd kan worden.
#
#     Args:
#         serienummer (str): Het serienummer dat geprogrammeerd moet worden.
#
#     Returns:
#         bytes: Het commando dat verstuurd moet worden.
#     """
#     serienummer_bytes = serienummer.encode()  # Converteer naar bytes
#     base_command = (
#         b'\x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D'
#         + serienummer_bytes
#         + b'\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03'
#     )
#     checksum = calculate_checksum(base_command)
#     return base_command + bytes([checksum]) + b'\xA0'
# def send_command(readUnitSer, command):
#     """
#     Stuurt een commando naar het apparaat via de seriele verbinding.
#
#     Args:
#         serial_conn: De seriele verbinding.
#         command (bytes): Het commando dat gestuurd moet worden.
#     """
#     readUnitSer.write(command)
#     readUnitSer.flush()
#
#
# def read_response(readUnitSer, duration):
#     """
#     Leest de respons van het apparaat via de seriele verbinding.
#
#     Args:
#         serial_conn: De seriele verbinding.
#         duration (float): De maximale tijd in seconden om te wachten op de respons.
#
#     Returns:
#         str: De respons als string, of None als er geen respons is.
#     """
#     start_time = time.time()
#     response = b""
#     while time.time() - start_time < duration:
#         if readUnitSer.in_waiting > 0:
#             response += readUnitSer.read(readUnitSer.in_waiting)
#
#         if b"\n" in response:  # Aannemen dat een nieuwe regel de respons afsluit
#             break
#     return response.decode(errors="replace").strip() if response else None
# def calculate_checksum(command):
#     total = sum(command)  # Som van alle bytewaarden
#     checksum = total & 0xFF  # Houd alleen de laatste 8 bits
#     return checksum
#
# DEVICES = {
#     "barcodescanner": {"vid": 0x0483, "pid": 0x5740},
#     "arduino Due": {"vid": 0x2a03, "pid": 0x003d},
#     "programeerUnit": {"vid": 0x2047 , "pid": 0x0ab9},
#
# }
# def find_all_devices():
#     found_devices = {}
#     ports = serial.tools.list_ports.comports()
#     for name, info in DEVICES.items():
#         match = next((p.device for p in ports if p.vid == info["vid"] and p.pid == info["pid"]), None)
#         found_devices[name] = match
#     return found_devices
#
#
# def init_device():
#     # from helperfunctions import find_all_devices
#     device_ports = find_all_devices()
#
#     for device, port in device_ports.items():
#         if port:
#             print(f"{device} zit op: {port}")
#         else:
#             print(f"{device} niet gevonden")
#     return device_ports
# COMMAND_SERIAL = b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'
# device_ports = init_device()
# send_command(device_ports["programeerUnit"], COMMAND_SERIAL)
# response = read_response(device_ports["programeerUnit"], 5)
# # print(f"Respons ontvangen: {response}")
# import serial
# import serial.tools.list_ports
# import time
#
# def create_command(serienummer):
#     serienummer_bytes = serienummer.encode()
#     base_command = (
#         b'\x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D' +
#         serienummer_bytes +
#         b'\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03'
#     )
#     checksum = calculate_checksum(base_command)
#     return base_command + bytes([checksum]) + b'\xA0'
#
# def calculate_checksum(command):
#     total = sum(command)
#     checksum = total & 0xFF
#     return checksum
#
# def send_command(serial_conn, command):
#     serial_conn.write(command)
#     serial_conn.flush()
#
# def read_response(serial_conn, duration):
#     start_time = time.time()
#     response = b""
#     while time.time() - start_time < duration:
#         if serial_conn.in_waiting > 0:
#             response += serial_conn.read(serial_conn.in_waiting)
#         if b"\n" in response:
#             break
#     return response.decode(errors="replace").strip() if response else None
#
# DEVICES = {
#     "barcodescanner": {"vid": 0x0483, "pid": 0x5740},
#     "arduino Due": {"vid": 0x2a03, "pid": 0x003d},
#     "programeerUnit": {"vid": 0x2047 , "pid": 0x0ab9},
# }
#
# def find_all_devices():
#     found_devices = {}
#     ports = serial.tools.list_ports.comports()
#     for name, info in DEVICES.items():
#         match = next((p.device for p in ports if p.vid == info["vid"] and p.pid == info["pid"]), None)
#         found_devices[name] = match
#     return found_devices
#
# def init_device():
#     device_ports = find_all_devices()
#     for device, port in device_ports.items():
#         if port:
#             print(f"{device} zit op: {port}")
#         else:
#             print(f"{device} niet gevonden")
#     return device_ports
#
# # === START VAN HET SCRIPT ===
#
# COMMAND_SERIAL = b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'
# device_ports = init_device()
#
# poort = device_ports["programeerUnit"]
# if not poort:
#     print("Geen programeerUnit gevonden.")
#     exit()
#
# try:
#     with serial.Serial(poort, baudrate=9600, timeout=1) as ser:
#         print(f"Verstuur: {COMMAND_SERIAL.hex(' ')}")
#         send_command(ser, COMMAND_SERIAL)
#         response = read_response(ser, 5)
#         print(f"Respons ontvangen: {response}")
# except serial.SerialException as e:
#     print(f"Fout bij openen van poort: {e}")
# b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'

import serial
import serial.tools.list_ports
import time
import string

# ===== Config =====
BAUDRATE = 9600
DELAY_BETWEEN_COMMANDS = 0.1  # in seconden
RESPONSETIME = 0.1  # max wachttijd voor respons


# ===== Functies =====

def calculate_checksum(command):
    total = sum(command)
    return total & 0xFF


def generate_command(code):
    payload = code.encode('ascii')
    base_command = b'\x01' + payload + b'\x02\x03'

    # print(f"Code: {payload}")
    # print(f"Base command: {base_command.hex(' ')}")

    checksum = calculate_checksum(base_command)
    # print(f"Checksum: {checksum:#04x}")  # Hex formaat

    return base_command + bytes([checksum]) + b'\xA0'



def read_response(serial_conn, timeout):
    start_time = time.time()
    response = b""
    while time.time() - start_time < timeout:
        if serial_conn.in_waiting > 0:
            response += serial_conn.read(serial_conn.in_waiting)
        if b'\n' in response:
            break
    return response.decode(errors="replace").strip() if response else None


def find_device_by_vid_pid(vid, pid):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == vid and port.pid == pid:
            return port.device
    return None


# ===== MAIN =====

VID = 0x2047  # programeerUnit
PID = 0x0ab9

poort = find_device_by_vid_pid(VID, PID)
if not poort:
    print("ProgrameerUnit niet gevonden.")
    exit()

try:
    with serial.Serial(poort, baudrate=BAUDRATE, timeout=1) as ser:
        print(f"Verbonden met {poort}")

        for letter in string.ascii_uppercase:  # A-Z
            for number in range(50):  # 00-99
                if letter == "A" or letter =="B":
                    break
                code = f"{letter}{number:02}"
                # code = 'N24'
                command = generate_command(code)

                ser.write(command)
                ser.flush()
                print(f"Verzonden: {code}")

                response = read_response(ser, RESPONSETIME)
                if response:
                    print(f"Respons op {code}: {response}")
                else:
                    print(f"Geen respons op {code}")

                time.sleep(DELAY_BETWEEN_COMMANDS)

except serial.SerialException as e:
    print(f"Fout bij verbinden: {e}")
