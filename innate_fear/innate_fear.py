import os
import h5py
import glob
import tkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import zscore
from data_import import import_ppd

sampling_rate = 130

def process_ppd_file(ppd_file_path):
    # Extract the filename without the extension
    filename = os.path.splitext(os.path.basename(ppd_file_path))[0]

    # Load the data from the PPD file
    data = import_ppd(ppd_file_path, low_pass=20, high_pass=0.001)

    # Convert sample index to time vector
    time = np.arange(len(data['analog_1'])) / sampling_rate

    # Calculate dFF using 405 fit as baseline
    reg = np.polyfit(data['analog_2'], data['analog_1'], 1)  # ch1 is 465nm, ch2 is 405nm
    fit_405 = reg[0] * data['analog_2'] + reg[1]
    dFF = (data['analog_1'] - fit_405) / fit_405
    data['fit_405'] = fit_405
    data['dFF'] = dFF

    return filename, data, time

def plot_data(filename, data, time):
    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot 1
    ax1.plot(time, data['analog_1'], label='analog_1')
    ax1.plot(time, data['analog_2'], label='analog_2')
    ax1.plot(time, data['fit_405'], label='fit_405')

    # Set plot 1 properties
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Value')
    ax1.set_title('Plot 1')
    ax1.legend()

    # Plot 2
    ax2.plot(time, data['dFF'], label='dFF')

    # Set plot 2 properties
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Value')
    ax2.set_title('Plot 2')
    ax2.legend()

    # Adjust spacing between subplots
    plt.tight_layout()

    # Set the figure title
    fig.suptitle(filename)

    # Save the figure as PNG with 300 dpi
    save_path = os.path.join(folder_path, filename + '.png')
    fig.savefig(save_path, dpi=300)

    # Display the plots
    plt.show()

def process_ppd_files(folder_path):
    # Find all PPD files in the folder
    ppd_files = glob.glob(os.path.join(folder_path, '*.ppd'))

    # Loop through each PPD file
    for ppd_file_path in ppd_files:
        # Process the PPD file
        filename, data, time = process_ppd_file(ppd_file_path)

        # Plot and save the data
        plot_data(filename, data, time)
        

# Define the PPD files folder path
folder_path = r'H:\fp_test\innate_fear'

# Process and plot the PPD files in the folder
process_ppd_files(folder_path)

