import customtkinter as ctk
import csv
from PIL import Image
from threading import Thread
from Globals import *
from RPI_USB_COMM import *
serienummerPath = r"/home/code-p/share/serienummer.csv"
TypeSoortPath = r"/home/code-p/share/TypeSoort.csv"
class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")  # Zet het uiterlijk op "dark mode"
        ctk.set_default_color_theme("blue")  # Standaard kleurenthema

        #Frames instellen
        self.inhoudScherm = ctk.CTkFrame(self)
        self.hoofdScherm = ctk.CTkFrame(self)
        self.zijBalk = ctk.CTkFrame(self.hoofdScherm, width=200)
        #Frames om keypad te maken op scherm
        self.aantalKeypad = ctk.CTkFrame(self.inhoudScherm)
        self.serienummerKeypad = ctk.CTkFrame(self.inhoudScherm)

        self.running = ctk.BooleanVar(value=False)
        self.paused = ctk.BooleanVar(value=False)

        self.assemblageLabel = ctk.CTkLabel
        self.aantalDiverEntry = ctk.StringVar()
        self.serieLabel = ctk.CTkLabel(self.inhoudScherm, text="")

        self.aantalLabel = ctk.CTkLabel(self.inhoudScherm, text="")


        self.huidige_waarde = ""
        self.amount_done = 0
        self.estimated_time = ctk.IntVar(value=0)
        self.progress = ctk.IntVar(value=0)

        self.progress = 0
        self.aantalDiver = ctk.IntVar()
        self.serieNummer = ctk.CTkEntry
        self.serieNummerEntry = ctk.StringVar()
        self.ok_button = ctk.CTkButton(self.inhoudScherm, state="disabled")
        self.progress_bar = ctk.CTkProgressBar(self.inhoudScherm)
        self.setup_gui()
        self.stateAssembly = ctk.StringVar()
        self.serieNummer = None

    def setup_gui(self):
        # Instellingen voor het hoofdscherm
        self.title(titel)
        self.geometry(schermAfmetingen)

        # Hoofdscherm
        self.hoofdScherm = ctk.CTkFrame(self)
        self.hoofdScherm.pack(fill="both", expand=True)

        # Zijbalk
        self.zijBalk = ctk.CTkFrame(self.hoofdScherm, width=200)
        self.zijBalk.pack(side="left", fill="y", padx=10, pady=10)
        # Logo in zijbalk
        self.image = ctk.CTkImage(
            dark_image=Image.open(logo),
            size=(100, 100))
        self.image_label = ctk.CTkLabel(self.zijBalk,
                                        text="",
                                        image=self.image).pack()
        # Knoppen toevoegen aan zijbalk
        self.homeButton = ctk.CTkButton(self.zijBalk,
                                        text="Home",
                                        command=self.show_start_screen)
        self.homeButton.pack(pady=10)

        self.instellingButton = ctk.CTkButton(self.zijBalk,
                                              text="Instellingen",
                                              command=self.show_settings_screen,
                                              state="disabled")
        self.instellingButton.pack(pady=10)

        self.assemblyButton = ctk.CTkButton(self.zijBalk,
                                            text="Assemblagelijn",
                                            command=self.show_running_screen,
                                            state="disabled")
        self.assemblyButton.pack(pady=10)
        self.klaarButton = ctk.CTkButton(self.zijBalk,
                                         text="Klaar",
                                         command=self.show_end_screen,
                                         state="disabled")
        self.klaarButton.pack(pady=10)
        self.dataButton = ctk.CTkButton(self.zijBalk,
                                        text="Data",
                                        command=self.show_data_screen)
        self.dataButton.pack(pady=10)
        # Hoofdcontentframe
        self.inhoudScherm = ctk.CTkFrame(self.hoofdScherm)
        self.inhoudScherm.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        self.show_start_screen()


    def show_start_screen(self):
        # Startscherm
        self.clear_screen() #Scherm leeghalen JIC
        self.welkomTekst = ctk.CTkLabel(self.inhoudScherm,
                                        text="Welkom bij de Assemblagelijn Besturing",
                                        font=("Arial", 24)).pack(pady=20)
        self.selecteerTekst = ctk.CTkLabel(self.inhoudScherm,
                     text="Selecteer een assemblagelijn:",
                     font=("Arial", 18)).pack(pady=10)
        # Knoppen om assemblagelijn te selecteren
        self.diverButton = ctk.CTkButton(self.inhoudScherm,
                                         text="Diver",
                                         command=lambda: self.geselecteerdeAssemblage("Diver"))
        self.diverButton.pack(pady=10)
        self.dekaTeckButton = ctk.CTkButton(self.inhoudScherm,
                                            text="DekaTeck",
                                            command=lambda: self.geselecteerdeAssemblage("DekaTeck"))
        self.dekaTeckButton.pack(pady=10)
        self.WIPButton = ctk.CTkButton(self.inhoudScherm,
                                       text="WIP",
                                       command=lambda: self.geselecteerdeAssemblage("WIP"))
        self.WIPButton.pack(pady=10)

        # Plaatsing label, als knop is ingedrukt veranderd de tekst
        self.assemblageLabel = ctk.CTkLabel(self.inhoudScherm, text="", font=("Arial", 18))
        self.assemblageLabel.pack(pady=20)

    def show_settings_screen(self):
        self.clear_screen()
        # Tekst
        ctk.CTkLabel(self.inhoudScherm,
                     text="Type Diver:",
                     font=("Arial", 18)).pack(pady=1)
        # Frame voor de widgets
        self.optieFrame = ctk.CTkFrame(self.inhoudScherm)
        self.optieFrame.pack(pady=10, padx=10)

        # Opties voor het type Diver
        self.diverType = ctk.CTkOptionMenu(self.optieFrame,
                                           values=['Diver',
                                                    'CTD-Diver'],
                                                    command=self.update_diver_type_soort
                                                    )
        self.diverType.grid(row=0, column = 0)
        self.diverTypeSoort = ctk.CTkOptionMenu(self.optieFrame,
                                                values=['DI800', 'DI801', 'DI802', 'DI805', 'DI810'])

        self.diverTypeSoort.grid(row=0,column=1)
        # Tekst
        ctk.CTkLabel(self.inhoudScherm,
                     text="Serienummer:",
                     font=("Arial", 18)).pack(pady=1)
        # Invoerveld voor serienummer
        self.serieNummer = ctk.CTkEntry(self.inhoudScherm,
                                        textvariable=self.serieNummerEntry)
        self.serieNummer.pack(pady=1)
        # Knop om serienummer in te voeren
        self.create_serial_number_keyboard()
        # Tekst
        ctk.CTkLabel(self.inhoudScherm,
                     text="Aantal sensoren:",
                     font=("Arial", 18)).pack(pady=1)
        # Invoerveld voor aantal sensoren
        self.aantalDiver = ctk.CTkEntry(self.inhoudScherm,
                                        textvariable=self.aantalDiverEntry)
        self.aantalDiver.pack(pady=1)
        # Knoppen om aantal sensoren in te voeren
        self.create_amount_keyboard()
        # Tekst voor tijd
        self.aantalLabel = ctk.CTkLabel(self.inhoudScherm,
                                        text=f"Geschatte tijd: {totaalTijd} uren")
        self.aantalLabel.pack(pady=1)
    def update_diver_type_soort(self, text):

        if text == "Diver":
            nieuweWaarde = ['DI800', 'DI801', 'DI802', 'DI805', 'DI810']
        if text == "CTD-Diver":
            nieuweWaarde = ['DI281', 'DI282', 'DI283', 'DI284']

        self.diverTypeSoort.configure(values=nieuweWaarde)
        if nieuweWaarde:
            self.diverTypeSoort.set(nieuweWaarde[0])
    def create_amount_keyboard(self):

        #maak een frame voor het toetsenbord
        self.aantalKeypad = ctk.CTkFrame(self.inhoudScherm)
        self.aantalKeypad.pack(pady=10)

        # Knoppen om aantal in te voeren
        buttons = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("C", 3, 0), ("0", 3, 1), ("OK", 3, 2),
        ]
        #Ga over alle knoppen en voeg ze toe aan het frame. Geeft de tekst mee aan de functie
        for text, row, col in buttons:
            if text == "OK":
                knop = ctk.CTkButton(self.aantalKeypad,
                                     text=text,
                                     height=10,
                                     command=self.validate_aantal)
            elif text == "C":
                knop = ctk.CTkButton(self.aantalKeypad,
                                     text=text,
                                     height=10,
                                     command=self.clear_aantal)
            else:
                knop = ctk.CTkButton(self.aantalKeypad,
                                     text=text,
                                     height= 10,
                                     command=lambda t=text: self.update_aantal(t))
            knop.grid(row=row, column=col, padx=2, pady=2)


    def clear_aantal(self):
        self.aantalDiverEntry.set("")
        self.aantalLabel.configure(text=f"Geschatte tijd: 0 uren")
        self.assemblyButton.configure(state="disabled")
    def validate_aantal(self):

        if 0 < int(self.aantalDiverEntry.get()) < 500:
            self.assemblyButton.configure(state="normal")
            aantalSensoren = int(self.aantalDiverEntry.get())
            startSerieNummer = self.serieNummerEntry.get()
            self.geschatteTijd = round(aantalSensoren * tijdSensor / secondeInUur,2)
            self.aantalLabel.configure(text=f"Geschatte tijd: {self.geschatteTijd} uren")
            genereer_Type_csv(self.diverTypeSoort.get(), aantalSensoren)
            genereer_csv(startSerieNummer, aantalSensoren)

        else:
            self.aantalLabel.configure(text="Ongeldige invoer, voer een getal in.")
    def update_aantal(self, text):
        self.huidigeAantal = self.aantalDiverEntry.get()
        self.aantalDiverEntry.set(self.huidigeAantal + text)

    def create_serial_number_keyboard(self):
        # Maak een frame voor het toetsenbord
        self.serienummerKeypad = ctk.CTkFrame(self.inhoudScherm)
        self.serienummerKeypad.pack(pady=1)

        # Knoppen om serie in te voeren
        serieNummerKnoppen = [
            ("A", 0, 0), ("B", 0, 1), ("C", 0, 2), ("D", 0, 3), ("E", 0, 4), ("F", 0, 5), ("G", 0, 6), ("H", 0, 7), ("J", 0, 8), ("K", 0, 9), ("L", 0, 10),
            ("M", 1, 0), ("N", 1, 1), ("P", 1, 2), ("R", 1, 3), ("S", 1, 4), ("T", 1, 5), ("U", 1, 6), ("V", 1, 7), ("W", 1, 8), ("X", 1, 9), ("Y", 1, 10),
            ("Z", 2, 0), ("0", 2, 1), ("1", 2, 2), ("2", 2, 3), ("3", 2, 4), ("4", 2, 5), ("5", 2, 6), ("6", 2, 7), ("7", 2, 8), ("8", 2, 9), ("9", 2, 10),
            ("Clear", 3, 4), ("OK", 3, 6)
        ]
        self.serieLabel = ctk.CTkLabel(self.inhoudScherm,
                                        text = "")
        self.serieLabel.pack(pady=1)
        # Voeg knoppen toe aan het frame
        for text, row, col in serieNummerKnoppen:
            if text == "OK":
                # Wanneer 'OK' wordt ingedrukt, valideer de invoer en sluit het toetsenbord
                button = ctk.CTkButton(self.serienummerKeypad,
                                       text=text,
                                       width= 10,
                                       command=self.validate_serial_number)
            elif text == "Clear":
                # 'C' voor wissen van de invoer
                button = ctk.CTkButton(self.serienummerKeypad,
                                       text=text,
                                       width=10,
                                       command=self.clear_serial_number)
            else:
                # Voeg letter- of cijferknoppen toe
                button = ctk.CTkButton(self.serienummerKeypad,
                                       text=text,
                                       width= 45,
                                       command=lambda t=text: self.update_serial_number(t))
            button.grid(row=row, column=col, padx=3, pady=3)

    def update_serial_number(self, text):
        # Verkrijg de huidige invoer van het serienummer
        huidigeSerieNummer = self.serieNummerEntry.get()
        self.serieNummerEntry.set(huidigeSerieNummer + text)

    def clear_serial_number(self):
        # Wis het serienummer veld
        self.serieNummerEntry.set("")
        self.serieLabel.configure(text="")

    def validate_serial_number(self):
        # Valideer de ingevoerde serienummer
        try:
            startSerieNummer = self.serieNummerEntry.get()
            serial = startSerieNummer
            prefix = serial[:2]  # De eerste twee tekens (letters)
            number = int(serial[2:])  # De laatste drie cijfers als integer
            if len(serial) != 5:
                self.serieLabel.configure(text="Serienummer te lang, probeer het opnieuw.")
            first_letter = prefix[0]
            second_letter = prefix[1]
            if first_letter in "IOQ" or second_letter in "IOQ":
                self.serieLabel.configure(text ="Serienummer mag geen IOQ, probeer het opnieuw.")

            if number == 000:
                self.serieLabel.configure("Serienummer mag niet 000, probeer het opnieuw.")

            elif startSerieNummer:
                self.serienummerKeypad.destroy()  # Verwijder het toetsenbord na validatie
            else:
                self.serieLabel.configure(text="Ongeldig serienummer, probeer het opnieuw.")
        except:
            self.serieLabel.configure(text="Ongeldig serienummer, probeer het opnieuw.")


    def show_running_screen(self):

        self.clear_screen()
        self.aantalSensoren = int(self.aantalDiverEntry.get())
        ctk.CTkLabel(self.inhoudScherm, text="Assemblagelijn in werking...", font=("Arial", 18)).pack(pady=20)
        self.progressie = gedaan / int(self.aantalSensoren)
        self.aantalLabel = ctk.CTkLabel(self.inhoudScherm, text=f"Geschatte tijd: {self.progressie} uren")
        self.aantalLabel.pack(pady=5)
        self.klaarButton.configure(state="normal")
        self.progress_bar = ctk.CTkProgressBar(self.inhoudScherm)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        self.startButton = ctk.CTkButton(self.inhoudScherm, text="Start", command=self.start_assembly())
        self.startButton.pack(pady=10)
        self.stopButton = ctk.CTkButton(self.inhoudScherm, text="Pauze", command=self.toggle_pause)
        self.stopButton.pack(pady=10)



    def toggle_pause(self):
        self.paused = not self.paused  # Toggle de waarde
        self.stateAssembly.set("Hervat" if not self.paused else "Pauze")
        self.stopButton.configure(text="Hervat" if self.paused else "Pauze")

    def start_assembly(self):
        self.running = True
        Thread(target=self.run_assembly, daemon=True).start()

    def run_assembly(self):
        global gedaan
        aantalSensoren = int(self.aantalDiverEntry.get())
        while self.running:
            waarde = int(self.aantalDiverEntry.get())
            for i in range(waarde):
                if self.paused:
                    while self.paused:
                        time.sleep(0.5)
                    if not self.running:
                        break
                time.sleep(2)  # Simuleer werk
                gedaan += 1
                self.benodigdetijd = round((tijdSensor * (aantalSensoren - gedaan)) / secondeInUur,2)
                self.progressie = gedaan / int(aantalSensoren)
                self.aantalLabel.configure(text=f"Geschatte tijd: {self.benodigdetijd} uren")
                self.progress_bar.set(self.progressie)

            self.show_end_screen()
            self.progress = 0
            self.running = False

    def show_end_screen(self):
        self.clear_screen()
        self.klaarButton.configure(state="normal")
        ctk.CTkLabel(self.inhoudScherm, text="Assemblagelijn klaar.", font=("Arial", 24)).pack(pady=20)

    def show_data_screen(self):
        self.clear_screen()
        ctk.CTkLabel(self.inhoudScherm, text="Data van de Assemblagelijn", font=("Arial", 24)).pack(pady=20)
        ctk.CTkButton(self.inhoudScherm,
                      text="Laat data zien",
                      command=self.show_data).pack(pady=10)

    def show_data(self):
        ctk.CTkLabel(self.inhoudScherm, text="Mooie DATA!", font=("Arial", 18)).pack(pady=20)
    def geselecteerdeAssemblage(self, text):
        if text == "Diver":
            self.diverButton.configure(fg_color="#0C955A")
            self.dekaTeckButton.configure(fg_color="grey")
            self.WIPButton.configure(fg_color="grey")
            self.assemblageLabel.configure(text="Diver assemblagelijn geselecteerd.", text_color="white")
            self.instellingButton.configure(state="normal")

        if text == "DekaTeck":
            self.dekaTeckButton.configure(fg_color="#0C955A")
            self.diverButton.configure(fg_color="grey")
            self.WIPButton.configure(fg_color="grey")
            self.assemblageLabel.configure(text="Dekateck assemblagelijn geselecteerd.", text_color="white")
            self.instellingButton.configure(state="normal")

        if text == "WIP":
            self.WIPButton.configure(fg_color="#0C955A")
            self.dekaTeckButton.configure(fg_color="grey")
            self.diverButton.configure(fg_color="grey")
            self.assemblageLabel.configure(text="WIP geselecteerd.", text_color="red")
            self.instellingButton.configure(state="disabled")
            self.assemblyButton.configure(state="disabled")
            self.klaarButton.configure(state="disabled")

    def clear_screen(self):
        #Verwijder alle widgets uit het content_frame
        if self.inhoudScherm.winfo_children():
            for widget in self.inhoudScherm.winfo_children():
                widget.destroy()

def increment_serial_number(serial):
    """
    Verhoogt het serienummer met 1, rekening houdend met alfanumerieke logica.
    """
    prefix = serial[:2]
    number = int(serial[2:])

    if number == 999:
        number = 1
        second_letter = chr(ord(prefix[1]) + 1)
        if second_letter in "IOQ":
            second_letter = chr(ord(second_letter) + 1)
        if second_letter > "Z":
            second_letter = "A"
            first_letter = chr(ord(prefix[0]) + 1)
            if first_letter in "IOQ":
                first_letter = chr(ord(first_letter) + 1)
            if first_letter > "Z":
                raise ValueError("Serienummerbereik is uitgeput.")
            prefix = first_letter + second_letter
        else:
            prefix = prefix[0] + second_letter
    else:
        number += 1

    return f"{prefix}{number:03}"

def genereer_csv(startSerieNummer, aantalSensoren, bestandsnaam=serienummerPath):
    """
    Genereert een CSV-bestand met een reeks serienummers.
    """
    try:
        serienummers = [startSerieNummer]
        current_serial = startSerieNummer

        for _ in range(aantalSensoren - 1):
            current_serial = increment_serial_number(current_serial)
            serienummers.append(current_serial)

        # Schrijf de serienummers naar een CSV-bestand
        with open(bestandsnaam, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows([[s] for s in serienummers])

        print(f"CSV-bestand '{bestandsnaam}' is succesvol gegenereerd!")
    except Exception as e:
        print(f"Er is een hier fout opgetreden: {e}")


def genereer_Type_csv(StartTypeSoort, aantalSensoren, bestandsnaam=TypeSoortPath):
    """
    Genereert een CSV-bestand met een reeks serienummers.
    """
    try:
        # Maak een lijst met het gewenste aantal van StartTypeSoort
        TypeSoort = [StartTypeSoort] * aantalSensoren  # Lijst met herhaalde waarden

        # Schrijf de lijst naar een CSV-bestand
        with open(bestandsnaam, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows([[s] for s in TypeSoort])  # Schrijf elk element op een aparte regel

        print(f"CSV-bestand '{bestandsnaam}' is succesvol gegenereerd!")
    except Exception as e:
        print(f"Er is een fout opgetreden: {e}")

