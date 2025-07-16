import customtkinter as ctk


class TouchKeyboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Touchscreen Tekstinvoer")
        self.geometry("800x480")

        # Variabele om ingevoerde tekst op te slaan
        self.text_var = ctk.StringVar(value="")

        # Label en invoerveld
        self.label = ctk.CTkLabel(self, text="Voer tekst in:", font=("Arial", 18))
        self.label.pack(pady=10)

        self.text_entry = ctk.CTkEntry(self, textvariable=self.text_var, width=400, font=("Arial", 16))
        self.text_entry.pack(pady=10)

        # Toetsenbord
        self.create_keyboard()

    def create_keyboard(self):
        """Maak een toetsenbord met knoppen."""
        keyboard_frame = ctk.CTkFrame(self)
        keyboard_frame.pack(pady=10)

        keys = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space', 'Back'
        ]

        row, col = 0, 0
        for key in keys:
            if key == "Space":
                button = ctk.CTkButton(keyboard_frame, text="␣", width=100, command=lambda: self.insert_text(" "))
            elif key == "Back":
                button = ctk.CTkButton(keyboard_frame, text="←", width=50, command=self.delete_last_char)
            else:
                button = ctk.CTkButton(keyboard_frame, text=key, width=50, command=lambda k=key: self.insert_text(k))

            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 9:  # Maximaal 10 knoppen per rij
                col = 0
                row += 1

    def insert_text(self, char):
        """Voeg een teken toe aan het invoerveld."""
        current_text = self.text_var.get()
        self.text_var.set(current_text + char)

    def delete_last_char(self):
        """Verwijder het laatste teken."""
        current_text = self.text_var.get()
        self.text_var.set(current_text[:-1])


# Start de app
app = TouchKeyboardApp()
app.mainloop()
