import os
import h5py
import tkinter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import zscore
from data_import import import_ppd

# Set the PPD files directory
ppd_files_dir = r'H:\fp_test\innate_fear'

# Get a list of all PPD files in the directory
ppd_files = [f for f in os.listdir(ppd_files_dir) if f.endswith('.ppd')]

timing_data = {
        '140': 
            {'Stim': [0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0], 
             'Time': ['00:29', '01:27', '01:58', '02:28', '03:22', '03:56', '04:35', '05:23', '06:23', '07:22', 
                      '08:09', '08:55', '09:38', '10:12', '10:53', '11:32', '12:14', '12:59', '13:33', '14:10', 
                      '15:02', '15:34', '16:08', '16:41', '17:37', '18:08', '18:50', '19:21', '19:59', '20:58']}, 
        '142': 
            {'Stim': [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1], 
             'Time': ['00:29', '01:04', '01:52', '02:24', '03:24', '04:15', '05:09', '05:58', '06:34', '07:18',
                      '08:16', '08:53', '09:49', '10:35', '11:29', '12:12', '12:47', '13:30', '14:15', '15:14',
                      '16:07', '17:02', '17:43', '18:26', '19:23', '20:20', '20:52', '21:26', '22:08', '23:06']}, 
        '514': 
            {
            'Stim': [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0], 
            'Time': ['00:29', '01:16', '01:46', '02:27', '03:10', '03:42', '04:18', '04:58', '05:31', '06:28', 
                     '07:27', '08:10', '08:41', '09:22', '10:17', '11:12', '12:03', '12:59', '13:35', '14:21', 
                     '15:12', '16:10', '16:51', '17:39', '18:13', '18:46', '19:35', '20:31', '21:21', '22:12']}, 
        '516': 
            {'Stim': [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0], 
             'Time': ['00:30', '01:29', '02:07', '02:48', '03:39', '04:19', '04:59', '05:46', '06:20', '06:50', 
                      '07:49', '08:38', '09:37', '10:19', '11:16', '12:03', '12:42', '13:34', '14:08', '14:53', 
                      '15:25', '16:12', '16:56', '17:41', '18:11', '19:06', '19:43', '20:27', '21:02', '22:02']}, 
        '517': 
            {'Stim': [0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1] ,
            'Time': ['00:30', '01:25', '02:24', '03:12', '03:45', '04:17', '04:52', '05:38', '06:09', '06:44', 
                    '07:30', '08:17', '08:49', '09:42', '10:31', '11:30', '12:26', '13:23', '14:11', '15:08', 
                    '15:57', '16:30', '17:10', '18:06', '18:39', '19:33', '20:25', '21:21', '22:01', '22:34'] }, 
        '518': 
            {'Stim': [1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1], 
             'Time': ['00:30', '01:26', '02:22', '03:00', '03:46', '04:45', '05:44', '06:16', '06:47', '07:19', 
                    '08:07', '08:53', '09:39', '10:30', '11:21', '12:06', '12:38', '13:16', '14:08', '14:57', 
                    '15:48', '16:40', '17:26', '18:04', '18:56', '19:49', '20:29', '21:22', '22:22', '23:17']}, 
        '519': 
            {'Stim': [0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
             'Time': ['00:30', '01:09', '01:42', '02:21', '03:15', '04:06', '05:03', '05:47', '06:17', '07:13', 
                    '08:02', '08:32', '09:05', '09:44', '10:25', '11:03', '11:45', '12:18', '12:54', '13:44',
                    '14:34', '15:05', '15:39', '16:14', '17:02', '17:37', '18:34', '19:14', '19:58', '20:52']}, 
        '520': {
            'Stim': [0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0],
            'Time': ['00:33', '01:14', '01:55', '02:44', '03:23', '04:22', '05:10', '06:02', '06:55', '07:39', 
                    '08:34', '09:17', '10:08', '10:51', '11:45', '12:44', '13:28', '14:05', '15:00', '15:50', 
                    '16:35', '17:24', '18:09', '19:03', '19:39', '20:30', '21:06', '21:55', '22:31', '23:18']},

        '521': 
            {
            'Stim': [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0],
            'Time': ['00:29', '01:23', '02:10', '03:00', '03:56', '04:34', '05:22', '06:06', '07:00', '07:41',
                     '08:20', '08:53', '09:44', '10:20', '11:20', '11:55', '12:41', '13:41', '14:19', '15:01',
                     '15:48', '16:26', '17:15', '17:48', '18:31', '19:27', '20:16', '20:50', '21:20', '22:13']}, 

        '522': 
            {'Stim': [1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1],
            'Time': ['00:29', '01:27', '02:07', '02:42', '03:27', '03:58', '04:32', '05:31', '06:10', '06:53',
                     '07:38', '08:24', '09:00', '09:50', '10:47', '11:42', '12:24', '13:08', '13:54', '14:53',
                     '15:35', '16:25', '17:13', '18:03', '18:34', '19:04', '19:51', '20:47', '21:18', '21:58']}, 

        '523': 
            {'Stim': [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1], 
            'Time': ['00:29', '01:05', '01:42', '02:18', '03:12', '03:45', '04:45', '05:19', '06:01', '06:42', 
             '07:27', '08:27', '09:20', '10:12', '11:11', '12:00', '12:59', '13:33', '14:10', '14:47', 
             '15:25', '16:02', '16:50', '17:45', '18:37', '19:29', '20:26', '21:20', '22:08', '22:57']}, 

        '524': 
            {'Stim': [0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1], 
             'Time': ['00:30', '01:02', '01:47', '02:39', '03:22', '04:17', '05:04', '05:52', '06:39', '07:12', 
                    '07:42', '08:14', '09:14', '10:03', '10:39', '11:23', '12:15', '12:56', '13:52', '14:31', 
                    '15:07', '15:42', '16:37', '17:17', '18:15', '19:09', '20:08', '20:39', '21:19', '22:12']}, 

        '525': 
            {'Stim': [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0,], 
             'Time': ['00:30', '01:06', '01:49', '02:29', '03:04', '04:01', '04:40', '05:25', '06:12', '06:48',
                     '07:34', '08:31', '09:10', '09:52', '10:43', '11:24', '12:00', '12:41', '13:13', '13:58', 
                     '14:53', '15:29', '17:06', '17:48', '18:23', '18:57', '19:56', '20:46', '21:18', '22:00']}}

trace_water_all = []
trace_tmt_all = []
trace_water_early_all = []
trace_tmt_early_all = []
trace_water_inter_all = []
trace_tmt_inter_all = []
trace_water_late_all = []
trace_tmt_late_all = []
    
    # Iterate over each PPD file in the directory
for ppd_file in ppd_files:
    ppd_file_path = os.path.join(ppd_files_dir, ppd_file)
    
    pre_start = 10
    post_start = 16
    
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
        relative_trace_data = (trace_data - baseline_mean)# / baseline_std
        
        # Append relative_trace_data to the matrix
        trace_data_matrix.append(relative_trace_data)
    
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
    
    #Calculate the average trace for water and TMT
    average_trace_water_early = np.mean(trace_data_matrix_water[0:5,:], axis=0)
    average_trace_tmt_early = np.mean(trace_data_matrix_tmt[0:5,:], axis=0)
    average_trace_water_inter = np.mean(trace_data_matrix_water[5:10,:], axis=0)
    average_trace_tmt_inter = np.mean(trace_data_matrix_tmt[5:10,:], axis=0)
    average_trace_water_late = np.mean(trace_data_matrix_water[10:15,:], axis=0)
    average_trace_tmt_late = np.mean(trace_data_matrix_tmt[10:15,:], axis=0)
    
    trace_water_all.append(average_trace_water)
    trace_tmt_all.append(average_trace_tmt)
    trace_water_early_all.append(average_trace_water_early)
    trace_tmt_early_all.append(average_trace_tmt_early)
    trace_water_inter_all.append(average_trace_water_inter)
    trace_tmt_inter_all.append(average_trace_tmt_inter)
    trace_water_late_all.append(average_trace_water_late)
    trace_tmt_late_all.append(average_trace_tmt_late)

# Calculate the mean and SEM for each list
mean_trace_water = np.mean(trace_water_all, axis=0)
sem_trace_water = np.std(trace_water_all, axis=0) / np.sqrt(len(trace_water_all))

mean_trace_tmt = np.mean(trace_tmt_all, axis=0)
sem_trace_tmt = np.std(trace_tmt_all, axis=0) / np.sqrt(len(trace_tmt_all))

mean_trace_water_early = np.mean(trace_water_early_all, axis=0)
sem_trace_water_early = np.std(trace_water_early_all, axis=0) / np.sqrt(len(trace_water_early_all))

mean_trace_tmt_early = np.mean(trace_tmt_early_all, axis=0)
sem_trace_tmt_early = np.std(trace_tmt_early_all, axis=0) / np.sqrt(len(trace_tmt_early_all))

mean_trace_water_inter = np.mean(trace_water_inter_all, axis=0)
sem_trace_water_inter = np.std(trace_water_inter_all, axis=0) / np.sqrt(len(trace_water_inter_all))

mean_trace_tmt_inter = np.mean(trace_tmt_inter_all, axis=0)
sem_trace_tmt_inter = np.std(trace_tmt_inter_all, axis=0) / np.sqrt(len(trace_tmt_inter_all))

mean_trace_water_late = np.mean(trace_water_late_all, axis=0)
sem_trace_water_late = np.std(trace_water_late_all, axis=0) / np.sqrt(len(trace_water_late_all))

mean_trace_tmt_late = np.mean(trace_tmt_late_all, axis=0)
sem_trace_tmt_late = np.std(trace_tmt_late_all, axis=0) / np.sqrt(len(trace_tmt_late_all))

