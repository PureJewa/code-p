#** helperfunctions

from imports import *
from logic.config import *
from logic.validation.general import *
from logic.JsonHandler import  *
from logic.config import PRODUCT_CONFIG, DIVER, CTD, SERIE, ENKEL
# from arduinoComm import *
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
def find_all_devices():
    found_devices = {}
    ports = serial.tools.list_ports.comports()
    for name, info in DEVICES.items():
        match = next((p.device for p in ports if p.vid == info["vid"] and p.pid == info["pid"]), None)
        found_devices[name] = match
    return found_devices

def make_line(app):
    ctk.CTkFrame(app.main_frame, height=2, width=app.screen_width, fg_color="gray").pack(pady=1)

def reset_app(app):
    choice = app.product_menu.get()
    if app.is_set:
        print('test2')
        app.is_set = False
        for widget in app.main_frame.winfo_children():
            widget.destroy()
        app.load_settings_screen()
        app.product_menu.set(choice)
        app.product_menu.configure(fg_color='#1F6AA5')
        app.product_feedback.configure(text=f"")
        app.type_menu.configure(state="disabled", values=PRODUCT_CONFIG[choice]["types"])
        app.type_menu.set(PRODUCT_CONFIG[choice]["types"][0])  # Zet de eerste type als standaard
        app.check_type_button.configure(state="disabled")

def check_product(app, choice):
    app.selected_product = choice
    app.product_feedback.configure(text=f"{choice} geselecteerd", text_color='green')
    app.product_menu.configure(fg_color='green')
    app.type_menu.set(PRODUCT_CONFIG[choice]["types"][0])  # Zet de eerste type als standaard
    app.type_menu.configure(state="normal", values=PRODUCT_CONFIG[choice]["types"])
    app.check_type_button.configure(state="normal")
    # reset_app(app, choice)
    app.is_set = True

def check_type(app):
    selected_type = app.type_menu.get()
    if not app.selected_product:
        app.typeLabel.configure(text="Selecteer eerst een product", text_color="red")
        return
    app.type_menu.configure(fg_color="green")
    app.amount_entry.configure(state="normal")
    app.check_amount_button.configure(state="normal")

    app.typeLabel.configure(text=selected_type, text_color="green")
    app.typeLabel.pack()

def checkOrderNumber(app):
    app.person_entry.configure(state="normal")
    app.person_button.configure(state="normal")

def checkPerson(app):
    if app.person_entry is not None:
        app.segmented_button.configure(state="normal")

    else:
        ctk.CTkLabel(app.scrollable_frame, text="Geen persoon geselecteerd", text_color="red").pack(pady=10)
def verzamel_instellingen(app):
    if app.segmented_button.get() == "Controle":
        app.instellingen_data = {
            "Productielijn": app.selected_product,
            "Type": app.type_menu.get(),
            "Aantal": app.amount_entry.get(),
            "Productie modus": {
                "Modus"
                : app.production_mode if hasattr(app, "production_mode") else "Niet gekozen"
            },
            "Ordernummer": app.order_entry.get(),
            "Datum": app.date_entry.get(),
            "Naam medewerker": app.person_entry.get(),
        }

    if app.segmented_button.get() == "Besturing":
        app.instellingen_data = {
            "Productielijn": app.selected_product,
            "Type": app.type_menu.get(),
            "Aantal": app.amount_entry.get(),
            "Productie modus": {
                "Modus"
                : app.production_mode if hasattr(app, "production_mode") else "Niet gekozen"
            },
            "Ordernummer": app.order_entry.get(),
            "Datum": app.date_entry.get(),
            "Naam medewerker": app.person_entry.get(),
            "Instellingen OK": app.instellingen_ok.get(),
            "Checklist OK": {}
        }
        for item, value in app.checklist_vars.items():
            app.instellingen_data["Checklist OK"][item] = value.get()
    if app.production_mode == SERIE:
        start_serial = app.serial_entry.get().strip().upper()
        app.instellingen_data["Productie modus"]["Start Serienummer"] = start_serial

        serials = generate_serials(app.serial_entry.get().upper(), int(app.amount_entry.get()),
                                   PRODUCT_CONFIG[app.selected_product]["serial_pattern"])
        if serials:
            app.instellingen_data["Productie modus"]["Eind Serienummer"] = serials[-1]
            app.instellingen_data["Productie modus"]["Serienummers"] = "\n".join(serials)

    elif app.production_mode == ENKEL:
        serials = app.serial_textbox.get("1.0", "end").strip().splitlines()
        serials = [s.strip().upper() for s in serials if s.strip()]
        app.instellingen_data["Productie modus"]["Serienummers"] = "\n".join(serials)


def format_instellingen_voor_weergave(app):
    regels = []
    for key, value in app.instellingen_data.items():
        if key == "Productie modus":
            modus_data = value
            regels.append(f"{key}: {modus_data.get('Modus', 'Niet gekozen')}")

            if modus_data["Modus"] == SERIE:
                regels.append(f"Start Serienummer: {modus_data.get('Start Serienummer', '')}")
                regels.append(f"Eind Serienummer: {modus_data.get('Eind Serienummer', '')}")
                """
                regels.append("Serienummers:")
                serienummers = modus_data.get("Serienummers", "")
                regels.extend(serienummers.split("\n"))
                """
            elif modus_data["Modus"] == ENKEL:
                regels.append("Serienummers:")
                serienummers = modus_data.get("Serienummers", "")
                regels.extend(serienummers.split("\n"))

        else:
            regels.append(f"{key}: {value}")
        # Voeg een lege regel toe voor betere leesbaarheid
        regels.append("------------------------------------------------------")
    return "\n".join(regels)


def switch_screen(app, name):
    if name != "Instellingen":
        try:
            verzamel_instellingen(app)
            product = app.instellingen_data.get("Productielijn", "")
            save_settings(product, app.instellingen_data)
        except Exception as e:
            print("Fout bij verzamelen instellingen:", e)

    for widget in app.main_frame.winfo_children():
        widget.forget()

    if name == "Instellingen":
        app.load_settings_screen()
        app.segmented_button.set("Instellingen")
    elif name == "Controle":
        app.load_controle_screen()
        app.segmented_button.set("Controle")
    elif name == "Besturing":
        app.load_besturing_screen()
        app.segmented_button.set("Besturing")

def increase_font_size(app):
    app.font_size += 1
    app.font.configure(size=app.font_size)
    _update_widget_fonts(app, app.topbar)
    _update_widget_fonts(app, app.centrebar)
    _update_widget_fonts(app, app.main_frame)
def decrease_font_size(app):
    app.font_size -= 1
    app.font.configure(size=app.font_size)
    _update_widget_fonts(app, app.topbar)
    _update_widget_fonts(app, app.centrebar)
    _update_widget_fonts(app, app.main_frame)
def _update_widget_fonts(app, widget):
    # Recursief alle widgets in de boom doorlopen
    for child in widget.winfo_children():
        try:
            # Probeer het font attribuut te veranderen als mogelijk
            child.configure(font=app.font)
            if isinstance(child, (ctk.CTkEntry, ctk.CTkTextbox)):
                new_height = 15 + 10  # Aangepaste formule voor hoogte
                child.configure(height=new_height)
            if isinstance(child, ctk.CTkProgressBar):
                new_width = int(app.screen_width * 0.25) + (app.font_size * 15)
                child.configure(width=new_width)
        except Exception:
            pass

        except Exception:
            # Niet alle widgets accepteren font; negeer fouten
            pass
def Barcode_to_raspberry():
    try:
        # Probeer verbinding te maken met de poort
        barcodeSer = serial.Serial(ScannerPort, baudrate, timeout)
        print(f"Verbonden met {portScanner}. Wachten op gegevens...")

        # Wachten op data van de scanner
        barcodeData = barcodeSer.readline().decode('utf-8').strip()
        barcodeSer.close()

        if data:
            print(f"Barcode gescand op {ScannerPort}: {barcodeData}")
            return True
        else:
            print(f"Geen gegevens ontvangen van {ScannerPort}.")
    except Exception as e:
        print(f"Fout bij {ScannerPort}: {e}")

def bevestig(app):
    instellingen_ok = app.instellingen_ok.get()
    checklist_waarden = {k: v.get() for k, v in app.checklist_vars.items()}
    send_command(f'PRODUCT:{app.product_menu.get()}')
    print(app.product_menu.get())
    print("Instellingen OK:", instellingen_ok)
    print("Checklistresultaten:")
    for item, value in checklist_waarden.items():
        print(f" - {item}: {'Ja' if value else 'Nee'}")



class CustomDateEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._popup = None
        self.bind("<Button-1>", self.show_calendar)
        self.configure(state="readonly")
        self.configure(state="normal")
        self.delete(0, tk.END)
        self.insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.configure(state="readonly")

    def show_calendar(self, event=None):
        if self._popup and self._popup.winfo_exists():
            self._popup.destroy()

        self._popup = tk.Toplevel(self)
        self._popup.wm_overrideredirect(True)
        self._popup.attributes('-topmost', 'true')

        x = self.winfo_rootx()
        y = self.winfo_rooty() - 250  # ruim genoeg bovenin

        self._popup.geometry(f"+{x}+{y}")

        font_lg = tkfont.Font(family="Arial", size=20)
        cal = Calendar(self._popup, date_pattern="dd-mm-yyyy", font=font_lg)
        cal.pack()

        cal.bind("<<CalendarSelected>>", lambda e: self._on_date_selected(cal.selection_get()))
    def _on_date_selected(self, date):
        self.configure(state="normal")
        self.delete(0, tk.END)
        self.insert(0, date.strftime("%d-%m-%Y"))
        self.configure(state="readonly")
        if self._popup:
            self._popup.destroy()

