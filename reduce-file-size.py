from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def reduceImageSize(input_image_path, output_image_path, quality, width, text_widget):
    with Image.open(input_image_path) as img:
        original_size = img.size
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Resize the image based on the width
        if width:
            aspect_ratio = img.height / img.width
            newHeight = int(width * aspect_ratio)
            img = img.resize((width, newHeight), Image.Resampling.LANCZOS)

        img.save(output_image_path, "JPEG", quality=int(quality))
        input_size = os.path.getsize(input_image_path)
        output_size = os.path.getsize(output_image_path)

        if output_size >= input_size:
            os.remove(output_image_path)
            messagebox.showinfo("Compression Result", "File cannot be compressed at this level.")
            return False

        fileName = os.path.basename(input_image_path)
        percentage_diff = ((input_size - output_size) / input_size) * 100
        log_message = (f"Original file name: {fileName}\n"
                       f"Original size: {input_size / 1024:.2f} KB\n"
                       f"New size: {output_size / 1024:.2f} KB\n"
                       f"Original dimensions: {original_size}\n"
                       f"New dimensions: {img.size}\n"
                       f"Percentage reduced: {percentage_diff:.2f}%\n"
                       "---------------------------------------------\n")
        
        text_widget.insert(tk.END, log_message)
        text_widget.see(tk.END)

        return True

def getOutputPath(input_path):
    directory, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}-s{ext}"
    return os.path.join(directory, new_filename)

def select_files(quality_entry, width_entry, text_widget):
    quality = quality_entry.get()
    width = width_entry.get()
    if not quality.isdigit() or int(quality) < 1 or int(quality) > 100:
        messagebox.showinfo("Error", "Please enter a valid quality percentage between 1-100.")
        return

    width = int(width) if width.isdigit() else None  # Only convert to int if it's a digit

    file_paths = filedialog.askopenfilenames(
        title="Select image files",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
    )

    for file_path in file_paths:
        output_path = getOutputPath(file_path)
        success = reduceImageSize(file_path, output_path, quality, width, text_widget)
        if not success:
            log_message = f"Compression failed for {file_path}\n"
            text_widget.insert(tk.END, log_message)
            text_widget.see(tk.END)

def windowGUI():
    root = tk.Tk()
    root.title("File Compression App")

    instructions = tk.Label(root, text="Select images to compress:")
    instructions.pack()

    #quality entry
    quality_label = tk.Label(root, text="Quality (1-100):")
    quality_label.pack()

    quality_entry = tk.Entry(root)
    quality_entry.pack()

    #width entry
    width_label = tk.Label(root, text="Image Resize (Change the width of the image):")
    width_label.pack()

    width_entry = tk.Entry(root)
    width_entry.pack()

    browse_button = tk.Button(root, text="Browse Images", command=lambda: select_files(quality_entry, width_entry, text_widget))
    browse_button.pack()

    text_widget = tk.Text(root, height=25, width=85)
    text_widget.pack(padx=20, pady=20)  

    root.mainloop()

windowGUI()
