import customtkinter as ctk
from PIL import Image
import os

class ImageApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Afbeeldingen in CTk")
        self.geometry("200x200")

        # Bestandspad controleren
        file_path = r"C:\Users\Jelle\PycharmProjects\pythonProject\logo.png"
        if not os.path.exists(file_path):
            print("Fout: Afbeelding niet gevonden:", file_path)
            return

        # Laad een afbeelding
        self.image = ctk.CTkImage(
            dark_image=Image.open(file_path),   # Voor donkere modus
            size=(200, 200)  # Optioneel: grootte aanpassen
        )

        # Voeg een label toe met de afbeelding
        self.image_label = ctk.CTkLabel(self, text="", image=self.image)
        self.image_label.pack(pady=20)

        # Voeg een knop toe met een afbeelding
        self.image_button = ctk.CTkButton(self, text="Klik mij", image=self.image, compound="top")
        self.image_button.pack(pady=20)


if __name__ == "__main__":
    app = ImageApp()
    app.mainloop()
