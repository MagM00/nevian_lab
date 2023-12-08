# © Jun Huang 2023.12.07
import os

# Specify the directory path
base_path = r'E:\sensory_stim\behavior\control'

# Initialize lists to store subfolder names and paths of first videos
subfolder_names = []
first_video_paths = []

# Iterate through the subdirectories
for root, dirs, files in os.walk(base_path):
    for dir in dirs:
        if dir.startswith('JH'):
            subfolder_names.append(dir)
            video_files = [file for file in os.listdir(os.path.join(root, dir)) if file.endswith('.mp4')]
            if video_files:
                first_video_paths.append(os.path.join(root, dir, video_files[0]))

# Print the subfolder names and paths of the first videos
print("Subfolder names starting with 'JH':")
print(subfolder_names)
print("\nPaths of the first videos in respective subfolders:")
""" first_video_paths = [
    'E:\\sensory_stim\\behavior\\control\\JH516\\20231123_113730A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH517\\20231124_115727A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH518\\20231124_154228A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH519\\20231124_174231A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH520\\20231127_111256A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH521\\20231129_124117A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH522\\20231129_160123A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH524\\20231130_104939A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH525\\20231201_111009A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH615\\20231206_142738A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH617\\20231122_121504A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH618\\20231116_005815A.mp4',
    'E:\\sensory_stim\\behavior\\control\\JH627\\20231206_165439A.mp4'
] """

# .npy file analysis

import numpy as np
import os
import matplotlib.pyplot as plt

# Directory where the .npy files are located. Change if needed.
directory_path = '.'

# List all .npy files in the directory
all_files = [f for f in os.listdir(directory_path) if f.endswith('.npy')]

# Lists to store the offset_points[0] and onset_points[1] values
offset_points_values = []
onset_points_values = []

# Loop through all the .npy files
for file in all_files:
    # Load the data from the file
    led_gray = np.load(file)
    
    # Plot the data for inspection
    plt.figure(figsize=(10, 6))
    plt.plot(led_gray)
    filename_without_extension = os.path.splitext(file)[0]  # Remove .npy extension
    plt.title(f'LED Gray Data for {filename_without_extension}')
    plt.xlabel('Data Points')
    plt.ylabel('Intensity')
    plt.grid(True)
    plt.show()

    # Ask the user to set the threshold manually based on the plot
    threshold = float(input(f"Please set the threshold for {filename_without_extension} based on the plot (e.g., 170): "))
    
    # Process the data
    convert_start = 1
    convert_end = 1
    led_gray[:convert_start] = 0
    led_gray[-convert_end:] = 0
    data_bool = led_gray > threshold
    
    diff = np.diff(data_bool.astype(int))
    onset_points = np.where(diff == 1)[0] + 1
    offset_points = np.where(diff == -1)[0]
    
    # Append the desired values to their respective lists
    if len(offset_points) > 0:
        offset_points_values.append(offset_points[0])
    else:
        offset_points_values.append(None)
    
    if len(onset_points) > 1:
        onset_points_values.append(onset_points[1])
    else:
        onset_points_values.append(None)

    # Plot the boolean data
    plt.figure(figsize=(10, 6))
    plt.plot(data_bool * 100)
    plt.title(f'Boolean Data (Thresholded) for {filename_without_extension}')
    plt.xlabel('Data Points')
    plt.ylabel('On/Off')
    plt.grid(True)
    plt.show()

# Combine the two lists into an array and print
combined_array = np.array([offset_points_values, onset_points_values]).T

# Print the array as a table
print("Offset_Point[0] | Onset_Point[1]")
print("-" * 30)
for row in combined_array:
    print(f"{row[0]}           | {row[1]}")
