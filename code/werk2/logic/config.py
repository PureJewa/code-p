from imports import *
BESTAND_INSTELLINGEN = "data/instellingen.json"
BESTAND_GESCHIEDENIS = "data/geschiedenis.json"


# BASE_DIR aanpassen zodat het naar de hoofdmap ('werk2') wijst
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Volledige paden naar afbeeldingen
logo_path = os.path.join(BASE_DIR, "img", "LogoImage.png")
off_path = os.path.join(BASE_DIR, "img", "OffImage.png")

# Afbeeldingen laden
_logo_pil = Image.open(logo_path)
_off_pil = Image.open(off_path)

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
