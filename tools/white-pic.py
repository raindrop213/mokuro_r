import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk, ImageOps
import os

class ImageProcessorApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Processor")
        self.geometry("800x600")

        self.image_frame = tk.Frame(self, bg="lightgrey")
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        self.image_canvas = tk.Canvas(self.image_frame, bg="white")
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        self.register_drop_target(self.image_frame)
        self.image_path = None

        self.bind("<Configure>", self.on_resize)

    def register_drop_target(self, widget):
        widget.drop_target_register(DND_FILES)
        widget.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        self.image_path = event.data.strip('{}')
        self.create_white_image()

    def create_white_image(self):
        if self.image_path:
            original_image = Image.open(self.image_path)
            white_image = ImageOps.colorize(ImageOps.grayscale(original_image), black="white", white="white")

            base_name = os.path.basename(self.image_path)
            name, ext = os.path.splitext(base_name)
            save_directory = os.path.dirname(self.image_path)
            white_image_path = os.path.join(save_directory, f"{name}a{ext}")

            white_image.save(white_image_path)

            messagebox.showinfo("Image Processor", f"White image has been created and saved as: {white_image_path}")
            self.display_image(white_image_path)

    def display_image(self, image_path):
        if image_path:
            self.image = Image.open(image_path)
            self.image_width, self.image_height = self.image.size
            self.scale_and_display_image()

    def scale_and_display_image(self):
        if self.image_path:
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            # Calculate scale factor to fit image within the canvas
            scale_factor = min(canvas_width / self.image_width, canvas_height / self.image_height)
            display_width = int(self.image_width * scale_factor)
            display_height = int(self.image_height * scale_factor)

            self.display_image_resized = self.image.resize((display_width, display_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.display_image_resized)

            self.image_canvas.delete("all")
            x_offset = (canvas_width - display_width) // 2
            y_offset = (canvas_height - display_height) // 2
            self.image_canvas.create_image(x_offset, y_offset, anchor='nw', image=self.tk_image)

    def on_resize(self, event):
        if self.image_path:
            self.scale_and_display_image()

if __name__ == "__main__":
    app = ImageProcessorApp()
    app.mainloop()
