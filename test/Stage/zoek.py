def add_hex_numbers(hex_numbers):
    """
    Voegt een lijst van hexadecimale getallen samen en retourneert het resultaat in hex.

    Args:
        hex_numbers (list): Lijst van hexadecimale getallen (bijvoorbeeld ['0x01', '0x4E', '0x32']).

    Returns:
        str: Het resultaat van de optelling in hexadecimale notatie.
    """
    # Zet de hexadecimale getallen om naar decimale getallen, tel ze op en zet het resultaat terug naar hex
    total = sum(int(hex_num, 16) for hex_num in hex_numbers)

    # Retourneer het resultaat als hexadecimale string (zonder de '0x' prefix)
    return hex(total)

#hex_numbers = ['0x01', '0x4E', '0x32', '0x34', '0x46', '0x4D', '0x38','0x35', '0x39', '0x02', '0x03']
# Voorbeeld van het gebruik:
hex_numbers = ['0x01', '0x46', '0x32', '0x34', '0x02', '0x03', '0x2E', '0x2E', '0x30', '0x30', '0x2D', '0x46', '0x4E', '0x30', '0x38', '0x36', '0x20', '0x20', '0x32', '0x31', '0x39', '0x2E', '0x47', '0x65', '0x31', '0x30', '0x38', '0x39', '0x31', '0x31', '0x35', '0x36', '0x55', '0x54', '0x43', '0x2B', '0x31', '0x20', '0x20', '0x20', '0x20', '0x20', '0x03']
hex_numbers2 = ['0x01', '0x46', '0x4D', '0x38', '0x35', '0x39', '0x02', '0x03']

result = add_hex_numbers(hex_numbers)
result2 = add_hex_numbers(hex_numbers2)
print(f"Resultaat van optelling: {result}")
print(f"Resultaat van optelling: {result2}")
