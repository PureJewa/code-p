from imports import *

class CustomDateEntry(ctk.CTkEntry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._popup = None
        self.bind("<Button-1>", self.show_calendar)
        self.configure(state="readonly")
        self.configure(state="normal")
        self.delete(0, tk.END)
        self.insert(0, datetime.now().strftime("%d-%m-%Y"))
        self.configure(state="readonly")

    def show_calendar(self, event=None):
        if self._popup and self._popup.winfo_exists():
            self._popup.destroy()

        self._popup = tk.Toplevel(self)
        self._popup.wm_overrideredirect(True)
        self._popup.attributes('-topmost', 'true')

        x = self.winfo_rootx()
        y = self.winfo_rooty() - 250  # ruim genoeg bovenin

        self._popup.geometry(f"+{x}+{y}")

        font_lg = tkfont.Font(family="Arial", size=20)
        cal = Calendar(self._popup, date_pattern="dd-mm-yyyy", font=font_lg)
        cal.pack()

        cal.bind("<<CalendarSelected>>", lambda e: self._on_date_selected(cal.selection_get()))
    def _on_date_selected(self, date):
        self.configure(state="normal")
        self.delete(0, tk.END)
        self.insert(0, date.strftime("%d-%m-%Y"))
        self.configure(state="readonly")
        if self._popup:
            self._popup.destroy()
