%random order of stimuli
clc
n_animals = 6;

% stimuli = {'cold', 'heat', 'pinprick', '2g', '0.4g', '0.07g'};
stimuli = {'cold', 'heat', 'pinprick', '2g', '0.4g', '0.07g'};

n_stim = length(stimuli);
n_trials = 6;

for i_rep = 1:n_animals
    r= cell(n_trials,n_stim);
    for raw = 1:length(r)
        r(raw,:) = stimuli(randperm(n_stim));
    end
    disp(r)
end


% random group saline or CNO 
mouseIDs = [577, 580, 569, 567, 566, 568, 575, 548, 546, 551, 571, 573]; 

shuffledIDs = mouseIDs(randperm(length(mouseIDs)));

% Create group assignments
numMice = 12;
groupAssignment = cell(1, numMice);

% Assign the first 6 to "saline" and the remaining 6 to "CNO"
numSaline = 6;
groupAssignment(1:numSaline) = repmat({'saline'}, 1, numSaline);
groupAssignment(numSaline + 1:end) = repmat({'CNO'}, 1, numMice - numSaline);

% Display the group assignments
for i = 1:numMice
    fprintf('Mouse %d (ID %d) is in Group: %s\n', i, shuffledIDs(i), groupAssignment{i});
end

%%
% random group saline or CNO FEMALES
mouseIDs = [577, 580,567, 566,548, 546, 551]; 

shuffledIDs = mouseIDs(randperm(length(mouseIDs)));

% Create group assignments
numMice = 7;
groupAssignment = cell(1, numMice);

% Assign the first 6 to "saline" and the remaining 6 to "CNO"
numSaline = 3;
groupAssignment(1:numSaline) = repmat({'saline'}, 1, numSaline);
groupAssignment(numSaline + 1:end) = repmat({'CNO'}, 1, numMice - numSaline);

% Display the group assignments
for i = 1:numMice
    fprintf('Mouse %d (ID %d) is in Group: %s\n', i, shuffledIDs(i), groupAssignment{i});
end

% random group saline or CNO MALES  
mouseIDs = [569,568, 575,571, 573]; 

shuffledIDs = mouseIDs(randperm(length(mouseIDs)));

% Create group assignments
numMice = 5;
groupAssignment = cell(1, numMice);

% Assign the first 6 to "saline" and the remaining 6 to "CNO"
numSaline = 2;
groupAssignment(1:numSaline) = repmat({'saline'}, 1, numSaline);
groupAssignment(numSaline + 1:end) = repmat({'CNO'}, 1, numMice - numSaline);

% Display the group assignments
for i = 1:numMice
    fprintf('Mouse %d (ID %d) is in Group: %s\n', i, shuffledIDs(i), groupAssignment{i});
end
