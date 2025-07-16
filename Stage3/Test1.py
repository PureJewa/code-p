import serial
import customtkinter as ctk
import time
from threading import Thread, Lock

class AssemblyLineApp(ctk.CTk):
    SERIAL_PORT = 'COM3'
    START_COMMAND = 'START'
    STOP_COMMAND = 'STOP'
    TIME_PER_SENSOR = 120  # Stel in op 5 seconden per sensor (dit kan later instelbaar worden gemaakt)

    def __init__(self):
        super().__init__()
        self.ser = None  # Seriële verbinding
        self.lock = Lock()  # Voor threadveiligheid
        self.num_sensors_var = ctk.StringVar(value="")
        self.sensor_types = ['TD-Diver', 'Baro-Diver', 'Micro-Diver']
        self.selected_line = ctk.StringVar(value="none")
        self.setup_ui()

    def setup_ui(self):
        """Setup van de GUI"""
        self.title("Assemblagelijn Controller")
        self.geometry("800x480")

        # Hoofdframe
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_frame, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # Hoofdcontentframe
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Sidebar knoppen
        ctk.CTkButton(self.sidebar, text="Start", command=self.start_screen).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Instellingen", command=self.show_settings_screen).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Assemblagelijn", command=self.show_working_screen).pack(pady=10)
        ctk.CTkButton(self.sidebar, text="Klaar", command=self.end_screen).pack(pady=10)

        # Start met het startscherm
        self.start_screen()

    def clear_screen(self):
        """Verwijder alle widgets uit het content_frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def clear_status_labels(self):
        """Verwijder alle statuslabels uit het content_frame"""
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

    def connect_to_arduino(self):
        """Verbind met Arduino"""
        try:
            with self.lock:
                self.ser = serial.Serial(self.SERIAL_PORT, 9600)
                time.sleep(2)
            print("Verbonden met Arduino.")
            self.show_status("Verbonden met Arduino.", "green")
        except serial.SerialException as e:
            print(f"Verbindingsfout: {e}")
            self.show_status("Fout bij verbinden met Arduino.", "red")
            self.ser = None

    def send_to_arduino(self, sensor_type, num_sensors):
        """Stuur gegevens naar de Arduino"""
        try:
            num_sensors = int(num_sensors)
            if num_sensors <= 0 or num_sensors > 500:
                raise ValueError("Aantal sensoren moet tussen 1 en 500 liggen.")
        except ValueError as e:
            self.show_status(f"Fout: {e}", "red")
            return

        if self.ser:
            try:
                self.ser.write(f"{sensor_type},{num_sensors}\n".encode())
                self.show_status(f"Gegevens verzonden: {sensor_type}, {num_sensors}", "green")
            except Exception as e:
                print(f"Fout bij verzenden: {e}")
                self.show_status("Fout bij verzenden naar Arduino.", "red")
        else:
            self.show_status("Geen verbinding met Arduino.", "red")

    def start_assembly(self):
        """Start de assemblagelijn"""
        if self.ser:
            try:
                self.ser.write(self.START_COMMAND.encode())
                self.show_status("Assemblagelijn gestart.", "green")
            except Exception as e:
                self.show_status(f"Fout: {e}", "red")
        else:
            self.show_status("Geen verbinding met Arduino.", "red")

    def stop_assembly(self):
        """Stop de assemblagelijn"""
        if self.ser:
            try:
                self.ser.write(self.STOP_COMMAND.encode())
                self.show_status("Assemblagelijn gestopt.", "orange")
            except Exception as e:
                self.show_status(f"Fout: {e}", "red")
        else:
            self.show_status("Geen verbinding met Arduino.", "red")

    def show_status(self, text, color):
        """Toon een statusbericht"""
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=text, text_color=color)
        else:
            self.status_label = ctk.CTkLabel(self.content_frame, text=text, text_color=color, font=("Arial", 14))
            self.status_label.pack(pady=5)

    def start_screen(self):
        """Startscherm voor het kiezen van een lijn"""
        self.clear_screen()

        label = ctk.CTkLabel(self.content_frame, text="Kies de Assemblagelijn", font=("Arial", 24))
        label.pack(pady=5)

        ctk.CTkButton(
            self.content_frame, text="Diver",
            command=lambda: self.select_line("lijn_1"),
            fg_color="#0C955A" if self.selected_line.get() == "lijn_1" else "gray"
        ).pack(pady=10)

        ctk.CTkButton(
            self.content_frame, text="WIP",
            command=lambda: self.select_line("lijn_2"),
            fg_color="#0C955A" if self.selected_line.get() == "lijn_2" else "gray"
        ).pack(pady=10)

    def select_line(self, line):
        """Selecteer een lijn"""
        self.selected_line.set(line)
        self.start_screen()

    def update_entry(self, text):
        """Werk het invoerveld bij op basis van toetsenblokinvoer."""
        current_value = self.num_sensors_var.get()
        if text == "C":
            self.num_sensors_var.set("")
            self.show_settings_screen()
        elif text == "OK":
            self.send_to_arduino(self.sensor_type_dropdown.get(), self.num_sensors_var.get())
            self.update_estimated_time()
        elif text.isdigit():
            self.num_sensors_var.set(current_value + text)
            self.update_estimated_time()

    def update_estimated_time(self):
        """Bereken en toon de geschatte tijd op basis van het aantal sensoren."""
        try:
            num_sensors = int(self.num_sensors_var.get())
            if 0 < num_sensors < 500:
                estimated_time = num_sensors * self.TIME_PER_SENSOR / 3600
                rounded_estimated_time = round(estimated_time, 2)
                if not hasattr(self, 'status_label'):
                    self.status_label = ctk.CTkLabel(self.content_frame, font=("Arial", 14))
                    self.status_label.pack(pady=5)
                self.status_label.configure(text=f"Geschatte tijd: {rounded_estimated_time} uur")
            else:
                self.status_label.configure(text="Voer een geldig aantal sensoren in.")
        except ValueError:
            self.status_label.configure(text="Voer een geldig aantal sensoren in.")

    def show_settings_screen(self):
        """Instellingen voor een assemblagelijn."""
        self.clear_screen()

        # Titel
        label = ctk.CTkLabel(self.content_frame, text="Instellingen voor Assemblagelijn", font=("Arial", 15))
        label.pack(pady=5)

        # Dropdown voor sensor type
        ctk.CTkLabel(self.content_frame, text="Type sensor:").pack(pady=5)
        self.sensor_type_dropdown = ctk.CTkOptionMenu(self.content_frame, values=self.sensor_types)
        self.sensor_type_dropdown.pack(pady=5)

        # Numerieke invoer
        ctk.CTkLabel(self.content_frame, text="Aantal sensoren:").pack(pady=5)
        entry = ctk.CTkEntry(self.content_frame, textvariable=self.num_sensors_var, width=200)
        entry.pack(pady=5)

        # Container voor het toetsenblok
        keypad_frame = ctk.CTkFrame(self.content_frame)
        keypad_frame.pack(pady=5)

        # Toetsenblokknoppen
        buttons = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("C", 3, 0), ("0", 3, 1), ("OK", 3, 2),
        ]
        for (text, row, col) in buttons:
            button = ctk.CTkButton(keypad_frame, text=text, command=lambda t=text: self.update_entry(t))
            button.grid(row=row, column=col, padx=10, pady=10)

    def end_screen(self):
        """Laat eindscherm zien."""
        self.clear_screen()
        self.show_status("Assemblagelijn gestopt.", "red")
