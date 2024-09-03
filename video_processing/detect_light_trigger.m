clear
clc
%%
warning('off')
videos_path = 'D:\data\'; % modify this path to where the original videos are
dir_vids = dir(videos_path);
names={dir_vids.name};
videos = names(endsWith(names, '.mp4'));

n_videos = length(videos);

% Set trimmed filepath
trimmed_path = 'trimmed_vids';
if ~exist(trimmed_path, 'dir'), mkdir(trimmed_path);end

%% loop
for iv = 1:n_videos
    this_vid = videos{iv};
    filename = fullfile(videos_path, this_vid);
    % Read video
    vid = VideoReader(filename);
    n_frames = vid.NumFrames;

    %% Select roi
    frame = read(vid, 1);
    imagesc(frame)
    h =  drawcircle(gca);
    % Wait for the user to double-click on the freehand
    wait(h);
    % Create a binary mask for the ROI
    binaryMask = h.createMask();
    % Initialize a variable to store the fluorescence values per frame
    %%
    disp(['Extracting from video'])
    w = waitbar(0, 'Processing frames...');

    intensity = zeros(n_frames,1);
    
    tic
    for iframe = 1:n_frames
        f = rgb2gray(read(vid,iframe ));
        intensity_roi = f(binaryMask);
        intensity(iframe) = median(intensity_roi);
        waitbar(iframe/n_frames, h); % Update status bar
    end
    
    toc
    
 
    % Use ginput to get the x and y coordinates of each peak
    x =zeros(2,1);    y =x;
    run_input = 1;
    
    % Make sure we have only 2 points
    while run_input
        % Plot the figure to select the first peak
        p = figure;
        plot(intensity);
        title({['Video : ', this_vid];'Select the peaks manually; press enter after zoom in and after selecting the frame'});
        
        % Allow zooming in to select precise peaks
        zoom on;
        waitfor(p,'CurrentCharacter',char(13)); % Press enter to exit zoom mode
        zoom off;
        [x(1),y(1)] = ginput;
        close(p)
        
         % Plot the figure to select the second peak
         p = figure;
         plot(intensity);
         title({['Video : ', this_vid],'Select the peaks manually; press enter after zoom in and after selecting the frame'});
         
        % Zoom in again to select the second peak
        zoom on;
        waitfor(gcf, 'CurrentCharacter', char(13)); % Press enter to exit zoom mode
        zoom off;
        [x(2),y(2)] = ginput;
        
        % Round the x coordinates to integers (assuming they correspond to frame numbers)
        x = floor(x);
        
        s= figure;
        plot(intensity), hold on
        scatter(x, intensity(x), 'filled');
        title('is it good?')
        waitfor(s)
        choice = questdlg('Are the selected points correct?', 'Confirmation', 'Yes', 'No', 'Yes');
        
        
        if length(x)~=2 || ismember({choice}, 'No')
            % reset
            x =zeros(2,1);    y =x;
            continue
        else
            run_input = false;
        end
    end

    close(p)
    
 
  
 
    % Create new video writer

    trimmed_video_filename = fullfile(trimmed_path, this_vid);
    newVid = VideoWriter(trimmed_video_filename, 'MPEG-4');
    newVid.FrameRate =vid.FrameRate;
    open(newVid);
    
    % Trim video to frames between x(1) and x(2)
    frames = x(1):x(2);
    
    % Write only the trimmed frames to new video
%     
%     for ii = frames
%         frame = read(v, ii);
%         writeVideo(newVid, frame);
%     end
    
    % Write only the trimmed frames to new video
    disp('Writing new video...')
    tic
    n_frames_new = length(frames);
    for ii = 1:n_frames_new
        frame = read(vid, frames(ii));
        writeVideo(newVid, frame);
        
        % Status bar
        if mod(ii, round(n_frames_new/10)) == 0 % Update status every 10%
            progress = ii/length(frames) * 100;
            fprintf('\r%0.2f%%', progress);
        end
    end
    disp('Finished creating the video for ')
    toc
    
    % Close video writer
    close(newVid);
    
end