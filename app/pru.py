#!/usr/bin/python3
from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.title("ImageTk Test")

image = Image.open("/home/sistemas/projects/temporal_pdf/app/logo.jpeg")
logo_image_path = ImageTk.PhotoImage(image)

label = tk.Label(root, image=logo_image_path)
label.pack()

root.mainloop()
