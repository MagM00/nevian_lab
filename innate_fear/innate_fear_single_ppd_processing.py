import os
import h5py
import tkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import zscore
from data_import import import_ppd

pre_start = 10
post_start = 20

# Define the PPD file path
ppd_file_path = r'H:\fp_test\innate_fear\142-2023-07-12-163112.ppd'

# Extract the filename without the extension
filename = os.path.splitext(os.path.basename(ppd_file_path))[0]

mouse_number = filename[0:3]

# Load the data from the CSV file
data = import_ppd(ppd_file_path, low_pass=20, high_pass=0.001)

# Convert sample index to time vector
time = np.arange(len(data['analog_1'])) / 130

# http://dx.doi.org/10.1016/j.cell.2015.07.014
# dFF using 405 fit as baseline
reg= np.polyfit(data['analog_2'], data['analog_1'], 1) # ch1 is 465nm, ch2 is 405nm 
fit_405=reg[0]*data['analog_2']+reg[1]
dFF=(data['analog_1']-fit_405)/fit_405 #this gives deltaF/F
data['fit_405']=fit_405
data['dFF']=dFF
ch1=data['analog_1']
ch2=data['analog_2']

timing_data = {
    '142': 
        {'Stim': [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1], 
         'Time': ['00:29', '01:04', '01:52', '02:24', '03:24', '04:15', '05:09', '05:58', '06:34', '07:18',
                  '08:16', '08:53', '09:49', '10:35', '11:29', '12:12', '12:47', '13:30', '14:15', '15:14',
                  '16:07', '17:02', '17:43', '18:26', '19:23', '20:20', '20:52', '21:26', '22:08', '23:06']}
}

stim_data = timing_data[mouse_number]['Stim']
time_stamps = timing_data[mouse_number]['Time']
sampling_rate = 130

def time_stamp_to_seconds(time_stamp):
    minutes, seconds = time_stamp.split(':')
    return int(minutes) * 60 + int(seconds)

water_indexes = [i for i, stim in enumerate(stim_data) if stim == 0]
tmt_indexes = [i for i, stim in enumerate(stim_data) if stim == 1]
all_indexes = [i for i, stim in enumerate(stim_data)]

water_time_stamps = [time_stamps[i] for i in water_indexes]
tmt_time_stamps = [time_stamps[i] for i in tmt_indexes]
all_time_stamps = [time_stamps[i] for i in all_indexes]

water_data_indexes = [int(time_stamp_to_seconds(time_stamp) * sampling_rate) for time_stamp in water_time_stamps]
tmt_data_indexes = [int(time_stamp_to_seconds(time_stamp) * sampling_rate) for time_stamp in tmt_time_stamps]
all_data_indexes = [int(time_stamp_to_seconds(time_stamp) * sampling_rate) for time_stamp in all_time_stamps]

# Create an empty matrix to store trace data
trace_data_matrix = []

# Plotting all traces
fig, ax = plt.subplots()

for index in all_data_indexes:
    start = int(index - pre_start * sampling_rate)
    end = int(index + post_start * sampling_rate)
    trace_data = dFF[start:end]
    time = np.arange(start, end) / sampling_rate

    # Calculate the baseline value
    baseline_start = int(index - 5 * sampling_rate)
    baseline_end = int(index - 3 * sampling_rate)
    baseline_mean = np.mean(dFF[baseline_start:baseline_end])
    baseline_std = np.std(dFF[baseline_start:baseline_end])

    # Compute the relative trace data
    relative_trace_data = (trace_data - baseline_mean) / baseline_std

    ax.plot(relative_trace_data)

    # Append relative_trace_data to the matrix
    trace_data_matrix.append(relative_trace_data)

ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Relative dFF')
ax.set_title('Traces of Mouse ' + mouse_number)
plt.show()

# Convert trace_data_matrix to a NumPy array
trace_data_matrix = np.array(trace_data_matrix)
trace_data_matrix_water = trace_data_matrix[water_indexes]
trace_data_matrix_tmt = trace_data_matrix[tmt_indexes]

# Calculate SEM for water and TMT
sem_water = np.std(trace_data_matrix_water, axis=0) / np.sqrt(trace_data_matrix_water.shape[0])
sem_tmt = np.std(trace_data_matrix_tmt, axis=0) / np.sqrt(trace_data_matrix_tmt.shape[0])

# Calculate the average trace for water and TMT
average_trace_water = np.mean(trace_data_matrix_water, axis=0)
average_trace_tmt = np.mean(trace_data_matrix_tmt, axis=0)

# Time array
time_array = np.arange(-pre_start, post_start, 1/sampling_rate)

plt.plot(time_array, average_trace_water, label='Water', color='blue')
plt.fill_between(time_array, average_trace_water - sem_water, average_trace_water + sem_water, color='blue', alpha=0.2)

plt.plot(time_array, average_trace_tmt, label='TMT', color='red')
plt.fill_between(time_array, average_trace_tmt - sem_tmt, average_trace_tmt + sem_tmt, color='red', alpha=0.2)

plt.axvline(x=0, color='k', linestyle='dashed')

plt.xlabel('Time (seconds)')
plt.ylabel('Average Relative dFF')
plt.title('Mouse ' + mouse_number)
plt.legend()
plt.show()

# Calculate the average trace for water and TMT
average_trace_water_early = np.mean(trace_data_matrix_water[0:4,:], axis=0)
average_trace_tmt_early = np.mean(trace_data_matrix_tmt[0:4,:], axis=0)
average_trace_water_late = np.mean(trace_data_matrix_water[10:14,:], axis=0)
average_trace_tmt_late = np.mean(trace_data_matrix_tmt[10:14,:], axis=0)

plt.plot(np.arange(-pre_start, post_start, 1/sampling_rate), average_trace_water_early, label='Water_early', color='blue')
plt.plot(np.arange(-pre_start, post_start, 1/sampling_rate), average_trace_tmt_early, label='TMT_early', color='red')
plt.plot(np.arange(-pre_start, post_start, 1/sampling_rate), average_trace_water_late, label='Water_late', color='green')
plt.plot(np.arange(-pre_start, post_start, 1/sampling_rate), average_trace_tmt_late, label='TMT_late', color='magenta')
plt.axvline(x=0, color='k', linestyle='dashed')
plt.xlabel('Time (seconds)')
plt.ylabel('Average Relative dFF')
plt.title('Mouse ' + mouse_number)
plt.legend()
plt.show()

