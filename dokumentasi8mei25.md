# Dokumentasi Proyek Modul GUI Segmentasi (8 Mei 2025)

## Struktur Proyek
- `Gui/`
  - `Main_gui.py` : File utama yang menjalankan aplikasi GUI menggunakan tkinter.
  - `document_list.py` : Modul untuk menampilkan daftar dokumen dengan fitur upload.
  - `feedback_panel.py` : Panel untuk menampilkan log atau feedback dari pengguna.
  - `segmentation_preview_new.py` : Modul untuk menampilkan preview segmentasi dokumen dengan fitur interaktif (resize dan move segment).
  - `validation_panel.py` : Panel untuk validasi status segmentasi dokumen.
- `logo pdf.png`, `logo2.png` : File gambar yang digunakan sebagai ikon atau preview dokumen.

## Penjelasan File dan Kelas Utama

### Main_gui.py
- Kelas `MainApp(tk.Tk)`:
  - Merupakan kelas utama aplikasi GUI.
  - Variabel penting:
    - `documents`: List dokumen contoh dengan atribut id, nama, status, dan gambar.
    - `segments_data`: Data segmentasi per dokumen, berisi koordinat dan status segment.
    - `correction_log`: Log perubahan status segment.
  - Fungsi utama:
    - `select_document(index)`: Memilih dokumen dan menampilkan preview serta data segmentasi.
    - `update_segment_status(segment_id, new_status)`: Memperbarui status segment dan mencatat log.
    - `upload_document()`: Placeholder untuk fungsi upload dokumen.
  - Komponen GUI:
    - Menu dokumen, preview segmentasi, panel validasi, dan panel feedback.

### document_list.py
- Kelas `DocumentList(tk.Frame)`:
  - Menampilkan daftar dokumen dalam bentuk Listbox.
  - Memiliki tombol "Upload Document".
  - Fungsi:
    - `refresh_list(documents)`: Memperbarui daftar dokumen.
    - `handle_selection(event)`: Menangani pemilihan dokumen.

### feedback_panel.py
- Kelas `FeedbackPanel(tk.Frame)`:
  - Menampilkan panel feedback dengan widget Text.
  - Fungsi:
    - `update_log(log_text)`: Memperbarui isi log yang ditampilkan.

### segmentation_preview_new.py
- Kelas `SegmentationPreview(tk.Frame)`:
  - Menampilkan preview gambar dokumen dengan segmentasi interaktif.
  - Fitur:
    - Navigasi halaman dokumen (next, previous).
    - Menampilkan dan mengatur posisi serta ukuran segmentasi (drag dan resize).
  - Fungsi utama:
    - `load_images(image_paths)`: Memuat gambar dokumen.
    - `set_segments_per_page(segments_per_page)`: Mengatur data segmentasi per halaman.
    - `display_segments(segments)`: Menampilkan segmentasi pada canvas.
    - Event handler untuk mouse (klik, drag, resize).

### validation_panel.py
- Kelas `ValidationPanel(tk.Frame)`:
  - Menampilkan daftar segmentasi dengan opsi untuk mengubah status.
  - Fungsi:
    - `load_segments(segments)`: Memuat data segmentasi.
    - `on_select(event)`: Menangani pemilihan segmentasi.
    - `update_status(new_status)`: Memperbarui status segmentasi dan memanggil callback.

## Catatan dan Saran Perbaikan
- Struktur kode sudah modular dengan pembagian fungsi yang jelas antar modul.
- Penanganan file gambar di `SegmentationPreview` dapat diperbaiki agar lebih fleksibel dan robust terhadap path file.
- Fungsi `upload_document` di `MainApp` masih placeholder, perlu implementasi upload file yang sesungguhnya.
- Perlu penambahan validasi input dan error handling terutama pada interaksi GUI.
- Dokumentasi kode inline (docstring) masih minim, sebaiknya ditambahkan untuk setiap kelas dan fungsi.
- Penggunaan logging untuk aktivitas penting dapat membantu debugging dan monitoring aplikasi.
- UI dapat ditingkatkan dengan styling dan responsivitas yang lebih baik.

---

Dokumentasi ini dibuat berdasarkan analisis kode sumber proyek GUI Segmentasi Dokumen.
