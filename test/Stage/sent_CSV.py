import smbprotocol
from smbprotocol import smb2
from smbprotocol import security
import os

# Initialize SMB protocol
smbprotocol.ClientConfig(username="code-p", password="1234")
smbprotocol.ClientConfig(server="192.168.16.97")


def send_file_to_windows(csv_file, share_name, remote_file_path):
    try:
        # Connect to the Windows share
        smb2_tree = smbprotocol.open_file(share_name, remote_file_path, access=smbprotocol.FILE_WRITE_DATA)

        # Open the CSV file on Raspberry Pi
        with open(csv_file, 'rb') as file:
            data = file.read()

        # Write the file data to the Windows machine
        smb2_tree.write(0, data)  # 0 is the starting position

        print(f"File {csv_file} sent successfully to {remote_file_path}")
    except Exception as e:
        print(f"Error: {e}")


# Example usage
csv_file = r"/home/code-p/share/serienummer.csv"
share_name = "your_share_name"  # Replace with the shared folder name on Windows
remote_file_path = "path/to/destination/file.csv"  # Destination file path on Windows

send_file_to_windows(csv_file, share_name, remote_file_path)
