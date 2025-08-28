# # # # # import serial
# # # # # import serial.tools.list_ports
# # # # # #
# # # # # # def find_usb_device(vid, pid):
# # # # # #     """Zoek naar het USB-apparaat op basis van VID en PID."""
# # # # # #     ports = serial.tools.list_ports.comports()
# # # # # #     for port in ports:
# # # # # #         # Controleer op VID en PID
# # # # # #         if port.vid == vid and port.pid == pid:
# # # # # #             print(f"Apparaat gevonden: {port.description}, op {port.device}")
# # # # # #             return port.device
# # # # # #     print("Geen apparaat gevonden")
# # # # # #     return None
# # # # # #
# # # # # # def read_barcode(port, baudrate=9600, timeout=2):
# # # # # #     """Lees de barcode van de opgegeven seriële poort."""
# # # # # #     try:
# # # # # #         with serial.Serial(port, baudrate, timeout=timeout) as ser:
# # # # # #             print(f"Verbonden met {port}. Wachten op barcode...")
# # # # # #             while True:
# # # # # #                 # Lees de barcode en verwijder ongewenste witruimtes
# # # # # #                 data = ser.readline().decode('utf-8').strip()
# # # # # #                 if data:
# # # # # #                     print(f"Barcode gescand: {data}")
# # # # # #                     return data
# # # # # #                 else:
# # # # # #                     print("Wachten op barcode...")
# # # # # #     except serial.SerialException as e:
# # # # # #         print(f"Fout bij het openen van de seriële poort: {e}")
# # # # # #         return None
# # # # # #     except Exception as e:
# # # # # #         print(f"Onverwachte fout: {e}")
# # # # # #         return None
# # # # # #
# # # # # # if __name__ == "__main__":
# # # # # #     # Definieer VID en PID van de barcodescanner
# # # # # #     vid_barcodescanner = 0x0483  # Vervang door jouw VID voor de barcodescanner
# # # # # #     pid_barcodescanner = 0x5740  # Vervang door jouw PID voor de barcodescanner
# # # # # #
# # # # # #     # Definieer VID en PID voor de Arduino Due
# # # # # #     vid_arduino_due = 0x2a03  # VID voor Arduino Due
# # # # # #     pid_arduino_due = 0x003d  # PID voor Arduino Due
# # # # # #
# # # # # #     # Zoek naar de barcodescanner
# # # # # #     port_barcodescanner = find_usb_device(vid_barcodescanner, pid_barcodescanner)
# # # # # #
# # # # # #     # Zoek naar de Arduino Due
# # # # # #     port_arduino_due = find_usb_device(vid_arduino_due, pid_arduino_due)
# # # # # #
# # # # # #     # Lees de barcode van de barcodescanner als gevonden
# # # # # #     if port_barcodescanner:
# # # # # #         read_barcode(port_barcodescanner)
# # # # # #
# # # # # #     # Lees van de Arduino Due als gevonden (meestal gebruikt voor seriële communicatie)
# # # # # #     if port_arduino_due:
# # # # # #         print(f"Verbonden met Arduino Due op {port_arduino_due}. Wachten op data...")
# # # # # #         # read_barcode(port_arduino_due)  # Dit kan aangepast worden, afhankelijk van de Arduino sketch
# # # # #
# # # # # # import re
# # # # # #
# # # # # #
# # # # # # def zoek_commando_combinaties(bestandspad):
# # # # # #     with open(bestandspad, "rb") as f:
# # # # # #         data = f.read()
# # # # # #
# # # # # #     # Converteer naar string van leesbare ASCII-tekens (alles tussen 32 en 126)
# # # # # #     tekst = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data)
# # # # # #
# # # # # #     # Maak alle mogelijke commando’s aan: A00 tot Z99
# # # # # #     mogelijke_commandos = [f"{chr(letter)}{i:02}" for letter in range(ord('A'), ord('Z')+1) for i in range(100)]
# # # # # #
# # # # # #     gevonden = set()
# # # # # #     for cmd in mogelijke_commandos:
# # # # # #         if cmd in tekst:
# # # # # #             gevonden.add(cmd)
# # # # # #
# # # # # #     print("Gevonden commando’s in de vorm X00 - X99:")
# # # # # #     for cmd in sorted(gevonden):
# # # # # #         print(f" - {cmd}")
# # # # # #
# # # # # # def zoek_commando_bytes(bestandspad):
# # # # # #     with open(bestandspad, "rb") as f:
# # # # # #         data = f.read()
# # # # # #
# # # # # #     mogelijke_commandos = [f"{chr(letter)}{i:02}" for letter in range(ord('A'), ord('Z')+1) for i in range(100)]
# # # # # #
# # # # # #     gevonden = set()
# # # # # #     for cmd in mogelijke_commandos:
# # # # # #         cmd_bytes = cmd.encode('ascii')
# # # # # #         if cmd_bytes in data:
# # # # # #             gevonden.add(cmd)
# # # # # #
# # # # # #     print("Gevonden commando’s in binaire data:")
# # # # # #     for cmd in sorted(gevonden):
# # # # # #         print(f" - {cmd}")
# # # # # #
# # # # # # def zoek_commando_pakketten(bestandspad):
# # # # # #     with open(bestandspad, "rb") as f:
# # # # # #         data = f.read()
# # # # # #
# # # # # #     # Zoek patronen als: \x01X00..\x03
# # # # # #     patroon = re.compile(rb'\x01([A-Z]\d{2})\x02.*?\x03', re.DOTALL)
# # # # # #
# # # # # #     gevonden = set()
# # # # # #     for match in patroon.finditer(data):
# # # # # #         commando = match.group(1).decode('ascii')
# # # # # #         gevonden.add(commando)
# # # # # #
# # # # # #     print("Commando’s gevonden in communicatie-pakketten:")
# # # # # #     for cmd in sorted(gevonden):
# # # # # #         print(f" - {cmd}")
# # # # # #
# # # # # # # Voorbeeld aanroep
# # # # # # zoek_commando_combinaties("C:/Users/Jelle/PycharmProjects/post.exe")
# # # # # # zoek_commando_bytes("C:/Users/Jelle/PycharmProjects/post.exe")
# # # # # # zoek_commando_pakketten("C:/Users/Jelle/PycharmProjects/post.exe")
# # # # #
# # # # # # def create_command(serienummer):
# # # # # #     """
# # # # # #     Cre�ert een commando dat naar het apparaat gestuurd kan worden.
# # # # # #
# # # # # #     Args:
# # # # # #         serienummer (str): Het serienummer dat geprogrammeerd moet worden.
# # # # # #
# # # # # #     Returns:
# # # # # #         bytes: Het commando dat verstuurd moet worden.
# # # # # #     """
# # # # # #     serienummer_bytes = serienummer.encode()  # Converteer naar bytes
# # # # # #     base_command = (
# # # # # #         b'\x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D'
# # # # # #         + serienummer_bytes
# # # # # #         + b'\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03'
# # # # # #     )
# # # # # #     checksum = calculate_checksum(base_command)
# # # # # #     return base_command + bytes([checksum]) + b'\xA0'
# # # # # # def send_command(readUnitSer, command):
# # # # # #     """
# # # # # #     Stuurt een commando naar het apparaat via de seriele verbinding.
# # # # # #
# # # # # #     Args:
# # # # # #         serial_conn: De seriele verbinding.
# # # # # #         command (bytes): Het commando dat gestuurd moet worden.
# # # # # #     """
# # # # # #     readUnitSer.write(command)
# # # # # #     readUnitSer.flush()
# # # # # #
# # # # # #
# # # # # # def read_response(readUnitSer, duration):
# # # # # #     """
# # # # # #     Leest de respons van het apparaat via de seriele verbinding.
# # # # # #
# # # # # #     Args:
# # # # # #         serial_conn: De seriele verbinding.
# # # # # #         duration (float): De maximale tijd in seconden om te wachten op de respons.
# # # # # #
# # # # # #     Returns:
# # # # # #         str: De respons als string, of None als er geen respons is.
# # # # # #     """
# # # # # #     start_time = time.time()
# # # # # #     response = b""
# # # # # #     while time.time() - start_time < duration:
# # # # # #         if readUnitSer.in_waiting > 0:
# # # # # #             response += readUnitSer.read(readUnitSer.in_waiting)
# # # # # #
# # # # # #         if b"\n" in response:  # Aannemen dat een nieuwe regel de respons afsluit
# # # # # #             break
# # # # # #     return response.decode(errors="replace").strip() if response else None
# # # # # # def calculate_checksum(command):
# # # # # #     total = sum(command)  # Som van alle bytewaarden
# # # # # #     checksum = total & 0xFF  # Houd alleen de laatste 8 bits
# # # # # #     return checksum
# # # # # #
# # # # # # DEVICES = {
# # # # # #     "barcodescanner": {"vid": 0x0483, "pid": 0x5740},
# # # # # #     "arduino Due": {"vid": 0x2a03, "pid": 0x003d},
# # # # # #     "programeerUnit": {"vid": 0x2047 , "pid": 0x0ab9},
# # # # # #
# # # # # # }
# # # # # # def find_all_devices():
# # # # # #     found_devices = {}
# # # # # #     ports = serial.tools.list_ports.comports()
# # # # # #     for name, info in DEVICES.items():
# # # # # #         match = next((p.device for p in ports if p.vid == info["vid"] and p.pid == info["pid"]), None)
# # # # # #         found_devices[name] = match
# # # # # #     return found_devices
# # # # # #
# # # # # #
# # # # # # def init_device():
# # # # # #     # from helperfunctions import find_all_devices
# # # # # #     device_ports = find_all_devices()
# # # # # #
# # # # # #     for device, port in device_ports.items():
# # # # # #         if port:
# # # # # #             print(f"{device} zit op: {port}")
# # # # # #         else:
# # # # # #             print(f"{device} niet gevonden")
# # # # # #     return device_ports
# # # # # # COMMAND_SERIAL = b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'
# # # # # # device_ports = init_device()
# # # # # # send_command(device_ports["programeerUnit"], COMMAND_SERIAL)
# # # # # # response = read_response(device_ports["programeerUnit"], 5)
# # # # # # # print(f"Respons ontvangen: {response}")
# # # # # # import serial
# # # # # # import serial.tools.list_ports
# # # # # # import time
# # # # # #
# # # # # # def create_command(serienummer):
# # # # # #     serienummer_bytes = serienummer.encode()
# # # # # #     base_command = (
# # # # # #         b'\x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D' +
# # # # # #         serienummer_bytes +
# # # # # #         b'\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03'
# # # # # #     )
# # # # # #     checksum = calculate_checksum(base_command)
# # # # # #     return base_command + bytes([checksum]) + b'\xA0'
# # # # # #
# # # # # # def calculate_checksum(command):
# # # # # #     total = sum(command)
# # # # # #     checksum = total & 0xFF
# # # # # #     return checksum
# # # # # #
# # # # # # def send_command(serial_conn, command):
# # # # # #     serial_conn.write(command)
# # # # # #     serial_conn.flush()
# # # # # #
# # # # # # def read_response(serial_conn, duration):
# # # # # #     start_time = time.time()
# # # # # #     response = b""
# # # # # #     while time.time() - start_time < duration:
# # # # # #         if serial_conn.in_waiting > 0:
# # # # # #             response += serial_conn.read(serial_conn.in_waiting)
# # # # # #         if b"\n" in response:
# # # # # #             break
# # # # # #     return response.decode(errors="replace").strip() if response else None
# # # # # #
# # # # # # DEVICES = {
# # # # # #     "barcodescanner": {"vid": 0x0483, "pid": 0x5740},
# # # # # #     "arduino Due": {"vid": 0x2a03, "pid": 0x003d},
# # # # # #     "programeerUnit": {"vid": 0x2047 , "pid": 0x0ab9},
# # # # # # }
# # # # # #
# # # # # # def find_all_devices():
# # # # # #     found_devices = {}
# # # # # #     ports = serial.tools.list_ports.comports()
# # # # # #     for name, info in DEVICES.items():
# # # # # #         match = next((p.device for p in ports if p.vid == info["vid"] and p.pid == info["pid"]), None)
# # # # # #         found_devices[name] = match
# # # # # #     return found_devices
# # # # # #
# # # # # # def init_device():
# # # # # #     device_ports = find_all_devices()
# # # # # #     for device, port in device_ports.items():
# # # # # #         if port:
# # # # # #             print(f"{device} zit op: {port}")
# # # # # #         else:
# # # # # #             print(f"{device} niet gevonden")
# # # # # #     return device_ports
# # # # # #
# # # # # # # === START VAN HET SCRIPT ===
# # # # # #
# # # # # # COMMAND_SERIAL = b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'
# # # # # # device_ports = init_device()
# # # # # #
# # # # # # poort = device_ports["programeerUnit"]
# # # # # # if not poort:
# # # # # #     print("Geen programeerUnit gevonden.")
# # # # # #     exit()
# # # # # #
# # # # # # try:
# # # # # #     with serial.Serial(poort, baudrate=9600, timeout=1) as ser:
# # # # # #         print(f"Verstuur: {COMMAND_SERIAL.hex(' ')}")
# # # # # #         send_command(ser, COMMAND_SERIAL)
# # # # # #         response = read_response(ser, 5)
# # # # # #         print(f"Respons ontvangen: {response}")
# # # # # # except serial.SerialException as e:
# # # # # #     print(f"Fout bij openen van poort: {e}")
# # # # # # b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'
# # # # #
# # # # # import serial
# # # # # import serial.tools.list_ports
# # # # # import time
# # # # # import string
# # # # #
# # # # # # ===== Config =====
# # # # # BAUDRATE = 9600
# # # # # DELAY_BETWEEN_COMMANDS = 0.1  # in seconden
# # # # # RESPONSETIME = 0.1  # max wachttijd voor respons
# # # # #
# # # # #
# # # # # # ===== Functies =====
# # # # #
# # # # # def calculate_checksum(command):
# # # # #     total = sum(command)
# # # # #     return total & 0xFF
# # # # #
# # # # #
# # # # # def generate_command(code):
# # # # #     payload = code.encode('ascii')
# # # # #     base_command = b'\x01' + payload + b'\x02\x03'
# # # # #
# # # # #     # print(f"Code: {payload}")
# # # # #     # print(f"Base command: {base_command.hex(' ')}")
# # # # #
# # # # #     checksum = calculate_checksum(base_command)
# # # # #     # print(f"Checksum: {checksum:#04x}")  # Hex formaat
# # # # #
# # # # #     return base_command + bytes([checksum]) + b'\xA0'
# # # # #
# # # # #
# # # # #
# # # # # def read_response(serial_conn, timeout):
# # # # #     start_time = time.time()
# # # # #     response = b""
# # # # #     while time.time() - start_time < timeout:
# # # # #         if serial_conn.in_waiting > 0:
# # # # #             response += serial_conn.read(serial_conn.in_waiting)
# # # # #         if b'\n' in response:
# # # # #             break
# # # # #     return response.decode(errors="replace").strip() if response else None
# # # # #
# # # # #
# # # # # def find_device_by_vid_pid(vid, pid):
# # # # #     ports = serial.tools.list_ports.comports()
# # # # #     for port in ports:
# # # # #         if port.vid == vid and port.pid == pid:
# # # # #             return port.device
# # # # #     return None
# # # # #
# # # # #
# # # # # # ===== MAIN =====
# # # # #
# # # # # VID = 0x2047  # programeerUnit
# # # # # PID = 0x0ab9
# # # # #
# # # # # poort = find_device_by_vid_pid(VID, PID)
# # # # # if not poort:
# # # # #     print("ProgrameerUnit niet gevonden.")
# # # # #     exit()
# # # # #
# # # # # try:
# # # # #     with serial.Serial(poort, baudrate=BAUDRATE, timeout=1) as ser:
# # # # #         print(f"Verbonden met {poort}")
# # # # #
# # # # #         for letter in string.ascii_uppercase:  # A-Z
# # # # #             for number in range(50):  # 00-99
# # # # #                 if letter == "A" or letter =="B":
# # # # #                     break
# # # # #                 code = f"{letter}{number:02}"
# # # # #                 # code = 'N24'
# # # # #                 command = generate_command(code)
# # # # #
# # # # #                 ser.write(command)
# # # # #                 ser.flush()
# # # # #                 print(f"Verzonden: {code}")
# # # # #
# # # # #                 response = read_response(ser, RESPONSETIME)
# # # # #                 if response:
# # # # #                     print(f"Respons op {code}: {response}")
# # # # #                 else:
# # # # #                     print(f"Geen respons op {code}")
# # # # #
# # # # #                 time.sleep(DELAY_BETWEEN_COMMANDS)
# # # # #
# # # # # except serial.SerialException as e:
# # # # #     print(f"Fout bij verbinden: {e}")
# # # # import customtkinter as ctk
# # # # from datetime import datetime
# # # #
# # # # class SerialSimulatorWindow(ctk.CTkToplevel):
# # # #     def __init__(self, master, on_send_callback=None):
# # # #         super().__init__(master)
# # # #         self.title("Arduino Simulator")
# # # #         self.geometry("500x400")
# # # #         self.on_send_callback = on_send_callback
# # # #
# # # #         # Outputbox
# # # #         self.output_box = ctk.CTkTextbox(self, width=480, height=300)
# # # #         self.output_box.pack(padx=10, pady=(10, 5))
# # # #         self.output_box.configure(state="disabled")  # Alleen lezen
# # # #
# # # #         # Invoerveld
# # # #         self.input_frame = ctk.CTkFrame(self)
# # # #         self.input_frame.pack(fill="x", padx=10, pady=(0, 10))
# # # #
# # # #         self.input_entry = ctk.CTkEntry(self.input_frame)
# # # #         self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
# # # #         self.input_entry.bind("<Return>", self._send_message)
# # # #
# # # #         self.send_button = ctk.CTkButton(self.input_frame, text="Verstuur", command=self._send_message)
# # # #         self.send_button.pack(side="right")
# # # #
# # # #     def _send_message(self, event=None):
# # # #         message = self.input_entry.get().strip()
# # # #         if message:
# # # #             self._append_message(">>", message)
# # # #             self.input_entry.delete(0, "end")
# # # #             if self.on_send_callback:
# # # #                 response = self.on_send_callback(message)
# # # #                 if response:
# # # #                     self._append_message("<<", response)
# # # #
# # # #     def _append_message(self, prefix, message):
# # # #         timestamp = datetime.now().strftime("%H:%M:%S")
# # # #         formatted = f"[{timestamp}] {prefix} {message}\n"
# # # #         self.output_box.configure(state="normal")
# # # #         self.output_box.insert("end", formatted)
# # # #         self.output_box.configure(state="disabled")
# # # #         self.output_box.see("end")
# # # #
# # # # # Voorbeeld van hoe je dit zou gebruiken in je hoofdapplicatie
# # # # def open_simulator_window():
# # # #     def fake_arduino_response(input_text):
# # # #         # Hier kun je simuleren hoe de Arduino zou reageren
# # # #         if input_text.lower() == "status":
# # # #             return "Systeem OK"
# # # #         elif input_text.lower() == "start":
# # # #             return "Startcommando ontvangen"
# # # #         else:
# # # #             return f"Onbekend commando: {input_text}"
# # # #
# # # #     SerialSimulatorWindow(master=root, on_send_callback=fake_arduino_response)
# # # #
# # # # # Voorbeeld hoofdvenster
# # # # if __name__ == "__main__":
# # # #     ctk.set_appearance_mode("dark")
# # # #     ctk.set_default_color_theme("blue")
# # # #     root = ctk.CTk()
# # # #     root.geometry("300x200")
# # # #     root.title("Hoofdvenster")
# # # #
# # # #     open_button = ctk.CTkButton(root, text="Open Simulator", command=open_simulator_window)
# # # #     open_button.pack(pady=40)
# # # #
# # # #     root.mainloop()
# # #
# # # import customtkinter as ctk
# # #
# # # ctk.set_appearance_mode("light")
# # # ctk.set_default_color_theme("blue")
# # #
# # # app = ctk.CTk()
# # # app.title("Entry + Enter voorbeeld")
# # # app.geometry("400x300")
# # #
# # #
# # # def make_entry_with_button(parent, label, command):
# # #     """Maakt een entry + knop die dezelfde functie aanroept, ook bij Enter."""
# # #     frame = ctk.CTkFrame(parent)
# # #     frame.pack(pady=10, padx=10, fill="x")
# # #
# # #     lbl = ctk.CTkLabel(frame, text=label)
# # #     lbl.pack(side="left", padx=5)
# # #
# # #     entry = ctk.CTkEntry(frame, width=200)
# # #     entry.pack(side="left", padx=5)
# # #
# # #     btn = ctk.CTkButton(frame, text="OK", command=lambda: command(entry))
# # #     btn.pack(side="left", padx=5)
# # #
# # #     # Bind Enter in dit entry aan dezelfde command
# # #     entry.bind("<Return>", lambda event: command(entry))
# # #
# # #     return entry
# # #
# # #
# # # # Voorbeeld functies
# # # def submit_product(entry):
# # #     print("Productnaam:", entry.get())
# # #
# # # def submit_type(entry):
# # #     print("Producttype:", entry.get())
# # #
# # # def submit_amount(entry):
# # #     try:
# # #         amount = int(entry.get())
# # #         print("Aantal:", amount)
# # #     except ValueError:
# # #         print("Geen geldig getal!")
# # #
# # #
# # # # Maak meerdere entries met hun knoppen
# # # entry1 = make_entry_with_button(app, "Product:", submit_product)
# # # entry2 = make_entry_with_button(app, "Type:", submit_type)
# # # entry3 = make_entry_with_button(app, "Aantal:", submit_amount)
# # #
# # # app.mainloop()
# #
# #
# # import customtkinter as ctk
# #
# # class App(ctk.CTk):
# #     def __init__(self):
# #         super().__init__()
# #         self.geometry("400x400")
# #         self.font = ("Arial", 14)
# #
# #         # Product OptionMenu
# #         self.product_menu = ctk.CTkOptionMenu(
# #             self, values=["Product A", "Product B"], command=lambda _: self.check_product()
# #         )
# #         self.product_menu.pack(pady=5)
# #         self.product_menu.configure(takefocus=True)  # zodat Tab kan
# #         self.product_menu.focus_set()  # start focus hier
# #
# #         # Check product knop
# #         self.check_product_button = ctk.CTkButton(self, text="Check Product", command=self.check_product)
# #         self.check_product_button.pack(pady=5)
# #         self.check_product_button.configure(takefocus=True)
# #
# #         # Aantal invoer
# #         self.amount_entry = ctk.CTkEntry(self)
# #         self.amount_entry.pack(pady=5)
# #         self.amount_entry.configure(takefocus=True)
# #
# #         self.check_amount_button = ctk.CTkButton(self, text="Check Aantal", command=self.check_amount)
# #         self.check_amount_button.pack(pady=5)
# #         self.check_amount_button.configure(takefocus=True)
# #
# #         # Bind Enter globally
# #         self.bind_all("<Return>", self.handle_enter)
# #
# #     def handle_enter(self, event):
# #         widget = event.widget
# #         if widget == self.product_menu or widget == self.check_product_button:
# #             self.check_product()
# #         elif widget == self.amount_entry or widget == self.check_amount_button:
# #             self.check_amount()
# #
# #     def check_product(self):
# #         print(f"Product geselecteerd: {self.product_menu.get()}")
# #
# #     def check_amount(self):
# #         print(f"Aantal ingevoerd: {self.amount_entry.get()}")
# #
# # app = App()
# # app.mainloop()
#
#
# import customtkinter as ctk
#
# class App(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("400x300")
#         self.font = ("Arial", 14)
#
#         # Product OptionMenu
#         self.product_menu = ctk.CTkOptionMenu(
#             self, values=["Product A", "Product B"]
#         )
#         self.product_menu.pack(pady=5)
#
#         # Check product knop
#         self.check_product_button = ctk.CTkButton(self, text="Check Product", command=self.check_product)
#         self.check_product_button.pack(pady=5)
#
#         # Aantal invoer
#         self.amount_entry = ctk.CTkEntry(self)
#         self.amount_entry.pack(pady=5)
#
#         self.check_amount_button = ctk.CTkButton(self, text="Check Aantal", command=self.check_amount)
#         self.check_amount_button.pack(pady=5)
#
#         # Bind Enter globally
#         self.bind_all("<Return>", self.handle_enter)
#
#     def handle_enter(self, event):
#         widget = event.widget
#         # OptionMenu werkt via de knop ernaast
#         if widget == self.product_menu or widget == self.check_product_button:
#             self.check_product()
#         elif widget == self.amount_entry or widget == self.check_amount_button:
#             self.check_amount()
#
#     def check_product(self):
#         print(f"Product geselecteerd: {self.product_menu.get()}")
#
#     def check_amount(self):
#         print(f"Aantal ingevoerd: {self.amount_entry.get()}")
#
# app = App()
# app.mainloop()
#


import customtkinter as ctk

PRODUCT_CONFIG = {
    "Product A": {"types": ["Type 1", "Type 2"]},
    "Product B": {"types": ["Type 3", "Type 4"]},
}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Toetsenbordvriendelijke selectie")
        self.geometry("400x300")
        self.font = ("Arial", 14)

        self.selected_product = ctk.StringVar(value="")
        self.selected_type = ctk.StringVar(value="")

        self.load_settings_screen()

    def load_settings_screen(self):
        ctk.CTkLabel(self, text="Selecteer productielijn", font=self.font).pack(pady=5)

        # Product radiobuttons
        for product in PRODUCT_CONFIG.keys():
            r = ctk.CTkRadioButton(
                self,
                text=product,
                variable=self.selected_product,
                value=product,
                command=self.reset_type_selection,
                font=self.font
            )
            r.pack(anchor="w", padx=20)

        self.check_product_button = ctk.CTkButton(
            self,
            text="Check Product",
            font=self.font,
            command=self.check_product
        )
        self.check_product_button.pack(pady=5)
        self.check_product_button.bind("<Return>", lambda e: self.check_product())

        ctk.CTkLabel(self, text="Selecteer type", font=self.font).pack(pady=5)
        self.type_frame = ctk.CTkFrame(self)
        self.type_frame.pack(pady=5)

        self.check_type_button = ctk.CTkButton(
            self,
            text="Check Type",
            font=self.font,
            command=self.check_type,
            state="disabled"
        )
        self.check_type_button.pack(pady=5)
        self.check_type_button.bind("<Return>", lambda e: self.check_type())

    def reset_type_selection(self):
        # Wis eerdere type-buttons
        for widget in self.type_frame.winfo_children():
            widget.destroy()

        # Maak nieuwe type-buttons
        product = self.selected_product.get()
        self.selected_type.set("")
        for type_name in PRODUCT_CONFIG[product]["types"]:
            r = ctk.CTkRadioButton(
                self.type_frame,
                text=type_name,
                variable=self.selected_type,
                value=type_name,
                font=self.font
            )
            r.pack(anchor="w", padx=20)

        self.check_type_button.configure(state="normal")

    def check_product(self):
        print("Gekozen product:", self.selected_product.get())

    def check_type(self):
        print("Gekozen type:", self.selected_type.get())


if __name__ == "__main__":
    app = App()
    app.mainloop()

