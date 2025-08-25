from imports import *
timeout = 2
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
        'check_list_items' : [
            "Juiste nulspanplaat gebruikt",
            "Graveermachine correct ingesteld",
            "Juiste submodules geplaatst",
            "divers geplaatst"],
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
    },

}
DEVICES = {
    "barcodescanner": {"vid": 0x0483, "pid": 0x5740},
    "Arduino": {"vid": 0x2341, "pid": 0x0042},
    "programeerUnit": {"vid": 0x2047 , "pid": 0x0ab9},

}

def init_device():
    from helperfunctions import find_all_devices
    device_ports = find_all_devices()
    return device_ports
device_ports = init_device()

# Commandos voor Diver USB reading unit
COMMAND_SERIAL = b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'
COMMAND_PRESSURE = b'\x01\x47\x32\x38\x02\x03\xB7\xA0'
COMMAND_PUSHSERIE = b'\x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D\x46\x4E\x30\x38\x36\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03\x80D\xA0'
