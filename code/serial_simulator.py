import customtkinter as ctk
from datetime import datetime
import queue

message_queue = queue.Queue()
class SerialSimulatorWindow(ctk.CTkToplevel):
    def __init__(self, master, on_send_callback=None):
        super().__init__(master)
        self.title("Arduino Simulator")
        self.geometry("500x400")
        self.on_send_callback = on_send_callback

        self.output_box = ctk.CTkTextbox(self, width=480, height=300)
        self.output_box.pack(padx=10, pady=(10, 5))
        self.output_box.configure(state="disabled")

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.input_entry = ctk.CTkEntry(self.input_frame)
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", self._send_message)

        self.send_button = ctk.CTkButton(self.input_frame, text="Verstuur", command=self._send_message)
        self.send_button.pack(side="right")

    def _send_message(self, event=None):
        message = self.input_entry.get().strip()
        if message:
            self._append_message(">>", message)
            self.input_entry.delete(0, "end")
            if self.on_send_callback:
                response = self.on_send_callback(message)
                if response:
                    self._append_message("<<", response)

    def _append_message(self, prefix, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {prefix} {message}\n"
        self.output_box.configure(state="normal")
        self.output_box.insert("end", formatted)
        self.output_box.configure(state="disabled")
        self.output_box.see("end")
