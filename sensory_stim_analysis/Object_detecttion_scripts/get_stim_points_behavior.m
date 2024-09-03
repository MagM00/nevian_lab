% function step_04__behavior_video_trimming_to_trigger(~,~)
% function step_04__behavior_video_trimming_to_trigger(date,animal_ID)
clear
get_intensity_from = 'red_light';
% get_intensity_from = 'big_lamp';

clc
%%
overwrite = 0;
warning('off')

videos_path = uigetdir('','select where the videos are');
rootpath = fileparts(videos_path);

% rootpath = fullfile('H:\DANNCE\', date, animal_ID);
% videos_path = fullfile(rootpath,'full_length_videos/equalized');
dir_vids = dir(videos_path);
names={dir_vids.name};
videos = names(endsWith(names, '.mp4'));
n_videos = length(videos);

% getthe cvs files
csv_files = names(endsWith(names, '.csv'));
n_csvs = length(csv_files);

% Set trimmed filepath
trimmed_path =fullfile(rootpath, 'trimmed_vids');

if ~exist(trimmed_path, 'dir'), mkdir(trimmed_path);end

% check if the frames are already saved
x_filename = fullfile(videos_path, 'frames_to_trim.mat');
if ~exist(x_filename, "file")
    do_detection = 1;
else
    do_detection = 0;
end
if do_detection || overwrite
    %% Loop through Vids and locate triggers
    L = [];
    X=NaN(n_csvs,2);
    for iv = 1:n_csvs
        this_csv = csv_files{iv};
        filename = fullfile(videos_path, this_csv);
        % Read video
        fprintf('Loading intensity for %s \n', this_csv)
%         vid = VideoReader(filename);
        intensity = csvread(filename);

        der_intensity = diff(intensity);


        [~,ptsidx]= sort(der_intensity, 'descend');
        % keyboard
        % TODO:
        % check if it's off - on or on-off signal
        % for now we take off-on
        off_signals = sort(ptsidx(end-1:end), 'descend');
        first_off = off_signals(2);
        xs = sort(ptsidx(1:2), 'ascend');
        % when we use diff, we need to add one, beacuase of the moving
        % window (gradient does not work as well as diff)
        X(iv,1) = first_off(1) +1 +1;
        X(iv,2) = xs(2) +1;
        % n_to_go_back = n_points - find(derpt1>0, 1,'first');
        % x(iv,1) = determine_trigger_point(pt1, n_points, intensity);
        % x(iv,2) = determine_trigger_point(pt2, n_points, intensity);

        % End reading loop
        length_trimmed = X(iv,2) - X(iv,1) +1;
        fprintf('The legth of the video was %i \n', length_trimmed)
        L = [L;length_trimmed];
    end
    % save the x values to read them afterwards in case needed
    T = [array2table(X, VariableNames={'start', 'end'}), array2table(videos','VariableNames',{'cams'})];


    save(x_filename, 'T');
    disp('Frames to trim saved')

else
    keyboard % Check sintax
    T=load(x_filename, 'T');
    T = T.T;
end
% read frames and go on
n_frames_after_eq = T.end - T.start +1;

% Take the min value of frames
min_frames = min(n_frames_after_eq);



%% Read the ori videos and trimm them accordingly
for iv = 2:n_videos
    this_vid = videos{iv};
    % Create new video writer
    trimmed_video_filename = fullfile(trimmed_path, this_vid);
    newVid = VideoWriter(trimmed_video_filename, 'MPEG-4');
    newVid.Quality = 100;
    newVid.FrameRate = 120;%newVid.FrameRate;
    open(newVid);

    % read video
    filename = fullfile(videos_path, this_vid);
    vid = VideoReader(filename);

    % Trim video to frames between x(1) and x(2)
    this_frame = T.start(ismember(T.cams,this_vid));
    frames = [this_frame: ((this_frame + min_frames)-1)];



    % Write only the trimmed frames to new video
    fprintf('Writing new video for %s\n', this_vid)
    tic
    n_frames_new = length(frames);
    for ii = 1:n_frames_new
        frame = read(vid, frames(ii));
        writeVideo(newVid, frame);

        % Status bar
        if mod(ii, round(n_frames_new/10)) == 0 % Update status every 10%
            progress = ii/length(frames) * 100;
            fprintf('\r%0.0f %% \n', progress);
        end
    end
    fprintf('Finished creating the video for ')
    toc

    % Close video writer
    close(newVid);

end



