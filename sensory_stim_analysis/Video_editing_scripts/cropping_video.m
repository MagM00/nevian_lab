%% Preamble
%{
This script is used to crop a video based on a rectangle selected by the
user. The cropped video is saved in the same directory as the original
video.
%}

% % 1. Ask the user to provide a video path
[filename, pathname] = uigetfile({'*.mp4;*.avi;*.mkv;*.flv', 'Video Files (*.mp4, *.avi, *.mkv, *.flv)'; ...
                                  '*.*', 'All Files (*.*)'}, ...
                                  'Select a Video File');
if isequal(filename,0)
    disp('User selected Cancel');
    return;
end
videoPath = fullfile(pathname, filename);

do_green = 1;

% 2. Display the first frame of the video
videoObj = VideoReader(videoPath);
firstFrame = read(videoObj, 1);
% Make figure full screen
fig_select = figure('color', 'k','units','normalized','outerposition',[0 0 1 1]);
imshow(firstFrame);
title({'Select a rectangle to crop the video : make it as large as it can get, to avoid problems with camera displacement'}, 'color', 'w'  );

% 3. Use a rectangle tool to let the user select a region to crop
rect = round(getrect); % [xmin ymin width height]

% Check if valid rectangle
if rect(3) <= 0 || rect(4) <= 0
    disp('Invalid rectangle selected');
    return;
end

% create a mask to select only the animal housing by doing a polygon
% selection
% Let user draw a polygon
title({'select a polygon (point by point) of the box'}, 'color', 'w'  );
h = drawpolygon;
drawnMask = createMask(h);

close(fig_select);

% ask user for a prefix
prompt = {'Enter the animal_ID you just cropped; or left and right:'};
dlgtitle = 'Input';
dims = [1 75];
definput = {''};
answer = inputdlg(prompt,dlgtitle,dims,definput);
prefix = answer{1};

% Select where to save the cropped video
cropped_pathname = fullfile(pathname, 'cropped');
if ~exist(cropped_pathname, 'dir')
    mkdir(cropped_pathname);
end	

% 4. Crop the entire video based on the rectangle selected in the reference frame
if do_green
    outputVideoPath = fullfile(cropped_pathname, [ prefix '_' 'cropped_' filename]);
else
    outputVideoPath = fullfile(cropped_pathname, [ prefix '_' 'cropped_RGB_' filename]);
end
outputVideo = VideoWriter(outputVideoPath, 'MPEG-4'); % You can change format if needed
outputVideo.FrameRate = videoObj.FrameRate;
open(outputVideo);

% print in the command window a waiting message
disp(['Cropping video: ', filename, '...']);

% Init a wait bar
h = waitbar(0, 'Cropping video...');
% loop through all the frames of the video
while hasFrame(videoObj)
    currentFrame = readFrame(videoObj);
    % increase contrast
    currentFrame = imadjust(currentFrame, [0 0 0; 0.8 0.8 0.8], [0 0 0; 1 1 1]);
    if do_green
        % turn to green
        currentFrame(:, :, 1) = 0;
        currentFrame(:, :, 3) = 0;
    end
    % increase brightness
    currentFrame = imadjust(currentFrame, [0 0 0; 0.8 0.8 0.8], [0.2 0.2 0.2; 1 1 1]);
    
    % apply mask
    for c = 1:3 % Assuming 3 color channels (RGB)
        currentFrame(:,:,c) = currentFrame(:,:,c) .* uint8(drawnMask);
    end

    % crop
    croppedFrame = imcrop(currentFrame, rect);

    % fixed the axes and make them saquare
    croppedFrame = imresize(croppedFrame, [1080 1080]);
    % croppedFrame = imresize(croppedFrame, [1080 1920]);

    % update waitbar
    waitbar(videoObj.CurrentTime/videoObj.Duration, h);
   

    writeVideo(outputVideo, croppedFrame);
end
% close the video
close(outputVideo);

% close waitbar
close(h);


disp(['Cropped video saved as: ', outputVideoPath]);
