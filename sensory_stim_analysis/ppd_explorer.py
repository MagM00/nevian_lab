import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from data_import import import_ppd
from tkinter import Tk, filedialog

def process_ppd(ppd_file_path, sampling_rate=130, plot_type="both"):
    """
    Process and plot PPD data.
    
    Parameters:
    - ppd_file_path (str): Path to the PPD file.
    - sampling_rate (int): Sampling rate of the data.
    - plot_type (str): "individual" for individual trials, "average" for average trial, "both" for both.
    """
    # Extract the filename without the extension
    filename = os.path.splitext(os.path.basename(ppd_file_path))[0]

    # Load the data from the PPD file
    data = import_ppd(ppd_file_path, low_pass=20, high_pass=0.001)

    # Convert sample index to time vector
    time = np.arange(len(data['analog_1'])) / sampling_rate

    # dFF calculation using 405 fit as baseline
    reg = np.polyfit(data['analog_2'], data['analog_1'], 1)  # ch1 is 465nm, ch2 is 405nm
    fit_405 = reg[0] * data['analog_2'] + reg[1]
    dFF = (data['analog_1'] - fit_405) / fit_405  # deltaF/F
    dFF = gaussian_filter1d(dFF, sigma=2)

    data['fit_405'] = fit_405
    data['dFF'] = dFF

    # Separate trials if data contains trial information (assuming data['trial'] column exists)

    # No trial data, plot just the main signals and dFF
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.plot(time, data['analog_1'], label='analog_1')
    ax1.plot(time, data['analog_2'], label='analog_2')
    ax1.plot(time, data['fit_405'], label='fit_405', linestyle='--')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Signal Intensity')
    ax1.set_title('Raw Signals and Fitted Baseline')
    ax1.legend()

    ax2.plot(time, data['dFF'], label='dFF', color='orange')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('dFF')
    ax2.set_title('dFF Signal')
    ax2.legend()

    plt.tight_layout()
    fig.suptitle(f'{filename} Data Overview', fontsize=14)
    fig.subplots_adjust(top=0.88)
    plt.show()

# Main code to select a PPD file and choose plot type
def main():
    # Open file dialog to select PPD file
    root = Tk()
    root.withdraw()  # Hide the main tkinter window
    ppd_file_path = filedialog.askopenfilename(title="Select a PPD file", filetypes=[("PPD files", "*.ppd")])

    if not ppd_file_path:
        print("No file selected.")
        return

    # Process and plot the selected PPD file
    process_ppd(ppd_file_path)

# Run the main function
if __name__ == "__main__":
    main()
