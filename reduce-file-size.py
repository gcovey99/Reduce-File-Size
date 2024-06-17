from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def reduce_image_size(input_image_path, output_image_path, quality, text_widget):
    """
    Reduces the file size of an image while maintaining its appearance.
    
    Parameters:
        input_image_path (str): Path to the input image file.
        output_image_path (str): Path to save the output image file.
        quality (int): Quality level to save the image (1-100). Lower values mean more compression.
        text_widget (tk.Text): The Text widget to display log messages.
    """
    # Open the image file
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
        
        log_message = (f"Original size: {input_size / 1024:.2f} KB\n"
                       f"Compressed size: {output_size / 1024:.2f} KB\n"
                       f"Percentage reduction: {percentage_diff:.2f}%\n")
        
        text_widget.insert(tk.END, log_message)
        text_widget.see(tk.END)
        
        return True

def get_output_path(input_path):
    """
    Generates an output file path by appending '-s' to the original file name.
    
    Parameters:
        input_path (str): Path to the input image file.
        
    Returns:
        str: Path to save the compressed image file.
    """
    directory, filename = os.path.split(input_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}-s{ext}"
    return os.path.join(directory, new_filename)

def select_files(text_widget):
    """
    Opens a file picker dialog to select multiple image files and then reduces their size.
    
    Parameters:
        text_widget (tk.Text): The Text widget to display log messages.
    """
    quality = simpledialog.askinteger("Input Quality", "Enter the quality level (1-100):", minvalue=1, maxvalue=100)
    
    if quality is not None:
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
    """
    Creates the main GUI window for the image compression tool.
    """
    root = tk.Tk()
    root.title("Image Compression Tool")

    canvas = tk.Canvas(root, width=500, height=400)
    canvas.pack()

    instructions = tk.Label(root, text="Select images to compress:")
    canvas.create_window(250, 50, window=instructions)

    log_label = tk.Label(root, text="Log:")
    canvas.create_window(250, 250, window=log_label)

    text_widget = tk.Text(root, height=10, width=60)
    canvas.create_window(250, 320, window=text_widget)

    browse_button = tk.Button(text="Browse", command=lambda: select_files(text_widget))
    canvas.create_window(250, 150, window=browse_button)

    root.mainloop()

# Run the GUI
create_gui()
