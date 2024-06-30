from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def reduce_image_size(input_image_path, output_image_path, quality, text_widget):
    with Image.open(input_image_path) as img:
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output_image_path, "JPEG", quality=int(quality))

        input_size = os.path.getsize(input_image_path)
        output_size = os.path.getsize(output_image_path)

        if output_size >= input_size:
            os.remove(output_image_path)
            messagebox.showinfo("Compression Result", "File cannot be compressed at this level.")
            return False

        file_name = os.path.basename(input_image_path)
        
        percentage_diff = ((input_size - output_size) / input_size) * 100
        log_message = (f"File name: {file_name}\n"
                       f"Original size: {input_size / 1024:.2f} KB\n"
                       f"Compressed size: {output_size / 1024:.2f} KB\n"
                       f"Percentage reduced: {percentage_diff:.2f}%\n"
                       "---------------------------------------------\n")
        
        text_widget.insert(tk.END, log_message)
        text_widget.see(tk.END)

        return True

def get_output_path(input_path):
    directory, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}-s{ext}"
    return os.path.join(directory, new_filename)

def select_files(quality_entry, text_widget):
    quality = quality_entry.get()
    if not quality.isdigit() or int(quality) < 1 or int(quality) > 100:
        messagebox.showinfo("Error", "Please enter a valid quality percentage between 1-100.")
        return

    file_paths = filedialog.askopenfilenames(
        title="Select image files",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )

    for file_path in file_paths:
        output_path = get_output_path(file_path)
        success = reduce_image_size(file_path, output_path, quality, text_widget)
        if not success:
            log_message = f"Compression failed for {file_path}\n"
            text_widget.insert(tk.END, log_message)
            text_widget.see(tk.END)

def create_gui():
    root = tk.Tk()
    root.title("File Compression App")

    instructions = tk.Label(root, text="Select images to compress:")
    instructions.pack()

    quality_label = tk.Label(root, text="Enter the quality percentage level (1-100):")
    quality_label.pack()

    quality_entry = tk.Entry(root)
    quality_entry.pack()

    browse_button = tk.Button(root, text="Browse Images", command=lambda: select_files(quality_entry, text_widget))
    browse_button.pack()

    text_widget = tk.Text(root, height=25, width=85)
    text_widget.pack(padx=20, pady=20)  

    root.mainloop()

create_gui()
