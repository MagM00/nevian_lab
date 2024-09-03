clc
clear
GC = general_configs();
%% set the version
version = '3';
rootpath = GC.repo_path; 
% if ispc
%     root_path = 'C:\Users\acuna\OneDrive - Universitaet Bern\Coding_playground\Anna_playground\';
% else
%     keyboard
% end

addpath(genpath('Object_detection_scripts\utilities'))

% load data
root_path_data = GC.temp_data_path;
gTruth_file =['gTruth', num2str(version), '.mat'];
gTruth = load(fullfile(root_path_data, gTruth_file));
gTruth = gTruth.gTruth;

% get the training data
training_folder = fullfile(root_path_data, 'training', ['v',num2str(version)]);
if ~exist(training_folder, 'dir')
    mkdir(training_folder)
end
[imds,bxds] = objectDetectorTrainingData(gTruth, 'WriteLocation', ['C:\Users\acuna\OneDrive - Universitaet Bern\Coding_playground\Anna_playground\training\v',num2str(version)]);%Combine the datastores.
ds = combine(imds,bxds);





%% set parameter network

pretrainedDetector = yolov2ObjectDetector("tiny-yolov2-coco"); % 'darknet19-coco'
% inputSize = pretrainedDetector.Network.Layers(1).InputSize;
inputSize = [720 720 3]; % check this
preprocessedData = transform(ds,@(data)resizeImageAndLabel(data, inputSize));

% preview data
data = preview(preprocessedData);
I = data{1};
bbox = data{2};
label = data{3};
imshow(I)
showShape("rectangle", bbox, Label=label)

% get the layers
featureLayer = "leaky_relu_5";

numAnchors = 9;
aboxes = estimateAnchorBoxes(preprocessedData, numAnchors);

% get the classes
ls = bxds.LabelData(:,2);
catArray = vertcat(ls{:});
class_labels = unique(catArray);


numClasses = length(class_labels);

% Network
pretrainedNet = pretrainedDetector.Network;
lgraph = yolov2Layers(inputSize, numClasses, aboxes, pretrainedNet, featureLayer);

% shuffle data for training
rng(0);
preprocessedData = shuffle(preprocessedData);

totalSamples = numel(imds.Files); % Replace with appropriate method if needed

% Define your split percentages (e.g., 70% training, 15% validation, 15% testing)
trainingSplit = 0.80;
validationSplit = 0.20;
% Test split will be the remaining percentage

% Calculate the number of samples for each subset; check if test is needed
numTrainingSamples = round(totalSamples * trainingSplit);
numValidationSamples = round(totalSamples * validationSplit);
% numTestingSamples = totalSamples - numTrainingSamples - numValidationSamples;

% Generate random indices for each subset
indices = randperm(totalSamples);
training_idx = indices(1:numTrainingSamples);
val_idx = indices(numTrainingSamples+1 : numTrainingSamples+numValidationSamples);
% test_idx = indices(numTrainingSamples+numValidationSamples+1 : end);

% Now you can create subsets
dsTrain = subset(preprocessedData, training_idx);
dsVal = subset(preprocessedData, val_idx);
% dsTest = subset(preprocessedData, test_idx);

% Augment the data
augmentedTrainingData = transform(dsTrain, @augmentData);
data = read(augmentedTrainingData);
I = data{1};
bbox = data{2};
label = data{3};
imshow(I)
showShape("rectangle", bbox, Label=label)

% Set parameters for Training
opts = trainingOptions("rmsprop",...
        InitialLearnRate=0.001,...
        MiniBatchSize=4,...
        MaxEpochs=100,...
        LearnRateSchedule="none",... %'piecewise'
        LearnRateDropPeriod=5,...
        VerboseFrequency=30, ...
        L2Regularization=0.001,...
        ValidationData=dsVal, ...
        ValidationFrequency=50, ...
        ExecutionEnvironment= 'gpu',...
        Plots='training-progress',...
        OutputNetwork="best-validation-loss");


% Train detector
[detector, info] = trainYOLOv2ObjectDetector(augmentedTrainingData,lgraph, opts);



% save detector
detector_filename = ['detector_v', (version), '.mat'];
detector_path = fullfile(root_path_data, 'detectors');
if ~exist(detector_path, 'dir')
    mkdir(detector_path)
end
save(fullfile(detector_path, detector_filename), 'detector', ')

% % get the results from test samples
% detectionThreshold = 0.01;
% results = detect(detector,dsTest, MiniBatchSize=8, Threshold=detectionThreshold);
% iouThresholds = [0.5 0.75 0.9];
% metrics = evaluateObjectDetection(results, dsTest, iouThresholds);
% metrics.ClassMetrics 
% 
% % visualize it
% figure
% classAP = metrics.ClassMetrics{:,"AP"}';
% classAP = [classAP{:}];
% bar(classAP')
% xticklabels(metrics.ClassNames)
% ylabel("AP")
% legend(string(iouThresholds) + " IoU")



%% helper fuctions
function B = augmentData(A)
addpath('C:\Users\acuna\Documents\MATLAB\Examples\R2023b\deeplearning_shared\MulticlassObjectDetectionUsingDeepLearningExample')

% Apply random horizontal flipping, and random X/Y scaling. Boxes that get
% scaled outside the bounds are clipped if the overlap is above 0.25. Also,
% jitter image color.
B = cell(size(A));

I = A{1};
sz = size(I);
if numel(sz)==3 && sz(3) == 3
    I = jitterColorHSV(I,...
        Contrast=0.2,...
        Hue=0,...
        Saturation=0.1,...
        Brightness=0.2);
end

% % Add randomized Gaussian blur
% I = imgaussfilt(I,1.5*rand);
% 
% % Add salt and pepper noise
% I = imnoise(I,"salt & pepper");

% Randomly flip and scale image.
tform = randomAffine2d(XReflection=true, Scale=[0.95 1.1]);
rout = affineOutputView(sz, tform, BoundsStyle="CenterOutput");
B{1} = imwarp(I, tform, OutputView=rout);

% Sanitize boxes, if needed. This helper function is attached as a
% supporting file. Open the example in MATLAB to open this function.
A{2} = helperSanitizeBoxes(A{2});

% Apply same transform to boxes.
[B{2},indices] = bboxwarp(A{2}, tform, rout, OverlapThreshold=0.25);
B{3} = A{3}(indices);

% Return original data only when all boxes are removed by warping.
if isempty(indices)
    B = A;
end
end


function data = resizeImageAndLabel(data,targetSize)
% Resize the images and scale the corresponding bounding boxes.

    scale = (targetSize(1:2))./size(data{1},[1 2]);
    data{1} = imresize(data{1},targetSize(1:2));
    data{2} = bboxresize(data{2},scale);

    data{2} = floor(data{2});
    imageSize = targetSize(1:2);
    boxes = data{2};
    % Set boxes with negative values to have value 1.
    boxes(boxes<=0) = 1;
    
    % Validate if bounding box in within image boundary.
    boxes(:,3) = min(boxes(:,3),imageSize(2) - boxes(:,1)-1);
    boxes(:,4) = min(boxes(:,4),imageSize(1) - boxes(:,2)-1);
    
    data{2} = boxes; 

end