%% Preamble
% This script will perform video concatenation for all videos in the TRAP experiment.
% The videos_concatenation function will be called for each video in the
% experiment. The input and output paths will be formulated based on the
% folder structure of the experiment.

%% Start
% Clear the workspace
clear; close all; clc;

% toggle remove_raw_videos to true if you want to remove the raw videos
remove_raw_videos = false;

% Define the root folder
Videos_root_folder = '..\TRAP experiment\videos\anxiety cohort';

% Get a list of all experimental groups
exp_groups = dir(Videos_root_folder);
exp_groups = exp_groups([exp_groups.isdir] & ~strcmp({exp_groups.name},'.') & ~strcmp({exp_groups.name},'..'));

% Iterate through each experimental group
for e = 1:length(exp_groups)
    exp_group = exp_groups(e).name;
    
    % Get a list of all times of injection for the current experimental group
    injection_times = dir(fullfile(Videos_root_folder, exp_group));
    injection_times = injection_times([injection_times.isdir] & ~strcmp({injection_times.name},'.') & ~strcmp({injection_times.name},'..'));
    
    % Iterate through each time of injection
    for t = 1:length(injection_times)
        injection_time = injection_times(t).name;
        
        % Get a list of all animal IDs for the current time of injection
        animal_IDs = dir(fullfile(Videos_root_folder, exp_group, injection_time));
        animal_IDs = animal_IDs([animal_IDs.isdir] & ~strcmp({animal_IDs.name},'.') & ~strcmp({animal_IDs.name},'..'));
        
        % Iterate through each animal ID
        for a = 1:length(animal_IDs)
            animal_ID = animal_IDs(a).name;
            
            % Formulate the input and output paths
            % Get the videos inside the current animal ID folder
            % videos = dir(fullfile(Videos_root_folder, exp_group, injection_time, animal_ID, '*.mp4'));
            % Concatenate the videos' names with the path fullfile(Videos_root_folder, exp_group, injection_time, animal_ID)
            
            % Formulate the input and output paths
            input_path = fullfile(Videos_root_folder, exp_group, injection_time, animal_ID);
            output_path = fullfile(Videos_root_folder, exp_group, injection_time, [animal_ID '.mp4']);
            
            if exist(output_path, 'file') == 2
                disp(['Video ' output_path ' already exists. Skipping...']);
                continue;
            end
            % Call the videos_concatenation function
            videos_concatenation(input_path, output_path, remove_raw_videos);
        end
    end
end

disp('Video concatenation process completed.');
