import customtkinter as ctk
from tkinter import messagebox


class AssemblyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Assemblagelijn Controleren")
        self.geometry("700x400")

        self.current_screen = None
        self.show_start_screen()  # Begin met het opstartscherm

    def show_start_screen(self):
        """Het opstartscherm weergeven."""
        self.clear_screen()

        label = ctk.CTkLabel(self, text="Welkom bij de Assemblagelijn Controleren!", font=("Arial", 24))
        label.pack(pady=20)

        start_button = ctk.CTkButton(self, text="Start Configuratie", command=self.show_config_screen)
        start_button.pack(pady=20)

    def show_config_screen(self):
        """Het configuratiescherm weergeven."""
        self.clear_screen()

        label = ctk.CTkLabel(self, text="Configureer de Assemblagelijn", font=("Arial", 18))
        label.pack(pady=20)

        # Keuzelijst voor het type sensor
        sensor_types = ["Sensor A", "Sensor B", "Sensor C"]
        self.sensor_type_var = ctk.StringVar(value=sensor_types[0])  # default
        sensor_dropdown = ctk.CTkOptionMenu(self, variable=self.sensor_type_var, values=sensor_types)
        sensor_dropdown.pack(pady=10)

        # Aantal sensoren invoeren
        self.num_sensors_var = ctk.StringVar()
        num_sensors_label = ctk.CTkLabel(self, text="Aantal sensoren:")
        num_sensors_label.pack(pady=10)
        num_sensors_entry = ctk.CTkEntry(self, textvariable=self.num_sensors_var)
        num_sensors_entry.pack(pady=10)

        # Verzend gegevens knop
        submit_button = ctk.CTkButton(self, text="Verzend Gegevens", command=self.submit_config)
        submit_button.pack(pady=10)

        # Start en stop knoppen
        start_button = ctk.CTkButton(self, text="Start Assemblagelijn", command=self.start_assembly)
        start_button.pack(pady=10)

        stop_button = ctk.CTkButton(self, text="Stop Assemblagelijn", command=self.stop_assembly)
        stop_button.pack(pady=10)

    def show_assembly_in_progress(self):
        """Het scherm weergeven wanneer de assemblagelijn bezig is."""
        self.clear_screen()

        label = ctk.CTkLabel(self, text="Assemblagelijn in werking...", font=("Arial", 18))
        label.pack(pady=20)

        # Voeg hier de voortgangsbalk of andere indicatoren toe

    def show_completion_screen(self):
        """Het scherm weergeven wanneer de assemblagelijn is voltooid."""
        self.clear_screen()

        label = ctk.CTkLabel(self, text="Assemblagelijn voltooid!", font=("Arial", 18))
        label.pack(pady=20)

        # Toon resultaatdata
        result_label = ctk.CTkLabel(self, text="Aantal verwerkte sensoren: 10")  # Dit zou dynamisch moeten zijn
        result_label.pack(pady=10)

    def clear_screen(self):
        """Verwijder het huidige scherm om het te vervangen door een nieuw scherm."""
        for widget in self.winfo_children():
            widget.destroy()

    def submit_config(self):
        """Verzend de gegevens naar de Arduino."""
        sensor_type = self.sensor_type_var.get()
        num_sensors = self.num_sensors_var.get()

        # Validatie van invoer
        try:
            num_sensors = int(num_sensors)
            if num_sensors <= 0 or num_sensors > 500:
                raise ValueError("Aantal sensoren moet tussen 1 en 500 liggen.")
            print(f"Sensor Type: {sensor_type}, Aantal sensoren: {num_sensors}")
            # Verstuur naar Arduino hier (bijvoorbeeld via ser.write() als je verbinding hebt)
        except ValueError as e:
            messagebox.showerror("Fout", f"Fout bij invoer: {e}")

    def start_assembly(self):
        """Start de assemblagelijn."""
        self.show_assembly_in_progress()

    def stop_assembly(self):
        """Stop de assemblagelijn."""
        self.show_completion_screen()


if __name__ == "__main__":
    app = AssemblyApp()
    app.mainloop()
