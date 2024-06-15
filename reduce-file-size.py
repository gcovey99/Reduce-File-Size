from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def reduce_image_size(input_image_path, output_image_path, quality):

    with Image.open(input_image_path) as img:
    
        # Convert the image to RGB mode if it's not already
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        
        # Save the image with the specified quality level
        img.save(output_image_path, "JPEG", quality=quality)
        
        # Get the file sizes before and after compression
        input_size = os.path.getsize(input_image_path)
        output_size = os.path.getsize(output_image_path)
        
        if output_size >= input_size:
            os.remove(output_image_path)
            messagebox.showinfo("Compression Result", "File cannot be compressed at this level.")
            return False
        
        percentage_diff = ((input_size - output_size) / input_size) * 100
        
        print(f"Original size: {input_size / 1024:.2f} KB")
        print(f"Compressed size: {output_size / 1024:.2f} KB")
        print(f"Percentage reduction: {percentage_diff:.2f}% \n")
        
        return True

def get_output_path(input_path):
 
    directory, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}-s{ext}"
    return os.path.join(directory, new_filename)

def select_files():
   
    root = tk.Tk()
    root.withdraw()

    quality = simpledialog.askinteger("Input Quality Percentage", "Enter the quality level (1-100):", minvalue=1, maxvalue=100)
    
    if quality is not None:
        file_paths = filedialog.askopenfilenames(
            title="Select image files",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        for file_path in file_paths:
            output_path = get_output_path(file_path)
            success = reduce_image_size(file_path, output_path, quality)
            if not success:
                print(f"Compression failed for {file_path}")


select_files()
