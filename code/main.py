#**Main
# test
from imports import *
from gui.widgets.widget import *
from logic.config import *
from logic.JsonHandler import *
from logic.validation.general import *
from helperfunctions import *
from logic.config import PRODUCT_CONFIG, logo_image, OFF_IMAGE, DEVICES, device_ports
from helperfunctions import *
from arduinoComm import *
from serial_simulator import SerialSimulatorWindow
from constants import *



class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title(app_title)
        self.overrideredirect(True)  # Verwijdert titelbalk
        #MISSCHIEN IS DIT NODIG VOOR LINUX, CHECK DIT!
        # self.attributes('-fullscreen', True)

        # Zet de grootte van het venster gelijk aan de schermresolutie
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        #Variable instellen
        self.instellingen_data = {}
        self.status_widgets = {}
        self.selected_product = None
        self.is_set = False
        self.amount_done = 0

        #Font grootte
        self.font_size = 15
        self.font = ctk.CTkFont(family=font, size=self.font_size)

        #Check of Arduino is gestart
        if initialize_serial():
            threading.Thread(target=serial_read_loop, daemon=True).start()
            self.after(100, self.poll_arduino)

        #Basis scherm laden
        self.CreateBaseLayout()
        # Check welke apparaten missen
        for device_name, port in device_ports.items():
            if port is None:
                self.warningNoDevice(device_name)

        #Eerste scherm laden
        switchScreen(self, "Instellingen")

    def createWarningNoDeviceWindows(self):
        """
        Maakt een waarschuwing venster aan als een apparaat niet is gevonden.
        Returns: Het waarschuwing venster

        """
        warning_window = ctk.CTkToplevel(self)
        warning_window.title(warning_window_title)
        warning_window.geometry(warning_window_size)
        warning_window.resizable(False, False)
        warning_window.attributes('-topmost', True)
        warning_window.protocol("WM_DELETE_WINDOW", lambda: None)

        return warning_window
    def warningNoDevice(self, device):
        """
        Toont een waarschuwing venster als een apparaat niet is gevonden.
        Zorgt ervoor dat de gebruiker kan kiezen om opnieuw te proberen of het venster te sluiten.

        Args
            device: Het apparaat dat niet is gevonden.
        """
        warning_window = self.createWarningNoDeviceWindows()

        ctk.CTkLabel(warning_window, text=warning_window_lable.format(device), font=self.font).pack(pady=20)
        ctk.CTkButton(warning_window, text=warning_window_button_ok, command=warning_window.destroy).pack(pady=10)
        ctk.CTkButton(warning_window, text=warning_window_button_retry, command=lambda: self.RetryInitDevice(device, warning_window)).pack(pady=10)

    def RetryInitDevice(self, device, warning_window):
        """
        Probeer opnieuw het apparaat te initialiseren.
        Args
            device: Het apparaat dat opnieuw moet worden geïnitialiseerd.
            warning_window:
        """
        # sluit de warning window
        warning_window.destroy()

        # probeer opnieuw specifiek voor dit device
        new_ports = init_device()  # haalt alle devices op
        new_port = new_ports.get(device)

        if new_port is None:
            # nog steeds niet gevonden → toon opnieuw waarschuwing
            self.warningNoDevice(device)
        else:
            # gelukt → update de self.device_ports
            device_ports[device] = new_port

    def CreateBaseLayout(self):
        """
        Maakt de basis layout van de applicatie aan.
        Bovenste balk met logo, knoppen en navigatie
        En een hoofdframe voor de inhoud
        """
        #Maak boven frame
        self.topbar_frame = ctk.CTkFrame(self, height=topbar_height)
        self.topbar_frame.pack(fill="x", padx=top_bar_padding, pady=top_bar_padding)

        #Maak frames voor links midden rechts
        self.left_bar_frame = ctk.CTkFrame(self.topbar_frame)
        self.center_bar_frame = ctk.CTkFrame(self.topbar_frame)
        self.right_bar_frame = ctk.CTkFrame(self.topbar_frame)

        self.left_bar_frame.pack(side="left")
        self.center_bar_frame.pack(side="left", fill="x", expand=True)
        self.right_bar_frame.pack(side="right")

        #Laad knoppen en logo
        self.logo_image = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=top_bar_image_size)
        self.logo_label = ctk.CTkLabel(self.left_bar_frame, image=self.logo_image, fg_color="transparent", text="")

        self.increase_font_button = ctk.CTkButton(self.left_bar_frame, text="+", command=lambda: increase_font_size(self), width=50, height=30, font=(font, 15))
        self.decrease_font_button = ctk.CTkButton(self.left_bar_frame, text="-", command=lambda: decrease_font_size(self), width=50, height=30, font=(font, 15))

        self.off_image = ctk.CTkImage(light_image=OFF_IMAGE, dark_image=OFF_IMAGE, size=top_bar_image_size)
        self.off_button = ctk.CTkButton(self.right_bar_frame, image=self.off_image, command=self.quit, fg_color="transparent", text="", hover_color="gray20", width=50, height=50)

        # Segmented button for navigation
        self.segmented_button = ctk.CTkSegmentedButton(self.center_bar_frame, values=list(segmented_button_values), command=lambda value: switchScreen(self, value))

        #Laten zien op in het scherm
        self.logo_label.pack(side='left')
        self.increase_font_button.pack(side='top')
        self.decrease_font_button.pack(side='bottom')
        self.segmented_button.pack(expand=True, fill="x")
        self.off_button.pack()

        #Maak frame voor inhoud
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill="both", expand=True)
    def productWidgets(self):
        """"
        Maakt de widgets aan voor het selecteren van een product.
        Dropdown menu, knop om product te controleren, label voor feedback
        """
        # Label voor product selectie
        ctk.CTkLabel(self.main_frame, text=setting_screen_product_label_text, font=self.font).pack(pady=setting_screen_padding_block)

        # Maak dropdown aan
        self.product_menu = ctk.CTkOptionMenu(self.main_frame, values=list(PRODUCT_CONFIG.keys()), font=self.font, command=lambda _: reset_app(self))
        self.product_menu.pack(pady=setting_screen_padding_block)

        # Knop om product te controleren.
        self.check_product_button = ctk.CTkButton(self.main_frame, text=setting_screen_product_button_text, font=self.font, command=lambda: check_product(self, self.product_menu.get()))
        self.check_product_button.pack(pady=setting_screen_padding_block)

        # Label voor feedback, leeg bij start
        self.product_feedback = ctk.CTkLabel(self.main_frame, text="", font=self.font)
        self.product_feedback.pack(pady=setting_screen_padding)

    def typeWidgets(self):
        """
        Maak de widgets aan voor het selecteren van een type.
        """
        #Header voor type selectie
        ctk.CTkLabel(self.main_frame, text=setting_screen_type_label_text, font=self.font).pack(pady=setting_screen_padding_block)

        #Dropdown menu voor type selectie
        self.type_menu = ctk.CTkOptionMenu(self.main_frame, values=PRODUCT_CONFIG[self.product_menu.get()]["types"], state="disabled" , font=self.font)
        self.type_menu.pack(pady=setting_screen_padding_block)

        #Knop voor type check
        self.check_type_button = ctk.CTkButton(self.main_frame, text=setting_screen_type_button_text, command=lambda: check_type(self), state="disabled", font=self.font)
        self.check_type_button.pack(pady=setting_screen_padding_block)

        #Label voor type
        self.typeLabel = ctk.CTkLabel(self.main_frame, text="", font=self.font)
        self.typeLabel.pack(pady=setting_screen_padding)

    def amountWidgets(self):
        """
        Maak widgets aan voor het invoeren van een hoeveelheid.
        """
        # Header voor aantal
        ctk.CTkLabel(self.main_frame, text=setting_screen_amount_label_text, font=self.font).pack(pady=setting_screen_padding_block)

        # Invoerveld voor aantal
        self.amount_entry = ctk.CTkEntry(self.main_frame, state="disabled", font=self.font)
        self.amount_entry.pack(pady=setting_screen_padding_block)

        #Knop voor aantal check
        self.check_amount_button = ctk.CTkButton(self.main_frame, text=setting_screen_amount_button_text, command=self.check_amount, state="disabled", font=self.font)
        self.check_amount_button.pack(pady=setting_screen_padding_block)

        # Bind Enter in dit entry aan dezelfde command
        self.amount_entry.bind("<Return>", lambda event: self.check_amount())

        self.amount_feedback = ctk.CTkLabel(self.main_frame, text="", font=self.font)
        self.amount_feedback.pack(pady=setting_screen_padding)

    def soortProductieWidgets(self):
        """
        Maak widgets aan voor het selecteren van de productiemodus.
        """
        # Productiemodus selectie, laat de gebruiker kiezen tussen reeks productie (serie) of individueel productie (enkel)
        ctk.CTkLabel(self.main_frame, text=setting_screen_soort_productie_label_text, font=self.font).pack(pady=setting_screen_padding_block)

        self.series_button = ctk.CTkButton(self.main_frame, text=setting_screen_series_button_text, command=lambda: self.set_mode(SERIE),state="disabled", font=self.font)
        self.series_button.pack(pady=setting_screen_padding_block)

        self.single_button = ctk.CTkButton(self.main_frame, text=setting_screen_single_button_text, command=lambda: self.set_mode(ENKEL),state="disabled", font=self.font)
        self.single_button.pack(pady=setting_screen_padding_block)

        self.serial_label = ctk.CTkLabel(self.main_frame, text="", font=self.font)
        self.serial_label.pack(pady=setting_screen_padding_block)

        # Maak de invoervelden aan, ze worden eerst verborgen zodat de juiste kan worden getoond op basis van de gekozen productiemodus
        self.serial_entry = ctk.CTkEntry(self.main_frame, font=self.font)
        self.serial_entry.pack_forget()  # eerst verbergen
        self.serial_entry.bind("<Return>", lambda event: self.serial())

        self.serial_textbox = ctk.CTkTextbox(self.main_frame, height=100, font=self.font)
        self.serial_textbox.pack_forget() # eerst verbergen
        self.serial_textbox.bind("<Return>", lambda event: self.serial())

        # Knop om serienummers te controleren, ook deze wordt eerst verborgen om verwarring te voorkomen
        self.check_serial_button = ctk.CTkButton(self.main_frame, text=setting_screen_check_serial_button_text,command=self.serial, font=self.font)
        self.check_serial_button.pack_forget()

        self.serial_feedback = ctk.CTkLabel(self.main_frame, text="", font=self.font)
        self.serial_feedback.pack(pady=setting_screen_padding)

        # Laad de laatste serienummer uit het JSON-bestand
        instellingen_data = load_settings(product=self.selected_product)
        productie_modus = instellingen_data.get("Productie modus", {})
        laatste_serial = productie_modus.get("Eind Serienummer", "")

        if laatste_serial:
            self.serial_entry.delete(0, "end")
            self.serial_entry.insert(0, laatste_serial)


    def orderNummerWidgets(self):
        # Ordernummer invoer
        self.order_label = ctk.CTkLabel(self.main_frame, text=setting_screen_ordernumber_label_text, font=self.font)
        self.order_label.pack(pady=setting_screen_padding_block)

        self.order_entry = ctk.CTkEntry(self.main_frame, state="disabled", font=self.font)
        self.order_entry.pack(pady=setting_screen_padding_block)
        self.order_entry.bind("<Return>", lambda event: self.checkOrderNumber())

        self.order_button = ctk.CTkButton(self.main_frame, text=setting_screen_ordernumber_button_text, state="normal", command=lambda: checkOrderNumber(self), font=self.font)
        self.order_button.pack(pady=setting_screen_padding_block)

        self.order_feedback = ctk.CTkLabel(self.main_frame, text="", font=self.font)
        self.order_feedback.pack(pady=setting_screen_padding)

    def datumWidgets(self):
        """
        Maakt widgets aan voor het invoeren van de datum.
        """
        self.date_label = ctk.CTkLabel(self.main_frame, text=setting_screen_date_label_text, font=self.font)
        self.date_label.pack(pady=setting_screen_padding_block)
        self.date_entry = CustomDateEntry(self.main_frame, font=self.font, state="disabled")
        self.date_entry.pack(pady=setting_screen_padding_block)

    def personWidgets(self):
        """
        Maak widgets aan voor het invoeren van de naam van de medewerker.
        """
        self.person_label = ctk.CTkLabel(self.main_frame, text=setting_screen_person_label_text, font=self.font)
        self.person_label.pack(pady=setting_screen_padding_block)

        self.person_entry = ctk.CTkEntry(self.main_frame, state="disabled", font=self.font)
        self.person_entry.pack(pady=setting_screen_padding_block)
        self.person_entry.bind("<Return>", lambda event: self.checkPerson())

        self.person_button = ctk.CTkButton(self.main_frame, text=setting_screen_person_button_text, state="disabled", command= lambda: checkPerson(self), font=self.font)
        self.person_button.pack(pady=setting_screen_padding_block   )


    def loadSettingsScreen(self):
        """
        Laad het instellingen scherm.
        Maakt alle widgets aan voor het instellingen scherm.
        """
        self.productWidgets()
        make_line(self)

        self.typeWidgets()
        make_line(self)

        self.amountWidgets()
        make_line(self)

        self.soortProductieWidgets()
        make_line(self)

        self.orderNummerWidgets()
        make_line(self)

        self.datumWidgets()
        make_line(self)

        self.personWidgets()

    def show_device_status(self, device_ports, control_frame):
        for device_name, port in device_ports.items():
            # Maak een frame voor het apparaat + statuslampje
            device_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
            device_frame.pack(pady=5, fill="x")

            # Zet een statuslampje met tekst
            status_color = "green" if port else "red"
            status_text = "🟢 Verbonden" if port else "🔴 Niet gevonden"
            # Apparaatnaam + poort
            device_label = ctk.CTkLabel(device_frame, text=f"{device_name}:", font=self.font)
            device_label.pack(side="left", padx=(0, 10))

            # Statuslampje label
            status_label = ctk.CTkLabel(device_frame, text=status_text, font=self.font, text_color=status_color)
            status_label.pack(side="left")

    def load_controle_screen(self):
        checklist_items = []
        # Frame voor de instellingen en serienummers
        content_frame = ctk.CTkFrame(self.main_frame)
        content_frame.pack(fill="x", pady=10)

        # Linker frame voor de instellingen
        left_frame = ctk.CTkFrame(content_frame, height=150)
        left_frame.pack(side="left", fill="both", expand=True)

        # Rechter frame voor de serienummers
        right_frame = ctk.CTkScrollableFrame(content_frame, height=150)
        right_frame.pack(side="right", fill="both", expand=True)

        # Toon de opgeslagen instellingen in het linker frame
        weergave_tekst = format_instellingen_voor_weergave(self)
        label = ctk.CTkLabel(left_frame, text=weergave_tekst, justify="left", anchor="w", font=self.font)
        label.pack(anchor="w", pady=10)

        # Toon de serienummers in het rechter frame
        ctk.CTkLabel(right_frame, text="Serienummers:", font=self.font, justify='right', anchor='e').pack(anchor="e", pady=10)

        productie_modus = self.instellingen_data.get("Productie modus", {})
        if productie_modus.get("Modus") == SERIE:
            serials = generate_serials(self.serial_entry.get().upper(), int(self.amount_entry.get()),
                                       PRODUCT_CONFIG[self.selected_product]["serial_pattern"])
            if serials:
                for serial in serials:
                    ctk.CTkLabel(right_frame, text=serial, font=self.font).pack(anchor="e", pady=2)
        elif productie_modus.get("Modus") == ENKEL:
            serials = productie_modus.get("Serienummers", "").split("\n")
            for serial in serials:
                if serial.strip():
                    ctk.CTkLabel(right_frame, text=serial.strip(), font=self.font).pack(anchor="e", pady=2)


        # Frame voor de switches en bevestigingsknop
        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.pack(fill="x", pady=10)

        self.show_device_status(device_ports, control_frame)
        # Switch: Kloppen de instellingen?
        self.instellingen_ok = ctk.BooleanVar(value=False)

        switch_label = ctk.CTkLabel(left_frame, text="Kloppen de instellingen?", font=self.font)
        switch_label.pack(side="left", padx=(0, 10))

        self.instellingen_switch = ctk.CTkSwitch(
            left_frame,
            text="Nee/Ja",
            variable=self.instellingen_ok,
            onvalue=True,
            offvalue=False,
            font=self.font
        )
        self.instellingen_switch.pack(side="left")
        checklist_items = PRODUCT_CONFIG[self.selected_product].get('check_list_items', [])
        # Switches voor fysieke checklist
        self.checklist_vars = {}

        checklist_frame = ctk.CTkFrame(control_frame)
        checklist_frame.pack(pady=10, padx=20, fill="x")

        for i, item in enumerate(checklist_items):
            var = ctk.BooleanVar(value=False)
            self.checklist_vars[item] = var

            label = ctk.CTkLabel(checklist_frame, text=item, font=self.font)
            label.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            switch = ctk.CTkSwitch(checklist_frame, text="", variable=var)
            switch.grid(row=i, column=1, sticky="e", padx=10, pady=5)

        if device_ports.get("barcodescanner") is None:
            # Als de barcodescanner niet gevonden is, toon een waarschuwing
            warning_label = ctk.CTkLabel(control_frame, text="⚠️ Barcodescanner niet gevonden!", font=self.font, text_color="red")
            warning_label.pack(pady=5)

        if device_ports.get("arduino Due") is None:
            # Als de Arduino Due niet gevonden is, toon een waarschuwing
            warning_label = ctk.CTkLabel(control_frame, text="⚠️ Arduino Due niet gevonden!", font=self.font, text_color="red")
            warning_label.pack(pady=5)

        # Bevestigknop
        bevestig_button = ctk.CTkButton(control_frame, text="Bevestigen", command=lambda: bevestig(self), font=self.font)
        bevestig_button.pack(pady=20)

    def load_besturing_screen(self):
        # --- Frame voor knoppen en status ---
        controls_frame = ctk.CTkFrame(self.main_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)

        # Centered label for the header
        header_label = ctk.CTkLabel(controls_frame, text="Assemblagelijn Besturing", font=self.font)
        header_label.pack(pady=2)

        self.status_label = ctk.CTkLabel(controls_frame, text="Status: Wacht op start", font=self.font)
        self.status_label.pack(pady=2)

        knop_frame = ctk.CTkFrame(controls_frame)
        knop_frame.pack(pady=5)

        ctk.CTkButton(knop_frame, text="▶ Start", font=self.font, command=self.start_production).pack(side="left",
                                                                                                      padx=5)
        ctk.CTkButton(knop_frame, text="⏸ Pauze", font=self.font, command=self.pause_production).pack(side="left",
                                                                                                      padx=5)
        ctk.CTkButton(knop_frame, text="⏹ Stop", font=self.font, command=self.stop_production).pack(side="left", padx=5)

        self.simulator_button = ctk.CTkButton(self, text="Simuleer Arduino", command=self.open_serial_simulator)
        self.simulator_button.pack(pady=10)

        self.progress_label = ctk.CTkLabel(controls_frame, text=f"Voortgang: 0/{self.amount_entry.get()}", font=self.font)
        self.progress_label.pack(pady=1)

        progress_width = int(self.screen_width * 0.25) + (self.font_size * 15)
        self.progressbar = ctk.CTkProgressBar(controls_frame, mode="determinate", width=progress_width,
                                              height=self.screen_height * 0.01)
        self.progressbar.pack(pady=15)
        self.progressbar.set(0)

        self.apparaat_status_label = ctk.CTkLabel(controls_frame, text="Apparaat status:", font=self.font)
        self.apparaat_status_label.pack(pady=2)

        self.apparaat_status_frame = ctk.CTkFrame(self.main_frame)
        self.apparaat_status_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.update_device()
        self.productie_overzicht_label = ctk.CTkLabel(controls_frame, text="Productie Overzicht", font=self.font)

        # Bevat header én scrollable data
        self.table_container = ctk.CTkFrame(self.main_frame)
        self.table_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Sticky header
        self.header_frame = ctk.CTkFrame(self.table_container)
        self.header_frame.grid(row=0, column=0, sticky="nsew")

        # Scrollable rows
        self.stepScreen = ctk.CTkScrollableFrame(self.table_container)
        self.stepScreen.grid(row=1, column=0, sticky="nsew")

        # Table-container groeit mee
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(1, weight=1)

        # Opbouwen
        self.create_production_steps_header()
        self.create_production_steps_rows()

    def open_serial_simulator(self):
        def fake_arduino_response(input_text):
            while not message_queue.empty():
                msg = message_queue.get()
                print(f"[Arduino]: {msg}")  # Voor debug

                if "ARDUINO_Persen:" in msg:
                    _, serial = msg.strip().split(":")
                    self.update_step_status_for_serial(serial.strip(), "Persen", True, _)

                if "ARDUINO_Programmeren:" in msg:
                    _, serial = msg.strip().split(":")
                    Prog_Diver(serial, device_ports["programeerUnit"])
                    serial_data, temp_data, pres_data = Diver_Read_Unit_to_raspberry(device_ports["programeerUnit"])
                    self.update_step_status_for_serial(serial.strip(), "Programmeren", True, serial_data)

                if "ARDUINO_Graveren:" in msg:
                    _, serial = msg.strip().split(":")
                    # data = read_barcode(device_ports["barcodescanner"])
                    self.update_step_status_for_serial(serial.strip(), "Graveren", True, _)

                if "ARDUINO_Controle:" in msg:
                    _, serial = msg.strip().split(":")

                    data = read_barcode(device_ports["barcodescanner"])

                    self.update_step_status_for_serial(serial.strip(), "Controle", True, data)

                if "ARDUINO_Verpakken:" in msg:
                    _, serial = msg.strip().split(":")
                    self.update_step_status_for_serial(serial.strip(), "Verpakken", True, _)

        SerialSimulatorWindow(self, on_send_callback=fake_arduino_response)

    def update_device(self):
        device_ports = init_device()  # haalt de actuele verbindingen op

        for i, (device_name, port) in enumerate(device_ports.items()):
            status_color = "green" if port else "red"
            status_text = "🟢 Verbonden" if port else "🔴 Niet gevonden"

            if device_name not in self.status_widgets:
                # Maak label voor apparaatnaam
                name_label = ctk.CTkLabel(self.apparaat_status_frame, text=f"{device_name}:", font=self.font)
                name_label.grid(row=0, column=i, padx=(0, 10), pady=5, sticky="w")

                # Maak label voor status
                status_label = ctk.CTkLabel(self.apparaat_status_frame, text=status_text, font=self.font,
                                            text_color=status_color)
                status_label.grid(row=1, column=i, padx=(0, 10), pady=5, sticky="w")

                self.status_widgets[device_name] = status_label
            else:
                # Alleen status bijwerken
                self.status_widgets[device_name].configure(text=status_text, text_color=status_color)

        # Plan volgende update over 1 seconden
        self.after(1000, self.update_device)

    def create_production_steps_header(self):
        steps = PRODUCT_CONFIG[self.selected_product].get("productie_stappen", [])
        column_widths = [100] + [50 for _ in steps]  # eerste kolom = Serienummer

        for col_index in range(len(steps) + 1):
            self.header_frame.grid_columnconfigure(col_index, weight=1, uniform="step")
            self.stepScreen.grid_columnconfigure(col_index, weight=1, uniform="step")

        self.header_frame.grid_columnconfigure(0, weight=1)
        for i in range(1, len(steps) + 1):
            self.header_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(
            self.header_frame,
            text="Serienummer",
            font=self.font,
            anchor="center"
        ).grid(row=0, column=0, sticky="nsew", padx=0, pady=5)

        for col, step in enumerate(steps, start=1):
            ctk.CTkLabel(
                self.header_frame,
                text=step,
                font=self.font,
                anchor="center",
                justify="center"
            ).grid(row=0, column=col, sticky="nsew", padx=0, pady=5)

    def create_production_steps_rows(self):
        serials = generate_serials(
            self.serial_entry.get().upper(),
            int(self.amount_entry.get()),
            PRODUCT_CONFIG[self.selected_product]["serial_pattern"]
        )
        steps = PRODUCT_CONFIG[self.selected_product].get("productie_stappen", [])
        column_widths = [100] + [50 for _ in steps]  # eerste kolom = Serienummer

        # Zorg dat self.stepScreen dezelfde kolomlayout heeft als header_frame
        for col_index in range(len(steps) + 1):
            self.header_frame.grid_columnconfigure(col_index, weight=1, uniform="step")
            self.stepScreen.grid_columnconfigure(col_index, weight=1, uniform="step")

        productie_data = {}
        if serials:
            for serial in serials:
                productie_data[serial] = {step: None for step in steps}

        self.step_labels = {}
        for r, (serial, status_dict) in enumerate(productie_data.items(), start=1):
            self.step_labels[serial] = {}
            ctk.CTkLabel(
                self.stepScreen,
                text=serial,
                font=self.font,
                anchor="center",
                justify="center"
            ).grid(row=r, column=0, sticky="nsew", padx=5, pady=5)

            for c, step in enumerate(steps, start=1):
                status = status_dict.get(step, None)
                if status is True:
                    kleur = "green"
                    symbool = "✔"
                elif status is False:
                    kleur = "red"
                    symbool = "✘"
                else:
                    kleur = "blue"
                    symbool = "◯"

                label = ctk.CTkLabel(
                    self.stepScreen,
                    text=symbool,
                    text_color="white",
                    fg_color=kleur,
                    width=20,
                    height=30,
                    corner_radius=15,
                    anchor="center"
                )
                label.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
                self.step_labels[serial][step] = label

    # Dummy methods voor knoppen
    def start_production(self):
        self.status_label.configure(text="Status: Productie gestart")

        self.send_next_serial_to_arduino()

    def pause_production(self):
        self.status_label.configure(text="Status: Productie gepauzeerd")

    def stop_production(self):
        print("Stop productie")

    def emergency_stop(self):
        print("Noodstop")

    def reset_error(self):
        print("Reset fout")
    def select_product(self, product):
        if product:
            for widget in self.scrollable_frame.winfo_children():
                widget.forget()
            self.loadSettingsScreen()
        self.selected_product = product
        # Knopkleuren bij selectie
        for key, button in self.product_buttons.items():
            button.configure(fg_color="green" if key == product else "#1F6AA5")

        self.selected_product_label.configure(text=f"Geselecteerde productielijn: {product}")

        # Type dropdown updaten
        self.type_menu.configure(state="normal", values=PRODUCT_TYPES[product])
        self.type_menu.set(PRODUCT_TYPES[product][0])

        # Reset feedback
        self.serial_label.configure(text="")
        self.amount_feedback.configure(text="")

        self.type_menu.configure(state="normal")
        self.check_type_button.configure(state="normal")

        # Reset volgende stappen
        self.amount_entry.configure(state="disabled")
        self.check_amount_button.configure(state="disabled")
        self.series_button.configure(state="disabled")
        self.single_button.configure(state="disabled")
        self.serial_entry.pack_forget()
        self.serial_textbox.pack_forget()
        self.check_serial_button.pack_forget()


    def check_amount(self):
        try:
            amount = int(self.amount_entry.get())
            max_value = PRODUCT_CONFIG[self.selected_product]["max_amount"]

            if 0 < amount <= max_value:
                self.amount_feedback.configure(text="Aantal is geldig ✅", text_color="green")
                self.series_button.configure(state="normal")
                self.single_button.configure(state="normal")
                self.amount_entry.configure(fg_color='green')
            else:
                self.amount_feedback.configure(text="Aantal is ongeldig ❌", text_color="red")
        except ValueError:
            self.amount_feedback.configure(text="Geen geldig getal ❌", text_color="red")

    def set_mode(self, mode):
        self.production_mode = mode
        self.series_button.configure(fg_color=positive_feedback_color if mode == SERIE else standard_button_color)
        self.single_button.configure(fg_color=positive_feedback_color if mode == ENKEL else standard_button_color)

        self.serial_label.configure(
            text="Start serienummer" if mode == SERIE else "Voer serienummer(s) in"
        )

        # Wissel de zichtbare inputvelden
        self.serial_entry.pack_forget()
        self.serial_textbox.pack_forget()

        if mode == SERIE:
            # Laad de laatste serienummer uit het JSON-bestand
            instellingen_data = load_settings(product=self.selected_product)
            productie_modus = instellingen_data.get("Productie modus", {})
            laatste_serial = productie_modus.get("Eind Serienummer", "")

            if laatste_serial:
                self.serial_entry.delete(0, "end")
                self.serial_entry.insert(0, laatste_serial)

            self.serial_entry.pack(pady=2, after=self.serial_label)
            self.check_serial_button.pack(pady=5, after=self.serial_entry)
        else:
            self.serial_textbox.pack(pady=2, after=self.serial_label)
            self.check_serial_button.pack(pady=5, after=self.serial_textbox)



    def serial(self):

        if not self.selected_product:
            self.serial_feedback.configure(text="Selecteer eerst een product", text_color="red")
            return

        try:
            amount = int(self.amount_entry.get())
        except ValueError:
            self.serial_feedback.configure(text="Ongeldig aantal", text_color="red")
            return

        if self.production_mode == SERIE:
            start_serial = self.serial_entry.get().strip().upper()

            # Validatie van eerste serienummer
            if self.selected_product == DIVER and not self._validate_diver_serial(start_serial):
                return
            elif self.selected_product == CTD and not self._validate_ctd_serial(start_serial):
                return

            serials = generate_serials(self.serial_entry.get().upper(), int(self.amount_entry.get()),
                                       PRODUCT_CONFIG[self.selected_product]["serial_pattern"])
            if serials:
                self.serial_feedback.configure(text=f"Laatst serienummer: {serials[-1]}", text_color="green")
                self.serial_entry.configure(fg_color=positive_feedback_color)
                self.order_button.configure(state="normal")
                self.order_entry.configure(state="normal")

            else:
                self.serial_feedback.configure(text="Kon serienummers niet genereren", text_color="red")

        elif self.production_mode == ENKEL:
            serials = self.serial_textbox.get("1.0", "end").strip().splitlines()
            serials = [s.strip().upper() for s in serials if s.strip() != ""]

            if len(serials) != amount:
                self.serial_feedback.configure(text=f"{len(serials)} serienummers ingevoerd, verwacht {amount}",
                                            text_color="red")
                return

            # Check elk serienummer
            for s in serials:
                if self.selected_product == DIVER and not self._validate_diver_serial(s):
                    return
                elif self.selected_product == CTD and not self._validate_ctd_serial(s):
                    return

            self.serial_feedback.configure(text="Alle serienummers OK ✅", text_color="green")
            self.serial_textbox.configure(fg_color=positive_feedback_color)
            self.order_button.configure(state="normal")
            self.order_entry.configure(state="normal")


    def _validate_diver_serial(self, serial):
        serial = serial.upper()
        if len(serial) != 5:
            self.serial_label.configure(text="DIVER: Serienummer moet 5 tekens zijn", text_color="red")
            return False
        if any(c in "IOQ" for c in serial[:2]):
            self.serial_label.configure(text="DIVER: Geen I, O of Q toegestaan in prefix", text_color="red")
            return False
        if not serial[:2].isalpha() or not serial[2:].isdigit():
            self.serial_label.configure(text="DIVER: Eerste 2 letters, dan 3 cijfers vereist", text_color="red")
            return False
        if int(serial[2:]) == 0:
            self.serial_label.configure(text="DIVER: Nummer mag niet 000 zijn", text_color="red")
            return False
        print(serial)
        return True

    def _validate_ctd_serial(self, serial):
        serial = serial.upper()
        if len(serial) != 5:
            self.serial_label.configure(text="CTD: Serienummer moet 5 tekens zijn", text_color="red")
            return False
        if serial[0] in "IOQ":
            self.serial_label.configure(text="CTD: Geen I, O of Q toegestaan in eerste letter", text_color="red")
            return False
        if not serial[0].isalpha() or not serial[1:].isdigit():
            self.serial_label.configure(text="CTD: Eerste letter en 4 cijfers vereist", text_color="red")
            return False
        if int(serial[1:]) == 0:
            self.serial_label.configure(text="CTD: Nummer mag niet 0000 zijn", text_color="red")
            return False
        return True

    def update_step_status_for_serial(self, serial, step_name, status, data):
        if data != serial and step_name == 'Controle':
            status = False
        if data != serial and step_name == 'Programmeren':
            status = False
        if status is True:
            kleur = "green"
            symbool = "✔"
        elif status is False:
            kleur = "red"
            symbool = "✘"
        else:
            kleur = "blue"
            symbool = "◯"

        if serial in self.step_labels and step_name in self.step_labels[serial]:

            if step_name == "Controle" and data:
                symbool = f"{symbool} {data}"

            if step_name == "Programmeren" and data:
                symbool = f"{symbool} {data}"


            label = self.step_labels[serial][step_name]
            label.configure(text=symbool, fg_color=kleur)
            self.update_progressbar()
            # Check of alle stappen klaar zijn
            if self.serial_is_done(serial):
                print(f"✅ {serial} is volledig verwerkt.")
                self.after(500, self.send_next_serial_to_arduino)

    def checkOrderNumber(self):
        order_nummer = self.order_entry.get().strip()
        if order_nummer:
            self.order_entry.configure(fg_color=positive_feedback_color)
            self.person_entry.configure(state="normal")
            self.person_button.configure(state="normal")
            self.order_feedback.configure(text="Order nummer is geldig ✅", text_color="green")
        else:
           self.order_feedback.configure(text="Order nummer is ongeldig ❌", text_color="red")
    def poll_arduino(self):
        while not message_queue.empty():
            msg = message_queue.get()
            print(f"[Arduino]: {msg}")  # Voor debug

            if "ARDUINO_Persen:" in msg:
                _, serial = msg.strip().split(":")
                self.update_step_status_for_serial(serial.strip(), "Persen", True, _)

            if "ARDUINO_Programmeren:" in msg:
                _, serial = msg.strip().split(":")
                Prog_Diver(serial, device_ports["programeerUnit"])
                serial_data, temp_data, pres_data = Diver_Read_Unit_to_raspberry(device_ports["programeerUnit"])
                self.update_step_status_for_serial(serial.strip(), "Programmeren", True, serial_data)

            if "ARDUINO_Graveren:" in msg:
                _, serial = msg.strip().split(":")
                # data = read_barcode(device_ports["barcodescanner"])
                self.update_step_status_for_serial(serial.strip(), "Graveren", True, _)

            if "ARDUINO_Controle:" in msg:
                _, serial = msg.strip().split(":")

                data = read_barcode(device_ports["barcodescanner"])

                self.update_step_status_for_serial(serial.strip(), "Controle", True, data)

            if "ARDUINO_Verpakken:" in msg:
                _, serial = msg.strip().split(":")
                self.update_step_status_for_serial(serial.strip(), "Verpakken", True,_)

        if not stop_event.is_set():
            self.after(100, self.poll_arduino)
    def send_serial_to_arduino(self, serial):
        if not is_booted:
            print("⚠️ Arduino is nog niet klaar.")
            return
        send_command(f"SERIAL:{serial}")

    def serial_is_done(self, serial):
        """Check of alle stappen voor een serienummer ✔ zijn."""
        if serial not in self.step_labels:
            return True  # Onbekend serial? overslaan
        for label in self.step_labels[serial].values():
            if label.cget("text") == "◯":
                return False
        return True

    def send_next_serial_to_arduino(self):
        for serial in self.step_labels:
            if not self.serial_is_done(serial):
                print(f"➡️ Verstuur serienummer naar Arduino: {serial}")
                self.current_serial_bezig = serial
                send_command(f"SERIAL:{serial}")
                return
        print("✅ Alle serienummers zijn verwerkt.")

    def update_progressbar(self):
        total_products = len(self.step_labels)
        completed_products = 0

        for serial, stappen in self.step_labels.items():
            all_done = all(label.cget("text") == "✔" for label in stappen.values())
            if all_done:
                completed_products += 1

        # Update progressbar
        if total_products > 0:
            progress = completed_products / total_products
            self.progressbar.set(progress)
            self.progress_label.configure(text=f"Voortgang: {completed_products}/{total_products}")
        else:
            self.progressbar.set(0)
            self.progress_label.configure(text="Voortgang: 0/0")
        if completed_products == total_products:
            self.progress_label.configure(text="Alle producten zijn klaar!")




if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()



