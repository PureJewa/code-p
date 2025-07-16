import serial
import customtkinter as ctk
import time
from PIL import Image
import os
from threading import Thread, Lock

class AssemblyLineApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.time_per_sensor = 120  # Stel in op 5 seconden per sensor (dit kan later instelbaar worden gemaakt)
        self.rounded_estimated_time = ctk.IntVar(value=0)
        self.progress = ctk.IntVar(value=0)
        self.ok_button = ctk.CTkButton
        self.on_ok_pressed = ctk.CTkButton
       # self.status_label = ctk.CTkLabel(content_frame)
        self.ser = None  # Seriële verbinding
        self.lock = Lock()  # Voor threadveiligheid
        self.num_sensors_var = ctk.StringVar(value= "")
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
        # Bestandspad controleren
        file_path = r"C:\Users\Jelle\PycharmProjects\pythonProject\logo.png"
        if not os.path.exists(file_path):
            print("Fout: Afbeelding niet gevonden:", file_path)
            return

        # Laad een afbeelding
        self.image = ctk.CTkImage(
            dark_image=Image.open(file_path),   # Voor donkere modus
            size=(100, 100)  # Optioneel: grootte aanpassen
        )
        self.image_label = ctk.CTkLabel(self.sidebar, text="", image=self.image)
        self.image_label.pack(pady=20)
        ctk.CTkButton(self.sidebar, text="Start", command=self.start_screen).pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Instellingen", command=self.show_settings_screen, state="disabled").pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Assemblagelijn", command=self.show_working_screen, state="disabled").pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Klaar", command=self.end_screen, state="disabled").pack(pady=5)
        ctk.CTkButton(self.sidebar, text="Data", command= self.show_data_screen).pack(pady=5)
        # Start met het startscherm
        self.start_screen()
    def show_data_screen(self):
        self.clear_screen()
        ctk.CTkButton(self.content_frame, text="Laat data zien", command=self.getData).pack(pady=5)\

    def getData(self):
        ctk.CTkLabel(self.content_frame, text="Mooie data").pack(pady=5)
    def clear_screen(self):
        """Verwijder alle widgets uit het content_frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def connect_to_arduino(self):
        """Verbind met Arduino"""
        try:
            with self.lock:
                self.ser = serial.Serial('COM3', 9600)
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
                self.ser.write("START\n".encode())
                self.show_status("Assemblagelijn gestart.", "green")
            except Exception as e:
                self.show_status(f"Fout: {e}", "red")
        else:
            self.show_status("Geen verbinding met Arduino.", "red")

    def stop_assembly(self):
        """Stop de assemblagelijn"""
        if self.ser:
            try:
                self.ser.write("STOP\n".encode())
                self.show_status("Assemblagelijn gestopt.", "orange")
            except Exception as e:
                self.show_status(f"Fout: {e}", "red")
        else:
            self.show_status("Geen verbinding met Arduino.", "red")

    def show_status(self, text, color):
        """Toon een statusbericht"""
        status_label = ctk.CTkLabel(self.content_frame, text=text, text_color=color, font=("Arial", 14))
        status_label.pack(pady=5)

    def assembly_selected(self):
        """Controleer of een assemblagelijn is geselecteerd en schakel de knoppen in."""
        if self.selected_line.get() == "lijn_1":
            self.sidebar.winfo_children()[2].configure(state="normal")
            self.sidebar.winfo_children()[3].configure(state="normal")
            self.sidebar.winfo_children()[4].configure(state="normal")
        else:
            self.sidebar.winfo_children()[2].configure(state="disabled")
            self.sidebar.winfo_children()[3].configure(state="disabled")
            self.sidebar.winfo_children()[4].configure(state="disabled")

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
        self.assembly_selected(),
        self.start_screen()

    def update_entry(self, text):
        """Werk het invoerveld bij op basis van toetsenblokinvoer."""
        self.current_value = self.num_sensors_var.get()
        if text == "C":
            # Wis het veld
            self.clear_screen()
            self.num_sensors_var.set("")
            self.reset_labels()
            self.status_label = ctk.CTkLabel(self.content_frame, text=" ", font=("Arial", 14))
            self.show_settings_screen()
        elif text == "OK":

            self.send_to_arduino(self.sensor_type_dropdown.get(), self.num_sensors_var.get())
            self.update_estimated_time()
        else:
            # Voeg de ingevoerde waarde toe
            self.num_sensors_var.set(current_value + text)
           # self.update_estimated_time()

    def reset_labels(self):
        """Reset de tekst van relevante labels."""
        self.num_sensors_var.set("")  # Reset het aantal sensoren
        #self.status_label.configure(text="")  # Reset de statuslabel
        #self.status_label.pack_forget() # Reset foutmelding
    def update_estimated_time(self):
        """Bereken en toon de geschatte tijd op basis van het aantal sensoren."""
        try:
            num_sensors = int(self.num_sensors_var.get())
            if 600 > num_sensors > 0:
                estimated_time = num_sensors * self.time_per_sensor / 3600
                rounded_estimated_time = round(estimated_time, 2)
                # Update status_label
                status_label.configure(text=f"Geschatte tijd: {rounded_estimated_time} uur")
                self.status_label.pack()
                return rounded_estimated_time
            else:
                self.status_label.configure(text="Voer een geldig aantal sensoren in.")
        except ValueError:
            self.status_label.configure(text="Voer een geldig aantal sensoren in.")
    def validate_input(self):
        """Controleer of de invoer geldig is."""
        try:
            value = int(self.num_sensors_var.get())
            if 600 > value > 0:  # Controleer of het een positief getal is
                self.ok_button.configure(state="normal")
            else:
                self.ok_button.configure(state="disabled")
        except ValueError:
            self.ok_button.configure(state="disabled")

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

        # Functie om invoer te valideren

        # Koppel validatie aan veranderingen in invoer
        self.num_sensors_var.trace("w", lambda *args: self.validate_input())

        # Toetsenblokknoppen
        buttons = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("C", 3, 0), ("0", 3, 1), ("OK", 3, 2),
        ]

        for text, row, col in buttons:
            if text == "OK":
                self.ok_button = ctk.CTkButton(
                    keypad_frame, text=text, state="disabled",
                    command=lambda: self.update_entry("OK")
                )
                self.ok_button.grid(row=row, column=col, padx=5, pady=5)
            else:
                ctk.CTkButton(
                    keypad_frame, text=text,
                    command=lambda t=text: self.update_entry(t)
                ).grid(row=row, column=col, padx=5, pady=5)

        # Bereken geschatte tijd
        try:
            self.update_entry(text)
            num_sensors = int(self.num_sensors_var.get())
            estimated_time = num_sensors * self.time_per_sensor / 3600
        except ValueError:
            estimated_time = "onbekend"  # Als er nog geen invoer is

        # Toon geschatte tijd
        self.status_label = ctk.CTkLabel(
            self.content_frame,
            text=f"Geschatte tijd: {estimated_time} uur",
            font=("Arial", 18)
        )
        self.status_label.pack(pady=10)

    def show_working_screen(self):
        """Toon voortgang van de assemblagelijn"""
        self.clear_screen()

        label = ctk.CTkLabel(self.content_frame, text="Assemblagelijn bezig...", font=("Arial", 24))
        label.pack(pady=20)

        num_sensors = int(self.num_sensors_var.get())
        estimated_time = num_sensors * self.time_per_sensor / 3600
        rounded_estimated_time = round(estimated_time, 2)
        self.time_label = ctk.CTkLabel(self.content_frame, text=f"Verwachte tijd: {rounded_estimated_time} uur", font=("Arial", 18))
        self.time_label.pack(pady=10)


        self.progress_bar = ctk.CTkProgressBar(self.content_frame, width=300)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        # Start simulatie in een aparte thread
        thread = Thread(target=self.run_assembly)
        thread.start()

    def run_assembly(self):
        """Voer de assemblagelijn uit"""
        total_items = int(self.num_sensors_var.get())
        for i in range(total_items):
            time.sleep(1)  # Simuleer werk
            progress = (i + 1) / total_items
            self.update_progress(progress, total_items - i - 1)

        self.end_screen()

    def update_progress(self, progress, remaining_time):
        """Update de voortgangsbalk en tijd"""
        self.progress_bar.set(progress)
        self.time_label.configure(text=f"Verwachte tijd: {remaining_time} seconden")

    def end_screen(self):
        """Toon eindscherm"""
        self.clear_screen()
        ctk.CTkLabel(self.content_frame, text="Assemblagelijn klaar!", font=("Arial", 24)).pack(pady=20)
        ctk.CTkButton(self.content_frame, text="Herstart", command=self.start_screen).pack(pady=20)


if __name__ == "__main__":
    app = AssemblyLineApp()
    app.mainloop()