import os
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Data import function for PPD files (simulating import_ppd from data_import.py)
def import_ppd(filepath):
    try:
        data = pd.read_csv(filepath, sep="\t", skiprows=15, usecols=[0, 1], names=["Time", "Value"])
        data.dropna(inplace=True)  # Remove any rows with missing values
        return data
    except Exception as e:
        raise Exception(f"Failed to import PPD file: {e}")

# Process PPD function
def process_ppd(filepath, sampling_rate):
    try:
        data = import_ppd(filepath)
        
        # Calculate time step based on sampling rate
        dt = 1 / sampling_rate
        data["Time"] = data.index * dt  # Adjust time based on index and sampling rate
        
        # Save the processed data to a new CSV file
        output_filepath = os.path.splitext(filepath)[0] + "_processed.csv"
        data.to_csv(output_filepath, index=False)
        
        return output_filepath
    except Exception as e:
        raise Exception(f"Error processing file: {e}")

# Function to select file
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PPD Files", "*.ppd")])
    file_path_var.set(file_path)

# Function to process the file
def process_file():
    file_path = file_path_var.get()
    sampling_rate = sampling_rate_var.get()
    
    if not file_path:
        messagebox.showerror("Error", "Please select a PPD file.")
        return
    
    try:
        sampling_rate = int(sampling_rate)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for sampling rate.")
        return
    
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", "Invalid file path.")
        return
    
    try:
        # Process file and get the output filepath
        output_filepath = process_ppd(file_path, sampling_rate)
        messagebox.showinfo("Success", f"File processed successfully.\nOutput saved to {output_filepath}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Set up the main application window
root = tk.Tk()
root.title("PPD Data Processor")

# File selection
file_path_var = tk.StringVar()
tk.Label(root, text="Select PPD File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=file_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_file).grid(row=0, column=2, padx=10, pady=10)

# Sampling rate input
sampling_rate_var = tk.StringVar(value="130")  # Default sampling rate
tk.Label(root, text="Sampling Rate (Hz):").grid(row=1, column=0, padx=10, pady=10, sticky="e")
tk.Entry(root, textvariable=sampling_rate_var, width=10).grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Process button
tk.Button(root, text="Process File", command=process_file, width=20).grid(row=2, column=0, columnspan=3, padx=10, pady=20)

# Run the main loop
root.mainloop()
