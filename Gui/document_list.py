import tkinter as tk

class DocumentList(tk.Frame):
    def __init__(self, parent, documents, on_select_document, on_upload_document):
        super().__init__(parent)
        self.on_select_document = on_select_document
        self.on_upload_document = on_upload_document

        # Header
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="Documents", font=("Arial", 14, "bold")).pack(side="left")
        tk.Button(header_frame, text="Upload Document", command=self.on_upload_document).pack(side="right")

        # Listbox for documents
        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True)
        self.refresh_list(documents)
        self.listbox.bind("<<ListboxSelect>>", self.handle_selection)

    def refresh_list(self, documents):
        self.listbox.delete(0, tk.END)
        for doc in documents:
            self.listbox.insert(tk.END, f"{doc['name']} ({doc['status']})")

    def handle_selection(self, event):
        index = self.listbox.curselection()
        if index:
            self.on_select_document(index[0])
