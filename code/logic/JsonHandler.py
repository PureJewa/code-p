from imports import *
from logic.config import *
def save_settings(product, data):
    try:
        # Laad bestaande instellingen
        if os.path.exists(BESTAND_INSTELLINGEN):
            with open(BESTAND_INSTELLINGEN, "r") as f:
                try:
                    instellingen = json.load(f)
                except json.JSONDecodeError:
                    instellingen = {}
        else:
            instellingen = {}

        # Overschrijven of toevoegen van de instelling voor dit product
        instellingen[product] = data

        # Opslaan van de instellingen (1 per product)
        with open(BESTAND_INSTELLINGEN, "w") as f:
            json.dump(instellingen, f, indent=4)

        # Toevoegen aan geschiedenis (alle data bewaren)
        historie_item = {
            "product": product,
            "tijd": datetime.now().isoformat(),
            "data": data
        }

        if os.path.exists(BESTAND_GESCHIEDENIS):
            with open(BESTAND_GESCHIEDENIS, "r") as f:
                try:
                    geschiedenis = json.load(f)
                    if not isinstance(geschiedenis, list):
                        geschiedenis = []
                except json.JSONDecodeError:
                    geschiedenis = []
        else:
            geschiedenis = []

        geschiedenis.append(historie_item)

        with open(BESTAND_GESCHIEDENIS, "w") as f:
            json.dump(geschiedenis, f, indent=4)

    except Exception as e:
        print(f"Fout bij opslaan instellingen voor product '{product}': {e}")


def load_settings(product):
    if os.path.exists(BESTAND_INSTELLINGEN):
        try:
            with open(BESTAND_INSTELLINGEN, "r") as f:
                content = f.read().strip()
                if content:
                    instellingen = json.loads(content)
                    return instellingen.get(product, {})
        except json.JSONDecodeError:
            print("Fout: instellingenbestand is geen geldige JSON.")
    return {}

import customtkinter as ctk

# Definieer het formulier als een lijst van items, elk met een type en extra info
form_items = [
    {"label": "Naam", "type": "entry", "var_type": "str"},
    {"label": "Leeftijd", "type": "entry", "var_type": "int"},
    {"label": "Geslacht", "type": "radiobutton", "options": ["Man", "Vrouw", "Anders"], "var_type": "str"},
    {"label": "Hobby's", "type": "checkbutton", "options": ["Sport", "Lezen", "Programmeren"], "var_type": "list"},
    {"label": "Voorkeurskleur", "type": "combobox", "options": ["Rood", "Groen", "Blauw"], "var_type": "str"},
    {"label": "Ervaring (jaren)", "type": "slider", "from_": 0, "to": 30, "var_type": "int"},
]

class DynamicForm(ctk.CTkFrame):
    def __init__(self, parent, items):
        super().__init__(parent)
        self.items = items
        self.variables = {}  # Om variabelen op te slaan

        for i, item in enumerate(items):
            # Label
            ctk.CTkLabel(self, text=item["label"]).grid(row=i, column=0, sticky="w", padx=5, pady=5)

            # Afhankelijk van type widget maken we de juiste aanroep
            if item["type"] == "entry":
                if item["var_type"] == "int":
                    var = ctk.IntVar()
                else:
                    var = ctk.StringVar()
                entry = ctk.CTkEntry(self, textvariable=var)
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                self.variables[item["label"]] = var

            elif item["type"] == "combobox":
                var = ctk.StringVar()
                combo = ctk.CTkComboBox(self, values=item["options"], variable=var)
                combo.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                self.variables[item["label"]] = var

            elif item["type"] == "checkbutton":
                # Voor meerdere opties maken we meerdere boolean vars en meerdere checkbuttons
                vars = []
                frame = ctk.CTkFrame(self)
                frame.grid(row=i, column=1, sticky="w", padx=5, pady=5)
                for opt in item["options"]:
                    var = ctk.BooleanVar()
                    chk = ctk.CTkCheckBox(frame, text=opt, variable=var)
                    chk.pack(side="left", padx=5)
                    vars.append((opt, var))
                self.variables[item["label"]] = vars  # lijst van tuples (optie, var)

            elif item["type"] == "radiobutton":
                var = ctk.StringVar()
                frame = ctk.CTkFrame(self)
                frame.grid(row=i, column=1, sticky="w", padx=5, pady=5)
                for opt in item["options"]:
                    rb = ctk.CTkRadioButton(frame, text=opt, variable=var, value=opt)
                    rb.pack(side="left", padx=5)
                self.variables[item["label"]] = var

            elif item["type"] == "slider":
                if item["var_type"] == "int":
                    var = ctk.IntVar()
                else:
                    var = ctk.DoubleVar()
                slider = ctk.CTkSlider(self, from_=item["from_"], to=item["to"], variable=var)
                slider.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                self.variables[item["label"]] = var

        self.columnconfigure(1, weight=1)  # Zorgt dat de rechterkolom uitrekt

        # Submit knop
        btn = ctk.CTkButton(self, text="Verzenden", command=self.submit)
        btn.grid(row=len(items), column=0, columnspan=2, pady=10)

    def submit(self):
        # Haal alle waardes op en print ze (of verwerk ze verder)
        resultaat = {}
        for key, var in self.variables.items():
            if isinstance(var, list):
                # checkbutton lijst, filter alleen geselecteerde
                geselecteerd = [opt for opt, v in var if v.get()]
                resultaat[key] = geselecteerd
            else:
                resultaat[key] = var.get()
        print("Ingevulde data:")
        for k, v in resultaat.items():
            print(f"  {k}: {v}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # 'dark', 'light' of 'system'
    app = ctk.CTk()
    app.geometry("450x350")
    app.title("Uitgebreid Data-Driven Formulier")

    form = DynamicForm(app, form_items)
    form.pack(fill="both", expand=True, padx=10, pady=10)

    app.mainloop()
