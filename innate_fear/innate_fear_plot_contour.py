import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import glob
import os

# Get all .npy files that match the pattern 'trace_tmt_XXX.npy'
tmt_files = sorted(glob.glob('trace_tmt_*.npy'))

for tmt_file in tmt_files:
    # Load the .npy files
    trace_tmt = np.load(tmt_file)
    
    # Assume that for every 'trace_tmt_XXX.npy' file there is a 'trace_water_XXX.npy' file
    trace_water = np.load(tmt_file.replace('tmt', 'water'))

    # Create the time axis
    total_time = trace_tmt.shape[1] / 130  # number of points divided by the sampling rate
    time = np.linspace(-10, total_time - 10, trace_tmt.shape[1])  # start, stop, num

    # Plot 3D contour for trace_tmt_XXX.npy and save as .png
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    Y, X = np.meshgrid(time, range(trace_tmt.shape[0]))
    surf = ax.plot_surface(X, Y, trace_tmt, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel('Series Index')
    ax.set_ylabel('Time (s)')
    ax.set_zlabel('Data Value')
    ax.set_title('3D Contour plot for ' + tmt_file)
    plt.savefig(os.path.splitext(tmt_file)[0] + '.png')
    plt.close()

    # Plot 3D contour for trace_water_XXX.npy and save as .png
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    Y, X = np.meshgrid(time, range(trace_water.shape[0]))
    surf = ax.plot_surface(X, Y, trace_water, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel('Series Index')
    ax.set_ylabel('Time (s)')
    ax.set_zlabel('Data Value')
    ax.set_title('3D Contour plot for ' + tmt_file.replace('tmt', 'water'))
    plt.savefig(os.path.splitext(tmt_file.replace('tmt', 'water'))[0] + '.png')
    plt.close()
