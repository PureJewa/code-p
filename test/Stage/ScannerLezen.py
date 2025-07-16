import serial


def read_barcode():
    # Open de seriële poort (pas de poortnaam aan als nodig)
    ser = serial.Serial('COM4', baudrate=9600, timeout=1)

    print("Wachten op barcode...")

    try:
        while True:
            if ser.in_waiting > 0:  # Controleer of er gegevens zijn
                data = ser.readline().decode('utf-8').strip()  # Lees de gegevens
                print(f"Barcode gescand: {data}")
    except KeyboardInterrupt:
        print("\nProgramma gestopt.")
    finally:
        ser.close()


if __name__ == "__main__":
    read_barcode()
