import serial
import serial.tools.list_ports

def find_available_ports():
    """Vind alle beschikbare COM-poorten en controleer of er apparaten op aangesloten zijn."""
    ports = serial.tools.list_ports.comports()
    available_ports = []

    for port in ports:
        try:
            ser = serial.Serial(port.device, 9600, timeout=1)
            ser.close()
            available_ports.append(port.device)
        except (OSError, serial.SerialException):
            pass

    return available_ports

def send_command(port, command):
    """Verstuur een commando naar een specifieke COM-poort."""
    try:
        ser = serial.Serial(port, 9600, timeout=1)
        ser.write(command.encode())
        response = ser.readline().decode().strip()
        ser.close()
        return response
    except Exception as e:
        return f"Fout bij het verzenden van het commando: {e}"

# Vind beschikbare COM-poorten
available_ports = find_available_ports()

if available_ports:
    print("Beschikbare COM-poorten:", available_ports)
    # Voorbeeld: verstuur een commando naar de eerste beschikbare poort
    port = available_ports[0]
    response = send_command(port, 'ENABLE_PORT_1')  # Vervang dit door het juiste commando
    print(f"Antwoord van {port}:", response)
else:
    print("Geen beschikbare COM-poorten gevonden.")
