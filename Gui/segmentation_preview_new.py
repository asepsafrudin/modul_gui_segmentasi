import os
import tkinter as tk
from PIL import Image, ImageTk

class SegmentationPreview(tk.Frame):
    HANDLE_SIZE = 8

    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill="both", expand=True)

        nav_frame = tk.Frame(self)
        nav_frame.pack(side="bottom", fill="x")

        self.prev_button = tk.Button(nav_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side="left", padx=5, pady=5)

        self.page_label = tk.Label(nav_frame, text="", font=("Arial", 12))
        self.page_label.pack(side="left", padx=5)

        self.next_button = tk.Button(nav_frame, text="Next", command=self.next_page)
        self.next_button.pack(side="left", padx=5, pady=5)

        self.images = []  # List of PIL Images for pages
        self.original_images = []  # Original images for scaling
        self.photo = None
        self.segments_per_page = {}  # Dict of page index to segments list
        self.current_page = 0

        self.rect_items = {}
        self.handle_items = {}
        self.current_action = None  # 'move' or 'resize'
        self.current_segment_id = None
        self.current_handle = None
        self.start_x = 0
        self.start_y = 0

        self.scale_ratio = 1.0

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Configure>", self.on_resize)

    def load_images(self, image_paths):
        self.images.clear()
        self.original_images.clear()
        self.segments_per_page.clear()
        for path in image_paths:
            if not os.path.isabs(path):
                base_dir = os.path.dirname(os.path.abspath(__file__))
                possible_paths = [
                    os.path.join(base_dir, path),
                    os.path.join(base_dir, '..', path),
                    os.path.join(base_dir, '..', 'public', os.path.basename(path)),
                    os.path.join(base_dir, os.path.basename(path)),
                ]
                for p in possible_paths:
                    if os.path.exists(p):
                        path = p
                        break
                else:
                    raise FileNotFoundError(f"Image file not found in expected locations: {possible_paths}")
            image = Image.open(path)
            self.original_images.append(image)
        self.current_page = 0
        self._resize_image_to_canvas()
        self.update_page_label()
        self.display_segments(self.segments_per_page.get(self.current_page, []))

    def set_segments_per_page(self, segments_per_page):
        """
        Set the segments data per page.
        segments_per_page: dict mapping page index to list of segments
        """
        self.segments_per_page = segments_per_page
        # Refresh display for current page
        self.display_segments(self.segments_per_page.get(self.current_page, []))

    def _resize_image_to_canvas(self):
        if not self.original_images or self.current_page >= len(self.original_images):
            return
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(100, self._resize_image_to_canvas)
            return
        orig_image = self.original_images[self.current_page]
        orig_width, orig_height = orig_image.size
        ratio = min(canvas_width / orig_width, canvas_height / orig_height)
        self.scale_ratio = ratio
        new_size = (int(orig_width * ratio), int(orig_height * ratio))
        resized_image = orig_image.resize(new_size, Image.Resampling.LANCZOS)
        self.images = resized_image
        self.photo = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.display_segments(self.segments_per_page.get(self.current_page, []))

    def display_segments(self, segments):
        self.canvas.delete("all")
        if self.photo:
            self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.rect_items.clear()
        self.handle_items.clear()
        self.segments = segments
        for seg in segments:
            self._draw_segment(seg)

    def _draw_segment(self, seg):
        x = seg["x"] * self.scale_ratio
        y = seg["y"] * self.scale_ratio
        w = seg["w"] * self.scale_ratio
        h = seg["h"] * self.scale_ratio
        color = self._get_color(seg["type"])
        rect_id = self.canvas.create_rectangle(x, y, x + w, y + h, outline=color, width=2, tags=("segment", seg["id"]))
        self.rect_items[seg["id"]] = rect_id
        handles = {}
        for cx, cy, tag in [
            (x, y, "nw"), (x + w, y, "ne"), (x, y + h, "sw"), (x + w, y + h, "se")
        ]:
            handle_id = self.canvas.create_rectangle(cx - self.HANDLE_SIZE//2, cy - self.HANDLE_SIZE//2,
                                                     cx + self.HANDLE_SIZE//2, cy + self.HANDLE_SIZE//2,
                                                     fill=color, outline=color, tags=("handle", seg["id"], tag))
            handles[tag] = handle_id
        self.handle_items[seg["id"]] = handles
        self.canvas.create_text(x, max(y - 10, 10), text=f"{seg['type']}: {seg.get('text', '')[:20]}",
                                anchor="nw", fill=color, font=("Arial", 10, "bold"))

    def _get_color(self, type_):
        return {
            "Header": "blue",
            "Teks Utama": "red",
            "Tanda Tangan": "yellow",
            "Tabel": "green",
            "Gambar": "green",
        }.get(type_, "gray")

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        handle = self._find_handle(event.x, event.y)
        if handle:
            self.current_action = "resize"
            self.current_segment_id, self.current_handle = handle
            return
        segment_id = self._find_segment(event.x, event.y)
        if segment_id:
            self.current_action = "move"
            self.current_segment_id = segment_id
            return
        self.current_action = None
        self.current_segment_id = None
        self.current_handle = None

    def on_mouse_move(self, event):
        if not self.current_action or not self.current_segment_id:
            return
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        seg = next((s for s in self.segments if s["id"] == self.current_segment_id), None)
        if not seg:
            return
        dx_orig = dx / self.scale_ratio
        dy_orig = dy / self.scale_ratio
        if self.current_action == "move":
            seg["x"] += dx_orig
            seg["y"] += dy_orig
        elif self.current_action == "resize":
            if self.current_handle == "nw":
                seg["x"] += dx_orig
                seg["y"] += dy_orig
                seg["w"] -= dx_orig
                seg["h"] -= dy_orig
            elif self.current_handle == "ne":
                seg["y"] += dy_orig
                seg["w"] += dx_orig
                seg["h"] -= dy_orig
            elif self.current_handle == "sw":
                seg["x"] += dx_orig
                seg["w"] -= dx_orig
                seg["h"] += dy_orig
            elif self.current_handle == "se":
                seg["w"] += dx_orig
                seg["h"] += dy_orig
            if seg["w"] < 10:
                seg["w"] = 10
            if seg["h"] < 10:
                seg["h"] = 10
        self.start_x = event.x
        self.start_y = event.y
        self.display_segments(self.segments)

    def on_mouse_up(self, event):
        self.current_action = None
        self.current_segment_id = None
        self.current_handle = None

    def _find_handle(self, x, y):
        items = self.canvas.find_overlapping(x, y, x, y)
        for item in items:
            tags = self.canvas.gettags(item)
            if "handle" in tags:
                segment_id = tags[1]
                handle_pos = tags[2]
                return segment_id, handle_pos
        return None

    def _find_segment(self, x, y):
        items = self.canvas.find_overlapping(x, y, x, y)
        for item in items:
            tags = self.canvas.gettags(item)
            if "segment" in tags:
                return tags[1]
        return None

    def on_resize(self, event):
        self._resize_image_to_canvas()

    def update_page_label(self):
        total_pages = len(self.original_images)
        if total_pages > 0:
            self.page_label.config(text=f"Page {self.current_page + 1} of {total_pages}")
        else:
            self.page_label.config(text="No pages")

    def next_page(self):
        if self.current_page + 1 < len(self.original_images):
            self.current_page += 1
            self._resize_image_to_canvas()
            self.display_segments(self.segments_per_page.get(self.current_page, []))
            self.update_page_label()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._resize_image_to_canvas()
            self.display_segments(self.segments_per_page.get(self.current_page, []))
            self.update_page_label()

