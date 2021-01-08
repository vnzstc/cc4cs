function [trainedModel, validationRMSE] = BoostedTreesRegressionModel(trainingData)
% [trainedModel, validationRMSE] = trainRegressionModel(trainingData)
% returns a trained regression model and its RMSE. This code recreates the
% model trained in Regression Learner app. Use the generated code to
% automate training the same model with new data, or to learn how to
% programmatically train models.
%
%  Input:
%      trainingData: a table containing the same predictor and response
%       columns as imported into the app.
%
%  Output:
%      trainedModel: a struct containing the trained regression model. The
%       struct contains various fields with information about the trained
%       model.
%
%      trainedModel.predictFcn: a function to make predictions on new data.
%
%      validationRMSE: a double containing the RMSE. In the app, the
%       History list displays the RMSE for each model.
%
% Use the code to train the model with new data. To retrain your model,
% call the function from the command line with your original data or new
% data as the input argument trainingData.
%
% For example, to retrain a regression model trained with the original data
% set T, enter:
%   [trainedModel, validationRMSE] = trainRegressionModel(T)
%
% To make predictions with the returned 'trainedModel' on new data T2, use
%   yfit = trainedModel.predictFcn(T2)
%
% T2 must be a table containing at least the same predictor columns as used
% during training. For details, enter:
%   trainedModel.HowToPredict

% Auto-generated by MATLAB on 19-Oct-2020 01:37:28


% Extract predictors and response
% This code processes the data into the right shape for training the
% model.
inputTable = trainingData;
predictorNames = {'SLOC', 'SCALAR_INPUT', 'RANGE_SCALAR_VALUES', 'SCALAR_INDEX_INPUT', 'RANGE_SCALAR_INDEX_VALUES', 'ARRAY_INPUT', 'RANGE_ARRAY_INPUT', 'DSTINCT_OPERATORS', 'TOTAL_OPERANDS', 'DISTINCT_OPERANDS', 'VOCABULARY_SIZE', 'EFFORT', 'BUGS_DELIVERED', 'TIME_TO_IMPLEMENT', 'DIFFICULTY_LEVEL', 'PROGRAM_LEVEL', 'GLOBALVARIABLES', 'GOTO', 'ASSIGNMENT', 'ExecutedCInstr', 'assemblyInstr'};
predictors = inputTable(:, predictorNames);
response = inputTable.clockCycles;
isCategoricalPredictor = [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false];

% Train a regression model
% This code specifies all the model options and trains the model.
template = templateTree(...
    'MinLeafSize', 8);
regressionEnsemble = fitrensemble(...
    predictors, ...
    response, ...
    'Method', 'LSBoost', ...
    'NumLearningCycles', 30, ...
    'Learners', template, ...
    'LearnRate', 0.1);

% Create the result struct with predict function
predictorExtractionFcn = @(t) t(:, predictorNames);
ensemblePredictFcn = @(x) predict(regressionEnsemble, x);
trainedModel.predictFcn = @(x) ensemblePredictFcn(predictorExtractionFcn(x));

% Add additional fields to the result struct
trainedModel.RequiredVariables = {'ARRAY_INPUT', 'ASSIGNMENT', 'BUGS_DELIVERED', 'DIFFICULTY_LEVEL', 'DISTINCT_OPERANDS', 'DSTINCT_OPERATORS', 'EFFORT', 'ExecutedCInstr', 'GLOBALVARIABLES', 'GOTO', 'PROGRAM_LEVEL', 'RANGE_ARRAY_INPUT', 'RANGE_SCALAR_INDEX_VALUES', 'RANGE_SCALAR_VALUES', 'SCALAR_INDEX_INPUT', 'SCALAR_INPUT', 'SLOC', 'TIME_TO_IMPLEMENT', 'TOTAL_OPERANDS', 'VOCABULARY_SIZE', 'assemblyInstr'};
trainedModel.RegressionEnsemble = regressionEnsemble;
trainedModel.About = 'This struct is a trained model exported from Regression Learner R2019a.';
trainedModel.HowToPredict = sprintf('To make predictions on a new table, T, use: \n  yfit = c.predictFcn(T) \nreplacing ''c'' with the name of the variable that is this struct, e.g. ''trainedModel''. \n \nThe table, T, must contain the variables returned by: \n  c.RequiredVariables \nVariable formats (e.g. matrix/vector, datatype) must match the original training data. \nAdditional variables are ignored. \n \nFor more information, see <a href="matlab:helpview(fullfile(docroot, ''stats'', ''stats.map''), ''appregression_exportmodeltoworkspace'')">How to predict using an exported model</a>.');

% Extract predictors and response
% This code processes the data into the right shape for training the
% model.
inputTable = trainingData;
predictorNames = {'SLOC', 'SCALAR_INPUT', 'RANGE_SCALAR_VALUES', 'SCALAR_INDEX_INPUT', 'RANGE_SCALAR_INDEX_VALUES', 'ARRAY_INPUT', 'RANGE_ARRAY_INPUT', 'DSTINCT_OPERATORS', 'TOTAL_OPERANDS', 'DISTINCT_OPERANDS', 'VOCABULARY_SIZE', 'EFFORT', 'BUGS_DELIVERED', 'TIME_TO_IMPLEMENT', 'DIFFICULTY_LEVEL', 'PROGRAM_LEVEL', 'GLOBALVARIABLES', 'GOTO', 'ASSIGNMENT', 'ExecutedCInstr', 'assemblyInstr'};
predictors = inputTable(:, predictorNames);
response = inputTable.clockCycles;
isCategoricalPredictor = [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false];

% Perform cross-validation
partitionedModel = crossval(trainedModel.RegressionEnsemble, 'KFold', 5);

% Compute validation predictions
validationPredictions = kfoldPredict(partitionedModel);

% Compute validation RMSE
validationRMSE = sqrt(kfoldLoss(partitionedModel, 'LossFun', 'mse'));
