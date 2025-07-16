logo = r"/home/code-p/PycharmProjects/Stage3/logo.png"
tijdSensor = 120
titel = "Assemblagelijn"
schermAfmetingen = "800x480"
totaalTijd = 0
geschatteTijd = 0
secondeInUur = 3600
gedaan = 0
startSerieNummer = ""
serieNummerLijst = []
ScannerPort = '/dev/ttyACM2'
ArduinoPort = '/dev/ttyACM1'
ReadingUnitPort = '/dev/ttyACM0'

serienummerPath = r"/home/code-p/PycharmProjects/serienummer.cvs"

result = {'serial_number': "Onbekend", 'pressure_value': "Onbekend", 'temperature_value': "Onbekend"}
baudrate = 9600
timeout = 2
ackMessage = "Copy"

# Commandos voor Diver USB reading unit
COMMAND_SERIAL = b'\x01\x4E\x32\x34\x02\x03\xBA\xA0'
COMMAND_PRESSURE = b'\x01\x47\x32\x38\x02\x03\xB7\xA0'
COMMAND_PUSHSERIE = b'\x01\x46\x32\x34\x02\x2E\x2E\x30\x30\x2D\x46\x4E\x30\x38\x36\x20\x20\x32\x31\x39\x2E\x47\x65\x31\x30\x38\x39\x31\x31\x35\x36\x55\x54\x43\x2B\x31\x20\x20\x20\x20\x20\x03\x80D\xA0'

print(startSerieNummer)