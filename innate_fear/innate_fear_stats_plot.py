# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 16:20:42 2023

@author: huang
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Function to calculate and plot
def calculate_and_plot(file1, file2, trial_type, color1='blue', color2='red'):
    # Define the index range
    start_index = int(14.5 * 130)
    end_index = int(15.5 * 130)

    # Loading the data
    data1 = np.load(file1)
    data2 = np.load(file2)

    # Calculating the mean along axis=1 for the specified index range
    mean_data1 = np.mean(data1[:, start_index:end_index], axis=1)
    mean_data2 = np.mean(data2[:, start_index:end_index], axis=1)

    # Performing a paired t-test
    t_stat, p_value = stats.ttest_rel(mean_data1, mean_data2)

    # Calculating the means and standard deviations
    mean1 = np.mean(mean_data1)
    mean2 = np.mean(mean_data2)
    sd1 = np.std(mean_data1)
    sd2 = np.std(mean_data2)

    # Converting means and SDs to percentages
    mean1_percent = mean1 * 100
    mean2_percent = mean2 * 100
    sd1_percent = sd1 * 100
    sd2_percent = sd2 * 100
    mean_data1_percent = mean_data1 * 100
    mean_data2_percent = mean_data2 * 100

    # Creating the plot with semi-transparent bars
    fig, ax = plt.subplots()

    # Adding the bars for the means with transparency
    ax.bar(0, mean1_percent, color=color1, alpha=0.3, label='Water')
    ax.bar(1, mean2_percent, color=color2, alpha=0.3, label='TMT')

    # Adding the error bars for the SD
    ax.errorbar(0, mean1_percent, yerr=sd1_percent, fmt='none', color='black')
    ax.errorbar(1, mean2_percent, yerr=sd2_percent, fmt='none', color='black')

    # Adding the individual observations
    for i in range(len(mean_data1)):
        ax.plot([0, 1], [mean_data1_percent[i], mean_data2_percent[i]], color='grey', alpha=0.5)
        ax.plot(0, mean_data1_percent[i], 'bo')
        ax.plot(1, mean_data2_percent[i], 'ro')

    # Adding the significance
    if p_value < 0.001:
        sig = '***'
    elif p_value < 0.01:
        sig = '**'
    elif p_value < 0.05:
        sig = '*'
    else:
        sig = 'n.s.'
    plt.text(0.5, 0.95, f'p={p_value:.3f} {sig}', transform=ax.transAxes, horizontalalignment='center', verticalalignment='center')

    # Formatting the plot
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Water', 'TMT'])
    ax.set_ylabel('ΔF/F₀ (%)')
    ax.set_title(f'Water vs TMT ({trial_type} trials, n = 8 mice)')

    # Adding the figure legends without the box
    legend = ax.legend(frameon=False)

    # Displaying the plot
    plt.show()

# Function to calculate and plot AUC
def calculate_and_plot_auc(file1, file2, trial_type, color1='blue', color2='red'):
    # Loading the data
    data1 = np.load(file1)
    data2 = np.load(file2)

    # Calculating the AUC along axis=1 for the entire trial duration
    auc_data1 = np.trapz(data1, axis=1)
    auc_data2 = np.trapz(data2, axis=1)

    # Performing a paired t-test
    t_stat, p_value = stats.ttest_rel(auc_data1, auc_data2)

    # Calculating the means and standard deviations
    mean1 = np.mean(auc_data1)
    mean2 = np.mean(auc_data2)
    sd1 = np.std(auc_data1)
    sd2 = np.std(auc_data2)

    # Converting means and SDs to percentages
    mean1_percent = mean1 * 100
    mean2_percent = mean2 * 100
    sd1_percent = sd1 * 100
    sd2_percent = sd2 * 100
    auc_data1_percent = auc_data1 * 100
    auc_data2_percent = auc_data2 * 100

    # Creating the plot with semi-transparent bars
    fig, ax = plt.subplots()

    # Adding the bars for the means with transparency
    ax.bar(0, mean1_percent, color=color1, alpha=0.3, label='Water')
    ax.bar(1, mean2_percent, color=color2, alpha=0.3, label='TMT')

    # Adding the error bars for the SD
    ax.errorbar(0, mean1_percent, yerr=sd1_percent, fmt='none', color='black')
    ax.errorbar(1, mean2_percent, yerr=sd2_percent, fmt='none', color='black')

    # Adding the individual observations
    for i in range(len(auc_data1)):
        ax.plot([0, 1], [auc_data1_percent[i], auc_data2_percent[i]], color='grey', alpha=0.5)
        ax.plot(0, auc_data1_percent[i], 'bo')
        ax.plot(1, auc_data2_percent[i], 'ro')

    # Adding the significance
    if p_value < 0.001:
        sig = '***'
    elif p_value < 0.01:
        sig = '**'
    elif p_value < 0.05:
        sig = '*'
    else:
        sig = 'n.s.'
    plt.text(0.5, 0.95, f'p={p_value:.3f} {sig}', transform=ax.transAxes, horizontalalignment='center', verticalalignment='center')

    # Formatting the plot
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Water', 'TMT'])
    ax.set_ylabel('AUC (%)')
    ax.set_title(f'Water vs TMT ({trial_type} trials, n = 8 mice)')

    # Adding the figure legends without the box
    legend = ax.legend(frameon=False)

    # Displaying the plot
    plt.show()

# Prepare the pairs of files and the trial type
file_pairs = [(('trace_water_all.npy', 'trace_tmt_all.npy'), 'All'), 
              (('trace_water_early_all.npy', 'trace_tmt_early_all.npy'), 'Early'),
              (('trace_water_inter_all.npy', 'trace_tmt_inter_all.npy'), 'Inter'),
              (('trace_water_late_all.npy', 'trace_tmt_late_all.npy'), 'Late'),]

# Calculate and plot for each pair of files
for file_pair, trial_type in file_pairs:
    calculate_and_plot(file_pair[0], file_pair[1], trial_type)

# Calculate and plot for each pair of files
for file_pair, trial_type in file_pairs:
    calculate_and_plot_auc(file_pair[0], file_pair[1], trial_type)