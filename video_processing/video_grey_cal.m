% Read video
vid = VideoReader('D:\data\cam1.mp4');
n_frames = vid.NumFrames;

%% Select roi
frame = read(vid, 1);
figure
imagesc(frame)
roi = drawrectangle();
pos = roi.Position;
%%
clc
warning('off')
ic =0;
intensity = [];
for iframe = 1:n_frames
    f = read(vid,ic+1);
    f = rgb2gray(f);
    intensity(ic+1) = mean(f(pos(1):pos(2)));
    ic = ic+1;
end

%%
figure
plot(intensity)