import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from data_import import import_ppd

def process_ppd(ppd_file_path, sampling_rate=130):
    # Extract the filename without the extension
    filename = os.path.splitext(os.path.basename(ppd_file_path))[0]

    # Load the data from the PPD file
    data = import_ppd(ppd_file_path, low_pass=20, high_pass=0.001)

    # Convert sample index to time vector
    time = np.arange(len(data['analog_1'])) / sampling_rate

    # dFF using 405 fit as baseline
    reg = np.polyfit(data['analog_2'], data['analog_1'], 1)  # ch1 is 465nm, ch2 is 405nm
    fit_405 = reg[0] * data['analog_2'] + reg[1]
    dFF = (data['analog_1'] - fit_405) / fit_405  # deltaF/F
    dFF = gaussian_filter1d(dFF, sigma=2)

    data['fit_405'] = fit_405
    data['dFF'] = dFF

    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot 1: Raw and fitted signals
    ax1.plot(time, data['analog_1'], label='analog_1')
    ax1.plot(time, data['analog_2'], label='analog_2')
    ax1.plot(time, data['fit_405'], label='fit_405', linestyle='--')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Signal Intensity')
    ax1.set_title('Raw Signals and Fitted Baseline')
    ax1.legend()

    # Plot 2: dFF signal
    ax2.plot(time, data['dFF'], label='dFF', color='orange')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('dFF')
    ax2.set_title('dFF Signal')
    ax2.legend()

    # Adjust layout and set the figure title
    plt.tight_layout()
    fig.suptitle(f'{filename} Data Overview', fontsize=14)
    fig.subplots_adjust(top=0.88)

    # Save and display the figure
    save_path = os.path.join(os.path.dirname(ppd_file_path), filename + '.png')
    fig.savefig(save_path, dpi=300)
    plt.show()

# Example PPD file paths
ppd_file_paths = [
    r'H:\Jun\sensory_stim\astro\control\1193-2024-08-22-131301.ppd',
    # Add more paths as needed
]

# Process and plot each PPD file
for ppd_file in ppd_file_paths:
    process_ppd(ppd_file)
