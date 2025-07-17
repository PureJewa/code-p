import customtkinter as ctk
from werk2.imports import *
BESTAND_INSTELLINGEN = "data/instellingen.json"
BESTAND_GESCHIEDENIS = "data/geschiedenis.json"
_logo_pil = Image.open("img/logo.png")
_off_pil = Image.open("img/img.png")

LOGO_IMAGE = _logo_pil
OFF_IMAGE = _off_pil


DIVER = "Diver"
CTD = "CTD"
SERIE = "Series"
ENKEL = "Enkel"


# ---------- Uitbreidbare configuratie ----------
#Producten, types, en serienummer
#Serienummer patronen kunnen worden aangepast per product
#L = Letter, D = Digit, X = Any character

PRODUCT_CONFIG = {
    "Diver": {
        "types": ["DI801", "DI802", "DI803"],
        "max_amount": 500,
        'serial_pattern': "LLDDD",  # Letter, Letter, Diggit, Digit, Digit
        'productie_stappen' :[
            'Persen',
            'Programmeren',
            'Graveren',
            'Controle',
            'Verpakken'
        ]
    },
    "CTD": {
        "types": ["DI281", "DI282", "DI283"],
        'max_amount': 100,
        'serial_pattern': "LDDDD",  # Letter, Letter, Diggit, Digit, Digit
        'productie_stappen' :[
            'Graveren',
            'Controle',
            'Verpakken'
        ]
    },
    "Dektech": {
        "types" : ["PLACEHOLDER"],
        'max_amount': 100,
    },
    "RDE-tips" : {
        "types" : ["Carbon", "Goud", "Silver", "Platina"],
        'max_amount': 100,
    }
}
# ----------------------------------------------

# # Product types per product voor dropdown
# PRODUCT_TYPES = {
#     "Diver": PRODUCT_CONFIG["Diver"]["types"],
#     "CTD": PRODUCT_CONFIG["CTD"]["types"],
#     "Dektech" : PRODUCT_CONFIG["Dektech"]["types"],
#     "RDE-tips" : PRODUCT_CONFIG["RDE-tips"]["types"]
# }

# print(PRODUCT_CONFIG["Diver"]["max_amount"])
# import pprint
# pprint.pprint(PRODUCT_CONFIG)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Werk2 Config")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        self.product_menu = ctk.CTkOptionMenu(
            self.frame,
            values=list(PRODUCT_CONFIG.keys()),
            # command=lambda _: self.update_types()  # _ ipv niets, om fout te voorkomen
        )
        self.product_menu.pack(pady=20)
        self.product_menu_button = ctk.CTkButton(
            self.frame,
            text="Update Types",
            command=self.update_types
        )
        self.product_menu_button.pack(pady=10)
        # self.product_menu.set(list(PRODUCT_CONFIG.keys())[0])  # <-- Belangrijk!

    def update_types(self):
        selected = self.product_menu.get()
        print(f"Geselecteerd product: {selected}")
        print("Max aantal:", PRODUCT_CONFIG[selected]["max_amount"])  # zou nu moeten werken

if __name__ == "__main__":
    app = App()
    app.mainloop()