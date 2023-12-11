%% Preamble
% This script will load cropped videos and then try to estimate when the stimulus comes
% based on the intensity of the frame
%% start
%
%  Ask user to load a video file
[filename, pathname] = uigetfile('*.mp4', 'Select a video file');
%  Load the video file
vid = VideoReader([pathname filename]);
%  Get the number of frames
nFrames = vid.NumberOfFrames;
%  Get the frame rate
frameRate = vid.FrameRate;
%  Get the duration of the video
duration = vid.Duration;
%  Get the height and width of the video
height = vid.Height;
width = vid.Width;
%  Get the number of channels
nChannels = vid.BitsPerPixel/8;

% Take first N frames to compute the background



%{
 % option 1: take the first N frames
N = 100; % Change based on your video
frames = zeros(height, width, N);

for k = 1:N
    frames(:, :, k) = rgb2gray(read(vid, k));
end
 
%}


% option 2: take a random sample of 1000 frames
N = 1000;
frames = zeros(height, width, N);
for k = 1:N
    frames(:, :, k) = rgb2gray(read(vid, randi([1 nFrames])));
end



background = median(frames, 3);
imshow(background);

threshold = 75; % Set a threshold for detecting changes
% figure
maxIntensity = zeros(nFrames,1);


% create waitbar
h = waitbar(0,'Please wait...');
% loop through frames
for i = 1:nFrames
    currentFrame = double(rgb2gray(read(vid, i))); % Replace with your actual image reading logic
    foregroundMask = abs(currentFrame - background) > threshold;
    
    % Post-processing to remove noise
    foregroundMask = imopen(foregroundMask, strel('disk', 3));
    foregroundMask = imclose(foregroundMask, strel('disk', 7));
    
    % Display or process the foreground mask as needed
    %imshow(foregroundMask);
    %title(num2str(i))
    maxIntensity(i) = max(max(foregroundMask));
    %update waitbar
    waitbar(i/nFrames,h,sprintf('%d of %d frames',i,nFrames));

end
close(h)

% convert x axis to time
x = linspace(0,duration,nFrames);

figure, plot(x,maxIntensity)
title(filename, 'Interpreter', 'none')
xlabel('Time (s)')
ylabel('probability of stimulus')

% detect frames >1
stimulusFrames = find(maxIntensity>0);
% convert stimulusFrames to time
stimulusTime = x(stimulusFrames);

save([pathname filename(1:end-4) '_stimulusFrames.mat'],'stimulusFrames', 'maxIntensity', 'stimulusTime')







%{
 
% Loop throught the frames and calculate the max intensity
maxIntensity = zeros(nFrames,3);
meanIntensity = zeros(nFrames,3);
maxIntensity_gray = zeros(nFrames,1);

% create waitbar
h = waitbar(0,'Please wait...');
% loop through frames
for i = 1:nFrames
    %  Read the frame
    frame = read(vid,i);
    %  Calculate the mean intensity
    meanIntensity(i,1) = mean(mean(frame(500:1000,500:1000,1)));
    meanIntensity(i,2) = mean(mean(frame(500:1000,500:1000,2)));
    meanIntensity(i,3) = mean(mean(frame(500:1000,500:1000,3)));
    % calculate the max intensity
    maxIntensity(i,1) = max(max(frame(500:1000,500:1000,1)));
    maxIntensity(i,2) = max(max(frame(500:1000,500:1000,2)));
    maxIntensity(i,3) = max(max(frame(500:1000,500:1000,3)));
    %convert to grayscale
    frame_gray = rgb2gray(frame);
    %  Calculate the max intensity
    maxIntensity_gray(i) = max(max(frame_gray));

    %update waitbar
    waitbar(i/nFrames,h,sprintf('%d of %d frames',i,nFrames));

end 
% close waitbar
close(h)
 
%}


