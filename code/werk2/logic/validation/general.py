import string

VALID_LETTERS = ''.join([c for c in string.ascii_uppercase if c not in "IOQ"])
LETTER_BASE = len(VALID_LETTERS)

def letter_to_num(s):
    n = 0
    for c in s:
        n = n * LETTER_BASE + VALID_LETTERS.index(c)
    return n

def num_to_letter(n, length):
    chars = []
    for _ in range(length):
        chars.append(VALID_LETTERS[n % LETTER_BASE])
        n //= LETTER_BASE
    return ''.join(reversed(chars)).rjust(length, VALID_LETTERS[0])  # Padding met 'A'

def parse_pattern(pattern):
    """Geeft een lijst van (type, waarde). Type kan 'L', 'D' of 'S' (speciaal) zijn."""
    parts = []
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char in ('L', 'D'):
            length = 1
            while i + 1 < len(pattern) and pattern[i + 1] == char:
                length += 1
                i += 1
            parts.append((char, length))
        else:
            parts.append(('S', char))  # Speciaal karakter
        i += 1
    return parts

def split_serial(serial, pattern):
    """Splitst het serienummer op basis van het patroon, inclusief speciale tekens."""
    pattern_parts = parse_pattern(pattern)
    serial_parts = []
    idx = 0
    for p_type, value in pattern_parts:
        if p_type == 'S':
            serial_parts.append(value)
            idx += 1
        else:
            serial_parts.append(serial[idx:idx + value])
            idx += value
    return serial_parts

def generate_serials(start_serial, count, pattern, allow_all_zero=False):
    """
    Genereert een lijst van serienummers op basis van een startwaarde en patroon.

    start_serial: Start serienummer (bv. 'AA-000').
    count: Aantal te genereren serienummers.
    pattern: Patroon, bv. 'LL-DDD'.
    allow_all_zero: Als False, worden nummers als 'AA-000' overgeslagen.
    """
    pattern_parts = parse_pattern(pattern)
    serial_parts = split_serial(start_serial, pattern)

    # Bepaal indexen van letter- en cijferdelen
    digit_idx = -1
    letter_idx = None
    num_digits = 0
    num_letters = 0

    for i, (p_type, value) in enumerate(pattern_parts):
        if p_type == 'D' and digit_idx == -1:
            digit_idx = i
            num_digits = value
        elif p_type == 'L' and letter_idx is None:
            letter_idx = i
            num_letters = value

    if digit_idx == -1:
        raise ValueError("Patroon moet ten minste één cijferdeel ('D') bevatten.")

    start_number = int(serial_parts[digit_idx])
    letter_number = letter_to_num(serial_parts[letter_idx]) if letter_idx is not None else 0

    result = []
    i = 0
    while len(result) < count:
        current_num = start_number + i
        current_letter_num = letter_number

        # Handle numeric overflow into letter part
        overflow_letters = current_num // (10 ** num_digits)
        current_num %= (10 ** num_digits)
        current_letter_num += overflow_letters

        if num_letters > 0 and current_letter_num >= LETTER_BASE ** num_letters:
            raise OverflowError("Serienummer letters zijn de maximale waarde gepasseerd.")

        new_parts = list(serial_parts)

        # Update digits
        new_parts[digit_idx] = f"{current_num:0{num_digits}}"

        # Update letters
        if letter_idx is not None:
            new_parts[letter_idx] = num_to_letter(current_letter_num, num_letters)

        serial_candidate = ''.join(new_parts)

        if not allow_all_zero and int(new_parts[digit_idx]) == 0:
            i += 1
            continue

        result.append(serial_candidate)
        i += 1

    return result
