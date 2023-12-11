
%Create a VideoReader object for the input video
root_path  = 'C:\Users\acuna\OneDrive - Universitaet Bern\Coding_playground\Anna_playground\';
input_video_filename = fullfile(root_path,'videos','cropped', 'left_cropped_RGB_577_580.mp4');
output_video_filename = fullfile(root_path,'videos', 'cropped','left_cropped_RGB_577_580_less_highlight.mp4');
video = VideoReader(input_video_filename);

% Create a VideoWriter object to write the output video
outputVideo = VideoWriter(output_video_filename);

% Open the output video for writing
open(outputVideo);

% display waitbar
h = waitbar(0,'Please wait...');

% Loop through each frame of the input video
while hasFrame(video)
    % Read the current frame
    frame = readFrame(video);
    
    % Decrease the highlight to 75%
    frame = frame * 0.65;
    
    % Write the modified frame to the output video
    writeVideo(outputVideo, frame);
    % update waitbar
    waitbar(video.CurrentTime/video.Duration,h)
end

% Close the output video
close(outputVideo);
close(h)
disp('done')
