import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import os

class ImageSplitterApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Image Splitter")
        self.geometry("800x600")

        self.image_frame = tk.Frame(self, bg="lightgrey")
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.split_slider = tk.Scale(self.control_frame, from_=0, to=800, orient=tk.HORIZONTAL, command=self.update_split_line)
        self.split_slider.pack(fill=tk.X)

        self.width_label = tk.Label(self.control_frame, text="Width:")
        self.width_label.pack(side=tk.LEFT)
        self.width_entry = tk.Entry(self.control_frame)
        self.width_entry.pack(side=tk.LEFT)

        self.height_label = tk.Label(self.control_frame, text="Height:")
        self.height_label.pack(side=tk.LEFT)
        self.height_entry = tk.Entry(self.control_frame)
        self.height_entry.pack(side=tk.LEFT)

        self.left_button = tk.Button(self.control_frame, text="Left", command=self.extract_left)
        self.left_button.pack(side=tk.LEFT, fill=tk.X)

        self.right_button = tk.Button(self.control_frame, text="Right", command=self.extract_right)
        self.right_button.pack(side=tk.LEFT, fill=tk.X)

        self.image_canvas = tk.Canvas(self.image_frame, bg="white")
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        self.split_line = None

        self.register_drop_target(self.image_frame)
        self.image_path = None

        self.bind("<Configure>", self.on_resize)

    def register_drop_target(self, widget):
        widget.drop_target_register(DND_FILES)
        widget.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        self.image_path = event.data.strip('{}')
        self.display_image()

    def display_image(self):
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image_width, self.image_height = self.image.size
            self.scale_and_display_image()

    def scale_and_display_image(self):
        if self.image_path:
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            # Calculate new dimensions to fit the image to the canvas height while maintaining aspect ratio
            scale_factor = canvas_height / self.image_height
            display_width = int(self.image_width * scale_factor)
            display_height = canvas_height

            self.display_image_resized = self.image.resize((display_width, display_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.display_image_resized)

            self.image_canvas.delete("all")
            x_offset = (canvas_width - display_width) // 2
            y_offset = 0  # No offset needed vertically since it's fit to the height
            self.image_canvas.create_image(x_offset, y_offset, anchor='nw', image=self.tk_image)

            self.split_slider.config(to=self.image_width)
            self.display_width = display_width
            self.display_height = display_height

            if self.split_line is not None:
                self.image_canvas.delete(self.split_line)
            self.split_line = self.image_canvas.create_line(self.split_slider.get() * scale_factor + x_offset, y_offset,
                                                           self.split_slider.get() * scale_factor + x_offset, display_height,
                                                           fill="red", width=2, dash=(2, 2))

    def update_split_line(self, value):
        if self.image_path:
            canvas_height = self.image_canvas.winfo_height()
            scale_factor = canvas_height / self.image_height
            x_offset = (self.image_canvas.winfo_width() - self.display_width) // 2
            x = int(value) * scale_factor + x_offset
            self.image_canvas.coords(self.split_line, x, 0, x, self.display_height)

    def extract_left(self):
        if self.image_path:
            try:
                target_width = int(self.width_entry.get())
                target_height = int(self.height_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for width and height.")
                return

            x = self.split_slider.get()
            left_image = self.image.crop((0, 0, x, self.image_height))

            resized_left_image = self.resize_and_align_image(left_image, target_width, target_height, align='right')

            self.save_image(resized_left_image, "left")

    def extract_right(self):
        if self.image_path:
            try:
                target_width = int(self.width_entry.get())
                target_height = int(self.height_entry.get())
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for width and height.")
                return

            x = self.split_slider.get()
            right_image = self.image.crop((x, 0, self.image_width, self.image_height))

            resized_right_image = self.resize_and_align_image(right_image, target_width, target_height, align='left')

            self.save_image(resized_right_image, "right")

    def resize_and_align_image(self, img, target_width, target_height, align='left'):
        img_aspect_ratio = img.width / img.height
        target_aspect_ratio = target_width / target_height

        # Calculate new dimensions to fit the image height to the target height
        new_height = target_height
        new_width = int(target_height * img_aspect_ratio)

        # Resize the image to the new dimensions
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        final_img = Image.new("RGB", (target_width, target_height), (255, 255, 255))

        # Determine horizontal offset based on alignment
        if align == 'left':
            x_offset = 0
        else:
            x_offset = target_width - new_width

        y_offset = 0  # Since we're fitting the image height to the target height, y_offset is 0

        # Paste the resized image onto the final image
        final_img.paste(resized_img, (x_offset, y_offset))

        return final_img

    def save_image(self, img, side):
        base_name = os.path.basename(self.image_path)
        name, ext = os.path.splitext(base_name)
        save_directory = os.path.dirname(self.image_path)
        save_path = os.path.join(save_directory, f"{name}_{side}{ext}")

        img.save(save_path, quality=95)

        messagebox.showinfo("Image Splitter", f"{side.capitalize()} half has been extracted and saved!\nPath: {save_path}")

    def on_resize(self, event):
        if self.image_path:
            self.scale_and_display_image()

if __name__ == "__main__":
    app = ImageSplitterApp()
    app.mainloop()
