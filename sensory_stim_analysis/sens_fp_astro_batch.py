import os
import tkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from data_import import import_ppd
from scipy.signal import savgol_filter
from scipy.stats import sem
from scipy.ndimage import gaussian_filter1d, uniform_filter1d

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

    """     # Create the figure and subplots
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
    plt.show() """

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
    """ 
        # Organize data into a dictionary
    data = {
        'mouse': {
            'Stim': [
                1,1,1,3,3,3,2,2,2,0,0,0,5,5,5,6,6,6,4,4,4,
                6,6,6,2,2,2,3,3,3,4,4,4,5,5,5,1,1,1,0,0,0,
                4,4,4,1,1,1,2,2,2,5,5,5,3,3,3,6,6,6,0,0,0,
                6,6,6,0,0,0,5,5,5,1,1,1,2,2,2,4,4,4,3,3,3,
                4,4,4,6,6,6,1,1,1,5,5,5,0,0,0,2,2,2,3,3,3
            ],
            'Time': time_on_new.tolist()
        }
    }

    # Organize data into a dictionary
    data = {
        'mouse': {
            'Stim': [
                1,1,1,3,3,3,2,2,2,0,0,0,5,5,5,6,6,6,4,4,4,
                6,6,6,2,2,2,3,3,3,4,4,4,5,5,5,1,1,1,0,0,0,
                4,4,4,1,1,1,2,2,2,5,5,5,3,3,3,6,6,6,0,0,0,
                6,6,6,0,0,0,5,5,5,1,1,1,2,2,2,4, 4,4,3,3,3,
                4,4,4,6,6,6,1,1,1,5,5,5,0,0,0,2,2,2,3,3,3
            ],
            'Time': time_on_new.tolist()
        }
    }

    # Use `data` as needed in your analysis

    stim_data = data['mouse']['Stim']
    time_stamps = data['mouse']['Time']

    pinp_indexes = [i for i, stim in enumerate(stim_data) if stim == 0]
    weak_indexes = [i for i, stim in enumerate(stim_data) if stim == 1]
    mild_indexes = [i for i, stim in enumerate(stim_data) if stim == 2]
    hard_indexes = [i for i, stim in enumerate(stim_data) if stim == 3]
    cold_indexes = [i for i, stim in enumerate(stim_data) if stim == 4]
    room_indexes = [i for i, stim in enumerate(stim_data) if stim == 5]
    warm_indexes = [i for i, stim in enumerate(stim_data) if stim == 6]

    pinp_data_indexes = [round(float(time_stamps[i]) * sampling_rate) for i in pinp_indexes]
    weak_data_indexes = [round(float(time_stamps[i]) * sampling_rate) for i in weak_indexes]
    mild_data_indexes = [round(float(time_stamps[i]) * sampling_rate) for i in mild_indexes]
    hard_data_indexes = [round(float(time_stamps[i]) * sampling_rate) for i in hard_indexes]
    cold_data_indexes = [round(float(time_stamps[i]) * sampling_rate) for i in cold_indexes]
    room_data_indexes = [round(float(time_stamps[i]) * sampling_rate) for i in room_indexes]
    warm_data_indexes = [round(float(time_stamps[i]) * sampling_rate) for i in warm_indexes]


    trace_duration = 5  # 5 seconds before and 30 seconds after each data index

    # Convert trace duration from seconds to data points
    trace_duration_points = trace_duration * sampling_rate

    # Function to analyze and plot data for different index sets
    def analyze_and_plot(indexes, dFF, sampling_rate, pre_start=5, post_start=10):
        trace_data_matrix = []

        for index in indexes:
            start = int(index - pre_start * sampling_rate)
            end = int(index + post_start * sampling_rate)
            trace_data = dFF[start:end]
            time = np.arange(start, end) / sampling_rate

            # Calculate the baseline value
            baseline_start = int(index - 5 * sampling_rate)
            baseline_end = int(index - 3 * sampling_rate)
            baseline = np.mean(dFF[baseline_start:baseline_end])

            # Compute the relative trace data
            relative_trace_data = trace_data - baseline

            # Append relative_trace_data to the matrix
            trace_data_matrix.append(relative_trace_data)


        return np.array(trace_data_matrix)

    # Example usage for each data index set
    trace_data_matrix_pinp = analyze_and_plot(pinp_data_indexes, dFF, sampling_rate)
    trace_data_matrix_weak = analyze_and_plot(weak_data_indexes, dFF, sampling_rate)
    trace_data_matrix_mild = analyze_and_plot(mild_data_indexes, dFF, sampling_rate)
    trace_data_matrix_hard = analyze_and_plot(hard_data_indexes, dFF, sampling_rate)
    trace_data_matrix_cold = analyze_and_plot(cold_data_indexes, dFF, sampling_rate)
    trace_data_matrix_room = analyze_and_plot(room_data_indexes, dFF, sampling_rate)
    trace_data_matrix_warm = analyze_and_plot(warm_data_indexes, dFF, sampling_rate)

    # Calculate the average traces for each index set
    average_trace_pinp = np.mean(trace_data_matrix_pinp, axis=0)
    average_trace_weak = np.mean(trace_data_matrix_weak, axis=0)
    average_trace_mild = np.mean(trace_data_matrix_mild, axis=0)
    average_trace_hard = np.mean(trace_data_matrix_hard, axis=0)
    average_trace_cold = np.mean(trace_data_matrix_cold, axis=0)
    average_trace_room = np.mean(trace_data_matrix_room, axis=0)
    average_trace_warm = np.mean(trace_data_matrix_warm, axis=0)

    traces = {
        'average_trace_pinp': average_trace_pinp,
        'average_trace_weak': average_trace_weak,
        'average_trace_mild': average_trace_mild,
        'average_trace_hard': average_trace_hard,
        'average_trace_cold': average_trace_cold,
        'average_trace_room': average_trace_room,
        'average_trace_warm': average_trace_warm,
    } """

    # Define the file path and name
    #save_file_path = r'C:\files\data\sensory_stim\\ + file_name + '.npy'

    # Save the dictionary to a NumPy file
    #np.save(save_file_path, traces)

    vector = np.arange(index_on_new[0], index_on_new[0]+len(index_on_new)/2*60*130, 30*130)
    #print(filename)
    #print(np.round((index_on_new-vector)/130))
    gap = np.round((index_on_new-vector)/130*30)
    if len(index_on_new) != 105:
        print('Error in', filename, ', the number of stimulus detected is', len(index_on_new))
   
    """     y = uniform_filter1d(gap, size=5)
    plt.plot(y)
    plt.show()
    plt.close() """

    # Define stimulus event mapping
    stim_dict = {
        0: "0: Pinprick",
        1: "1: 0.07g-Green",
        2: "2: 0.4g-Dark blue",
        3: "3: 2g-Purple",
        4: "4: Cold water",
        5: "5: Room temp",
        6: "6: Hot water"
    }

    # Stimuli sequence (as provided in your example)
    stim_sequence = [
        1,1,1,3,3,3,2,2,2,0,0,0,5,5,5,6,6,6,4,4,4,
        6,6,6,2,2,2,3,3,3,4,4,4,5,5,5,1,1,1,0,0,0,
        4,4,4,1,1,1,2,2,2,5,5,5,3,3,3,6,6,6,0,0,0,
        6,6,6,0,0,0,5,5,5,1,1,1,2,2,2,4,4,4,3,3,3,
        4,4,4,6,6,6,1,1,1,5,5,5,0,0,0,2,2,2,3,3,3
    ]

    # Ensure index_on_new length matches stim_sequence
    if len(index_on_new) != len(stim_sequence):
        print(f"Error in {filename}, the number of stimulus detected is {len(index_on_new)}")
        df = pd.DataFrame({
        'Index': np.arange(1, len(index_on_new) + 1),
        'Event': 'stim',
        'Frame': gap,
        'Response': 1})
        
        # Define the file path and name for the Excel file
        excel_filename = f"{filename}.xlsx"
        excel_file_path = os.path.join(os.path.dirname(ppd_file_path), excel_filename)

        # Save the DataFrame as an Excel file
        df.to_excel(excel_file_path, index=False)

        print(f"Excel file saved as {excel_file_path}")
        return

    # Create the DataFrame
    df = pd.DataFrame({
        'Index': np.arange(1, len(stim_sequence) + 1),
        'Event': [stim_dict[stim] for stim in stim_sequence],
        'Frame': index_on_new,
        'Response': 1
    })

    # Define the file path and name for the Excel file
    excel_filename = f"{filename}.xlsx"
    excel_file_path = os.path.join(os.path.dirname(ppd_file_path), excel_filename)

    # Save the DataFrame as an Excel file
    df.to_excel(excel_file_path, index=False)

    print(f"Excel file saved as {excel_file_path}")

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

ppd_file_paths = [
    r'H:\Jun\sensory_stim\astro\sni\1193-2024-09-25-100942.ppd',
    r'H:\Jun\sensory_stim\astro\sni\1194-2024-09-25-124601.ppd',
    r'H:\Jun\sensory_stim\astro\sni\1195-2024-09-25-160328.ppd',
    r'H:\Jun\sensory_stim\astro\sni\1196-2024-09-26-140713.ppd',
    r'H:\Jun\sensory_stim\astro\sham\1198-2024-09-26-155349.ppd',
    r'H:\Jun\sensory_stim\astro\sham\1199-2024-09-27-114043.ppd',
    r'H:\Jun\sensory_stim\astro\sham\1200-2024-10-02-120908.ppd',
    r'H:\Jun\sensory_stim\astro\sham\1201-2024-10-01-144637.ppd'
]

# Process each PPD file
for ppd_file in ppd_file_paths:
    process_ppd(ppd_file)