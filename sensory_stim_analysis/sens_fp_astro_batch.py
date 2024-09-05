import os
import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

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
    save_path = os.path.join(os.path.dirname(ppd_file_path), filename + '.png')
    fig.savefig(save_path, dpi=300)

    # Display the plots
    plt.show()

    # Index of np.diff(data['digital_1']) bigger than 0.5 or smaller than -0.5
    index_on = np.where(np.diff(data['digital_1']) > 0.5)[0]
    index_off = np.where(np.diff(data['digital_1']) < -0.5)[0]

    ttl_duration = index_off - index_on

    # Remove indexes with ttl_duration < 20
    indexes_to_remove = np.where(ttl_duration < 20)[0]
    index_on_new = np.delete(index_on, indexes_to_remove)
    index_off_new = np.delete(index_off, indexes_to_remove)
    ttl_duration_new = np.delete(ttl_duration, indexes_to_remove)

    time_on_new = index_on_new / sampling_rate

    return time_on_new

# List of PPD file paths
ppd_file_paths = [
    r'H:\Jun\sensory_stim\astro\control\1193-2024-08-22-131301.ppd',
    r'H:\Jun\sensory_stim\astro\control\1194-2024-08-22-151631.ppd',
    r'H:\Jun\sensory_stim\astro\control\1195-2024-08-22-165525.ppd',
    r'H:\Jun\sensory_stim\astro\control\1196-2024-08-23-103346.ppd',
    r'H:\Jun\sensory_stim\astro\control\1198-2024-08-23-142816.ppd',
    r'H:\Jun\sensory_stim\astro\control\1199-2024-08-23-164310.ppd',
    r'H:\Jun\sensory_stim\astro\control\1200-2024-08-26-112939.ppd',
    r'H:\Jun\sensory_stim\astro\control\1201-2024-08-26-151315.ppd'
]

# Process each PPD file
for ppd_file in ppd_file_paths:
    process_ppd(ppd_file)
