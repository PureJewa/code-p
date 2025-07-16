import socket

# Instellingen
computer_ip = "192.168.48.173"  # IP-adres van de computer
port = 3384  # Poort van de server op de computer
csv_filename = "data.csv"

# CSV-bestand genereren
with open(csv_filename, "w") as f:
    f.write("Naam,Leeftijd,Score\n")
    f.write("Alice,25,90\n")
    f.write("Bob,30,85\n")
    f.write("Charlie,22,95\n")

print(f"CSV-bestand '{csv_filename}' gegenereerd.")

# Verbinden met de computer en bestand verzenden
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    print(f"Verbinden met {computer_ip}:{port}...")
    client_socket.connect((computer_ip, port))
    with open(csv_filename, "rb") as f:
        for chunk in f:
            client_socket.sendall(chunk)
    print("Bestand succesvol verzonden!")

