import customtkinter as ctk

class ControleScherm(ctk.CTkFrame):
    def __init__(self, master, data):
        """
        data: dict van serienummer -> dict van stapnaam -> status (bool)
        """
        super().__init__(master)

        self.data = data
        self.stappen = list(next(iter(data.values())).keys())  # neem stappen van eerste item

        # Header row met stappen
        ctk.CTkLabel(self, text="Serienummer", width=120, anchor="w", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5)

        for col, stap in enumerate(self.stappen, start=1):
            ctk.CTkLabel(self, text=stap, width=150, anchor="w", font=ctk.CTkFont(weight="bold")).grid(row=0, column=col, padx=5, pady=5)

        # Data rijen
        for row, (serial, stap_status) in enumerate(self.data.items(), start=1):
            ctk.CTkLabel(self, text=serial, width=120, anchor="w").grid(row=row, column=0, padx=5, pady=5)

            for col, stap in enumerate(self.stappen, start=1):
                status = stap_status.get(stap, False)
                kleur = "green" if status else "red"
                symbool = "✔" if status else "✘"

                label = ctk.CTkLabel(self, text=symbool, fg_color=kleur, text_color="white", width=30, height=30, corner_radius=15)
                label.grid(row=row, column=col, padx=10, pady=5)

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("700x400")

    # Voorbeeld data
    voorbeeld_data = {
        "SN1001": {"Materialen verzamelen": True, "Assemblage": True, "Kwaliteitscontrole": False, "Verpakking": True},
        "SN1002": {"Materialen verzamelen": True, "Assemblage": True, "Kwaliteitscontrole": True, "Verpakking": True},
        "SN1003": {"Materialen verzamelen": False, "Assemblage": False, "Kwaliteitscontrole": False, "Verpakking": False},
        # etc...
    }

    scherm = ControleScherm(root, voorbeeld_data)
    scherm.pack(fill="both", expand=True)

    root.mainloop()
