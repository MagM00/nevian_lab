
addpath('C:\Users\acuna\Documents\MATLAB\Examples\R2023b\deeplearning_shared\MulticlassObjectDetectionUsingDeepLearningExample')

pretrainedDetector = yolov2ObjectDetector("tiny-yolov2-coco");
inputSize = pretrainedDetector.Network.Layers(1).InputSize;
pretrainedNet = pretrainedDetector.Network;

preprocessedData = transform(ds,@(data)resizeImageAndLabel(data, inputSize));

% % Find the index of the feature layer
% featureLayer = 'yolov2ClassConv';
% featureLayerIndex = find(arrayfun(@(l) strcmp(l.Name, featureLayer), pretrainedNet.Layers), 1, 'first');

numAnchors = 5;
aboxes = estimateAnchorBoxes(preprocessedData, numAnchors);

numClasses = numel(classes);

% % Adjust the network architecture
featureLayer = "leaky_relu_5";

lgraph = yolov2Layers(inputSize, numClasses, aboxes, pretrainedNet, featureLayer);

% lgraph = layerGraph(pretrainedNet);
lgraph = removeLayers(lgraph, 'yolov2Transform');
lgraph = removeLayers(lgraph, 'yolov2OutputLayer');

classNames = {}; % TODO

%
% Add new layers
lgraph = addLayers(lgraph, [
    yolov2TransformLayer(numAnchors, 'Name', 'yolov2_transform')
    yolov2OutputLayer(aboxes, 'Name','yolov2_output')
]);

% Update the number of filters
numFilters = numAnchors * (5 + numClasses);
%convLayerIndex = ...; % Index of the convolutional layer before the transform layer

convLayer = lgraph.Layers(convLayerIndex);

newConvLayer = convolution2dLayer(convLayer.FilterSize, numFilters, 'Name', convLayer.Name, 'Weights', convLayer.Weights, 'Bias', convLayer.Bias);


% Connect new layers
lgraph = connectLayers(lgraph, 'yolov2ClassConv', 'yolov2_transform');
% lgraph = connectLayers(lgraph, 'yolov2_transform', 'yolov2_output');

% Continue with the rest of the code...

% Continue with your code for data preparation
rng(0);
preprocessedData = shuffle(preprocessedData);
trainingIdx = 1:4;
validationIdx = 3;
testIdx = 4;
dsTrain = subset(preprocessedData, trainingIdx);
dsVal = subset(preprocessedData, validationIdx);
dsTest = subset(preprocessedData, testIdx);

augmentedTrainingData = transform(dsTrain, @augmentData);
data = read(augmentedTrainingData);

% Displaying the data
I = data{1};
bbox = data{2};
label = data{3};
imshow(I);
showShape("rectangle", bbox, Label=label);

% Training options
opts = trainingOptions("rmsprop",...
        InitialLearnRate=0.001,...
        MiniBatchSize=8,...
        MaxEpochs=10,...
        LearnRateSchedule="piecewise",...
        LearnRateDropPeriod=5,...
        VerboseFrequency=30, ...
        L2Regularization=0.001,...
        ValidationData=dsVal, ...
        ValidationFrequency=50, ...
        OutputNetwork="best-validation-loss");

% Training the model
[detector, info] = trainYOLOv2ObjectDetector(augmentedTrainingData, lgraph, opts);
