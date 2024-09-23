import tkinter as tk
from tkinter import filedialog, messagebox, font
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO

# Convert a single image to a PDF
def image_to_pdf(image, pdf_path, quality=85, watermark_text=None, filter_type=None):
    if filter_type:
        image = apply_filter(image, filter_type)
    
    if watermark_text:
        image = add_watermark(image, watermark_text)
    
    image = compress_image(image, quality)
    image.save(pdf_path, "PDF", resolution=100.0)

# Convert multiple images to a single PDF
def images_to_pdf(image_paths, pdf_path, quality=85, watermark_text=None, filter_type=None):
    image_list = []

    for image_path in image_paths:
        img = Image.open(image_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        if filter_type:
            img = apply_filter(img, filter_type)
        
        if watermark_text:
            img = add_watermark(img, watermark_text)
        
        img = compress_image(img, quality)
        image_list.append(img)

    image_list[0].save(pdf_path, save_all=True, append_images=image_list[1:])
    messagebox.showinfo("Success", f"PDF created successfully at {pdf_path}")

# Apply basic filters to the image
def apply_filter(image, filter_type="grayscale"):
    if filter_type == "grayscale":
        return image.convert('L')
    elif filter_type == "blur":
        return image.filter(ImageFilter.BLUR)
    return image

# Compress the image to reduce file size
def compress_image(image, quality=85):
    img_io = BytesIO()
    image.save(img_io, 'JPEG', quality=quality)
    img_io.seek(0)
    return Image.open(img_io)

# Add watermark text to the image
def add_watermark(image, text="Watermark"):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    
    # Calculate text size using textbbox
    bbox = draw.textbbox((0, 0), text, font=font)
    textwidth, textheight = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Position watermark at the bottom right corner
    width, height = image.size
    x = width - textwidth - 10
    y = height - textheight - 10

    # Add watermark text
    draw.text((x, y), text, font=font)
    return image


# Open file dialog to select images
def open_file_dialog():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
    return file_paths

# Convert button functionality
def convert_images():
    images = open_file_dialog()
    if not images:
        messagebox.showwarning("No file selected", "Please select at least one image.")
        return

    pdf_output = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not pdf_output:
        return

    quality = int(quality_slider.get())
    watermark_text = watermark_entry.get() if watermark_var.get() else None
    filter_type = filter_var.get()

    if len(images) == 1:
        image_to_pdf(Image.open(images[0]), pdf_output, quality, watermark_text, filter_type)
    else:
        images_to_pdf(images, pdf_output, quality, watermark_text, filter_type)

# Build a more attractive GUI with Tkinter
root = tk.Tk()
root.title("Image to PDF Converter")
root.geometry("400x400")
root.configure(bg="#f5f5f5")

# Set a custom font
heading_font = font.Font(family="Helvetica", size=16, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=10, weight="bold")

# Title
title_label = tk.Label(root, text="Image to PDF Converter", font=heading_font, fg="#333", bg="#f5f5f5")
title_label.pack(pady=20)

# Watermark checkbox and entry
watermark_var = tk.IntVar()
watermark_check = tk.Checkbutton(root, text="Add Watermark", variable=watermark_var, font=label_font, fg="#333", bg="#f5f5f5")
watermark_check.pack(pady=5)

watermark_entry = tk.Entry(root, font=label_font, width=30)
watermark_entry.pack(pady=5)

# Filter selection
filter_var = tk.StringVar(value="none")
tk.Label(root, text="Apply Filter:", font=label_font, bg="#f5f5f5").pack(pady=5)

filters_frame = tk.Frame(root, bg="#f5f5f5")
filters_frame.pack(pady=5)

tk.Radiobutton(filters_frame, text="None", variable=filter_var, value="none", font=label_font, bg="#f5f5f5").grid(row=0, column=0)
tk.Radiobutton(filters_frame, text="Grayscale", variable=filter_var, value="grayscale", font=label_font, bg="#f5f5f5").grid(row=0, column=1)
tk.Radiobutton(filters_frame, text="Blur", variable=filter_var, value="blur", font=label_font, bg="#f5f5f5").grid(row=0, column=2)

# Compression slider
tk.Label(root, text="Image Quality (Compression):", font=label_font, bg="#f5f5f5").pack(pady=5)
quality_slider = tk.Scale(root, from_=10, to=100, orient='horizontal', font=label_font, bg="#f5f5f5")
quality_slider.set(85)
quality_slider.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert to PDF", command=convert_images, font=button_font, bg="#4CAF50", fg="white", height=2, width=20)
convert_button.pack(pady=20)

# Start the GUI loop
root.mainloop()
