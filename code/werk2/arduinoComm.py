import serial
import threading
import queue
import time
from logic.config import device_ports

COM_PORT = device_ports.get("arduino Due")
BAUD_RATE = 9600

message_queue = queue.Queue()
stop_event = threading.Event()  # Event om threads netjes af te sluiten

arduino = None
is_booted = False

def initialize_serial():
    global arduino
    try:
        arduino = serial.Serial(COM_PORT, BAUD_RATE, timeout=0.5)
        time.sleep(2)  # Geef Arduino tijd om op te starten
        arduino.reset_input_buffer()
        message_queue.put("✅ Seriële poort geopend.")
        return True
    except serial.SerialException as e:
        message_queue.put(f"❌ Fout bij openen seriële poort: {e}. Controleer of de poort vrij is en correct is.")
        return False


def serial_read_loop():
    global is_booted
    # Wacht totdat seriële verbinding is geopend
    while arduino is None:
        if stop_event.is_set():
            return
        time.sleep(0.1)

    # Boot handshake
    boot_attempts = 0
    while not is_booted and boot_attempts < 10:  # Max 10 pogingen
        if stop_event.is_set():
            return
        arduino.write(b"Python_Booted\n")
        message_queue.put("📤 Verzend: Python_Booted")

        start_time = time.time()
        response_received = False
        while time.time() - start_time < 2:  # Wacht 2 seconden op boot response
            if stop_event.is_set():
                return
            if arduino.in_waiting:
                response = arduino.readline().decode('utf-8').strip()
                if response:
                    message_queue.put("⤷ " + response)
                    if response == "ARDUINO_BOOTED":
                        message_queue.put("✅ Arduino klaar")
                        is_booted = True
                        response_received = True
                        break
        if not response_received:
            message_queue.put(f"⚠️ Geen 'ARDUINO_BOOTED' respons na poging {boot_attempts + 1}.")
            boot_attempts += 1
        time.sleep(1)  # Wacht 1 seconde voor volgende poging

    if not is_booted:
        message_queue.put("❌ Boot handshake mislukt na meerdere pogingen. Start programma opnieuw.")
        stop_threads.set()  # Stop verdere communicatie als boot mislukt

    # Hoofd seriële leesloop
    while not stop_event.is_set():
        try:
            if arduino.in_waiting:
                msg = arduino.readline().decode('utf-8').strip()
                if msg:
                    message_queue.put("⤷ " + msg)  # Toon alles wat binnenkomt
                    if msg.startswith("ARDUINO_SAYS:"):
                        cmd = msg.split(":")[1]
                        message_queue.put(f"🔄 Arduino vraagt om commando: {cmd}")
                        # Hier zou je logica kunnen toevoegen om op 'cmd' te reageren
                        arduino.write(f"PYTHON_ACK:{cmd}\n".encode('utf-8'))
                        arduino.write(b"PYTHON_DONE\n")
                        message_queue.put(f"📤 Verzend: PYTHON_ACK:{cmd} & PYTHON_DONE")

                    elif msg == "ARDUINO_PROGRAMMEER":
                        message_queue.put("🔧 Arduino vraagt om programmeeractie.")
                        # Simulate programming action
                        time.sleep(0.5)  # Korte vertraging om actie te simuleren
                        arduino.write(b"PYTHON_PROGRAMMING_DONE\n")
                        message_queue.put("📤 Verzend: PYTHON_PROGRAMMING_DONE")
                    elif msg =='ARDUINO_Persen_OK':
                        message_queue.put("✅ Arduino heeft gepersd.")
                        arduino.write(b"PYTHON_PERSEN_ACK\n")
                        arduino.write(b"PYTHON_PERSEN_DONE\n")
                        message_queue.put(f"📤 Verzend: PYTHON_ACK:{cmd} & PYTHON_DONE")

                    # Optioneel: afhandeling van ACK/DONE voor verstuurd commando
                    # Als de GUI wacht op een specifieke ACK/DONE, moet dit hier worden afgehandeld
                    # en via een Queue of Event terug naar de send_command functie worden gecommuniceerd.
                    # Voor nu volstaat de visuele feedback in de textbox.

        except serial.SerialException as e:
            message_queue.put(f"❌ Seriële fout: {e}. Verbinding mogelijk verbroken.")
            stop_event.set()
            break
        except Exception as e:
            message_queue.put(f"❌ Onverwachte fout in seriële thread: {e}")
            stop_event.set()
            break
        time.sleep(0.01)  # Korte pauze om CPU te ontlasten


def send_command(cmd):
    if not is_booted:
        message_queue.put("⚠️ Arduino is nog niet klaar.")
        return
    if cmd.strip() == "":
        return

    # Voorkom dat de GUI blokkeert terwijl een commando wordt verstuurd
    def _send_actual_command():
        try:
            full_cmd = f"PYTHON_SAYS:{cmd}\n".encode('utf-8')
            arduino.write(full_cmd)
            message_queue.put(f"📤 Verzend: {cmd}")
        except Exception as e:
            message_queue.put(f"❌ Fout bij verzenden commando: {e}")

    threading.Thread(target=_send_actual_command, daemon=True).start()
