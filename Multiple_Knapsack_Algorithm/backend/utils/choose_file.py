import tkinter as tk
from tkinter import filedialog

def choose_file():
    file_path = filedialog.askdirectory()
    if file_path:
        print("Selected File:", file_path)
    else:
        print("No file selected.")
    
    return file_path