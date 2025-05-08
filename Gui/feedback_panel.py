import tkinter as tk

class FeedbackPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.label = tk.Label(self, text="Feedback Panel", font=("Arial", 14, "bold"))
        self.label.pack(pady=5)

        self.text = tk.Text(self, height=10, state="disabled")
        self.text.pack(fill="both", expand=True)

    def update_log(self, log_text):
        self.text.config(state="normal")
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, log_text)
        self.text.config(state="disabled")
