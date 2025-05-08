import tkinter as tk

class ValidationPanel(tk.Frame):
    def __init__(self, parent, on_update_segment_status):
        super().__init__(parent)
        self.on_update_segment_status = on_update_segment_status
        self.segments = []

        self.label = tk.Label(self, text="Validation Panel", font=("Arial", 14, "bold"))
        self.label.pack(pady=5)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.status_var = tk.StringVar()
        self.status_options = ["Diterima", "Perlu Validasi", "Ditolak"]
        self.status_menu = tk.OptionMenu(self, self.status_var, *self.status_options, command=self.update_status)
        self.status_menu.pack(pady=5)

    def load_segments(self, segments):
        self.segments = segments
        self.listbox.delete(0, tk.END)
        for seg in segments:
            self.listbox.insert(tk.END, f"{seg['type']} - {seg.get('text', '')[:20]}")

    def on_select(self, event):
        index = self.listbox.curselection()
        if index:
            seg = self.segments[index[0]]
            self.status_var.set(seg.get("status", "Perlu Validasi"))

    def update_status(self, new_status):
        index = self.listbox.curselection()
        if index:
            seg = self.segments[index[0]]
            seg_id = seg["id"]
            self.on_update_segment_status(seg_id, new_status)
