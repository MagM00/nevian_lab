import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np

# Initialize main app window
root = tk.Tk()
root.title("PPD File Data Explorer")
root.geometry("800x600")

# Global dataframe variable
df = pd.DataFrame()

# Function to load PPD file
def load_ppd_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("PPD Files", "*.ppd"), ("All Files", "*.*")])
    if file_path:
        try:
            df = pd.read_csv(file_path, sep='\t')  # Adjust separator as needed
            messagebox.showinfo("Success", "PPD file loaded successfully!")
            display_data(df)
            update_column_options()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

# Function to display data in Treeview
def display_data(data):
    # Clear existing treeview
    for widget in data_frame.winfo_children():
        widget.destroy()
    
    # Create treeview
    tree = ttk.Treeview(data_frame, columns=list(data.columns), show='headings')
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    # Insert rows
    for _, row in data.iterrows():
        tree.insert("", "end", values=list(row))
    
    tree.pack(fill="both", expand=True)

# Update column options in dropdowns
def update_column_options():
    columns = df.columns.tolist()
    column_select["values"] = columns
    column_select.current(0)  # Set default selection
    filter_column_select["values"] = columns
    filter_column_select.current(0)

# Function to calculate statistics
def calculate_stats():
    selected_col = column_select.get()
    if selected_col in df.columns:
        mean = df[selected_col].mean()
        median = df[selected_col].median()
        std_dev = df[selected_col].std()
        stats_text.set(f"Mean: {mean:.2f}\nMedian: {median:.2f}\nStd Dev: {std_dev:.2f}")
    else:
        messagebox.showerror("Error", "Select a valid column for statistics.")

# Function to filter data by column and range
def filter_data():
    filter_col = filter_column_select.get()
    if filter_col in df.columns:
        try:
            min_val = float(min_value.get())
            max_val = float(max_value.get())
            filtered_df = df[(df[filter_col] >= min_val) & (df[filter_col] <= max_val)]
            display_data(filtered_df)
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric values for filtering.")
    else:
        messagebox.showerror("Error", "Select a valid column to filter.")

# UI layout
load_button = tk.Button(root, text="Load PPD File", command=load_ppd_file)
load_button.pack(pady=10)

# Frame for data display
data_frame = tk.Frame(root)
data_frame.pack(fill="both", expand=True)

# Column selection for statistics
column_select_frame = tk.Frame(root)
column_select_frame.pack(pady=10)

tk.Label(column_select_frame, text="Select Column for Stats:").grid(row=0, column=0)
column_select = ttk.Combobox(column_select_frame, state="readonly")
column_select.grid(row=0, column=1)

calculate_button = tk.Button(column_select_frame, text="Calculate Stats", command=calculate_stats)
calculate_button.grid(row=0, column=2, padx=5)

# Display stats result
stats_text = tk.StringVar()
stats_label = tk.Label(root, textvariable=stats_text, font=("Arial", 10))
stats_label.pack(pady=5)

# Filtering options
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Filter Column:").grid(row=0, column=0)
filter_column_select = ttk.Combobox(filter_frame, state="readonly")
filter_column_select.grid(row=0, column=1)

tk.Label(filter_frame, text="Min Value:").grid(row=0, column=2)
min_value = tk.Entry(filter_frame, width=10)
min_value.grid(row=0, column=3)

tk.Label(filter_frame, text="Max Value:").grid(row=0, column=4)
max_value = tk.Entry(filter_frame, width=10)
max_value.grid(row=0, column=5)

filter_button = tk.Button(filter_frame, text="Apply Filter", command=filter_data)
filter_button.grid(row=0, column=6, padx=5)

# Run the app
root.mainloop()
