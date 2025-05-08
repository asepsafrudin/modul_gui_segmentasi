import tkinter as tk
from document_list import DocumentList
from segmentation_preview_new import SegmentationPreview
from validation_panel import ValidationPanel
from feedback_panel import FeedbackPanel

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Modul Segmentasi Dokumen - Layout 2")

        # Sample data (replace with API calls)
        self.documents = [
            {"id": "doc1", "name": "Kontrak Klien A.pdf", "status": "Selesai", "image": "logo pdf.png"},
            {"id": "doc2", "name": "Laporan Keuangan Q3.docx", "status": "Perlu Validasi", "image": "logo2.png"},
            {"id": "doc3", "name": "Surat Perjanjian.pdf", "status": "Baru", "image": "logo pdf.png"},
        ]
        self.segments_data = {
            "doc1": [
                {"id": "seg1-1", "type": "Header", "text": "Judul Dokumen Kontrak", "x": 50, "y": 30, "w": 700, "h": 40, "status": "Diterima"},
                {"id": "seg1-2", "type": "Teks Utama", "text": "Pasal 1 ayat 1 menyatakan bahwa...", "x": 50, "y": 100, "w": 700, "h": 200, "status": "Diterima"},
                {"id": "seg1-3", "type": "Tanda Tangan", "text": "[TTD Klien]", "x": 600, "y": 500, "w": 150, "h": 50, "status": "Diterima"},
            ],
            "doc2": [
                {"id": "seg2-1", "type": "Header", "text": "Laporan Keuangan Kuartal 3", "x": 50, "y": 30, "w": 700, "h": 40, "status": "Perlu Validasi"},
                {"id": "seg2-2", "type": "Tabel", "text": "[Data Tabel Keuangan]", "x": 50, "y": 100, "w": 700, "h": 300, "status": "Perlu Validasi"},
            ],
            "doc3": [],
        }
        self.correction_log = []

        # Main container paned window for resizable columns
        container = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        container.pack(fill="both", expand=True)

        # Column 1: Menu bar and submenu interaction (vertical menu)
        col1 = tk.Frame(container, bg="#e0e0e0")
        container.add(col1, minsize=100)

        menu_label = tk.Label(col1, text="Menu", font=("Arial", 16, "bold"), bg="#e0e0e0")
        menu_label.pack(pady=10)

        # Use a Listbox for menu items
        self.menu_listbox = tk.Listbox(col1)
        self.menu_listbox.pack(fill="x", padx=10, pady=5)
        for item in ["Open Document", "Save Changes", "Settings"]:
            self.menu_listbox.insert(tk.END, item)

        # Submenu interaction area below menu
        submenu_label = tk.Label(col1, text="Documents", font=("Arial", 14, "bold"), bg="#e0e0e0")
        submenu_label.pack(pady=10)

        self.document_list = DocumentList(col1, self.documents, self.select_document, self.upload_document)
        self.document_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Column 2: Preview area with a frame and title
        col2 = tk.Frame(container, bg="white")
        container.add(col2, minsize=100)

        preview_label = tk.Label(col2, text="Preview", font=("Arial", 16, "bold"), bg="white")
        preview_label.pack(pady=5)

        self.segmentation_preview = SegmentationPreview(col2)
        self.segmentation_preview.pack(fill="both", expand=True, padx=5, pady=5)

        # Column 3: Validation panel and feedback panel stacked vertically with titles
        col3 = tk.Frame(container, bg="#f9f9f9")
        container.add(col3, minsize=100)

        validation_label = tk.Label(col3, text="Validation Panel", font=("Arial", 16, "bold"), bg="#f9f9f9")
        validation_label.pack(pady=5)

        self.validation_panel = ValidationPanel(col3, self.update_segment_status)
        self.validation_panel.pack(fill="both", expand=True, padx=5, pady=5)

        feedback_label = tk.Label(col3, text="Feedback Panel", font=("Arial", 16, "bold"), bg="#f9f9f9")
        feedback_label.pack(pady=5)

        self.feedback_panel = FeedbackPanel(col3)
        self.feedback_panel.pack(fill="both", expand=True, padx=5, pady=5)

        # Set initial sash positions for equal ratio columns after window is initialized
        self.update_idletasks()
        total_width = self.winfo_width()
        if total_width > 0:
            container.sash_place(0, total_width // 3, 0)
            container.sash_place(1, 2 * total_width // 3, 0)

        self.select_document(0)

    def select_document(self, index):
        if index < 0 or index >= len(self.documents):
            return
        self.selected_document_index = index
        doc = self.documents[index]
        image_path = doc.get("image", "")
        self.segmentation_preview.load_images([image_path])
        segments = self.segments_data.get(doc["id"], [])
        # Set segments per page with page 0 segments for single page document
        self.segmentation_preview.set_segments_per_page({0: segments})
        self.segmentation_preview.display_segments(segments)
        self.validation_panel.load_segments(segments)

    def update_segment_status(self, segment_id, new_status):
        for seg_list in self.segments_data.values():
            for seg in seg_list:
                if seg["id"] == segment_id:
                    seg["status"] = new_status
                    log_entry = f"Segment {segment_id} status updated to {new_status}"
                    self.correction_log.append(log_entry)
                    self.feedback_panel.update_log("\n".join(self.correction_log))
                    print(log_entry)
                    return

    def upload_document(self):
        print("Upload document clicked")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
