import serial
import serial.tools.list_ports

def find_usb_device(vid, pid):
    """Zoek naar het USB-apparaat op basis van VID en PID."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Controleer op VID en PID
        if port.vid == vid and port.pid == pid:
            print(f"Apparaat gevonden: {port.description}, op {port.device}")
            return port.device
    print("Geen apparaat gevonden")
    return None

def read_barcode(port, baudrate=9600, timeout=2):
    """Lees de barcode van de opgegeven seriële poort."""
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            print(f"Verbonden met {port}. Wachten op barcode...")
            while True:
                # Lees de barcode en verwijder ongewenste witruimtes
                data = ser.readline().decode('utf-8').strip()
                if data:
                    print(f"Barcode gescand: {data}")
                    return data
                else:
                    print("Wachten op barcode...")
    except serial.SerialException as e:
        print(f"Fout bij het openen van de seriële poort: {e}")
        return None
    except Exception as e:
        print(f"Onverwachte fout: {e}")
        return None

if __name__ == "__main__":
    # Definieer VID en PID van de barcodescanner
    vid_barcodescanner = 0x0483  # Vervang door jouw VID voor de barcodescanner
    pid_barcodescanner = 0x5740  # Vervang door jouw PID voor de barcodescanner

    # Definieer VID en PID voor de Arduino Due
    vid_arduino_due = 0x2a03  # VID voor Arduino Due
    pid_arduino_due = 0x003d  # PID voor Arduino Due

    # Zoek naar de barcodescanner
    port_barcodescanner = find_usb_device(vid_barcodescanner, pid_barcodescanner)

    # Zoek naar de Arduino Due
    port_arduino_due = find_usb_device(vid_arduino_due, pid_arduino_due)

    # Lees de barcode van de barcodescanner als gevonden
    if port_barcodescanner:
        read_barcode(port_barcodescanner)

    # Lees van de Arduino Due als gevonden (meestal gebruikt voor seriële communicatie)
    if port_arduino_due:
        print(f"Verbonden met Arduino Due op {port_arduino_due}. Wachten op data...")
        # read_barcode(port_arduino_due)  # Dit kan aangepast worden, afhankelijk van de Arduino sketch
