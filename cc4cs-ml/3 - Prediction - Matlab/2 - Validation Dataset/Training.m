%% Variables
timeTrain = [0 0 0 0 0];
timePrediction = [0 0 0 0 0];
validationRMSET = [0 0 0 0 0];

%% Parameters
i = 1;
Te = TTrain;
sizeT = size(TValTest);

%% Fine Tree
tic
[FineTreeModel, validationRMSET(i)] = FineTreeRegressionModel(Te);
timeTrain(i) = toc;

yReal = TValTest.clockCycles;                                              % real values
tic
yfit = FineTreeModel.predictFcn(TValTest);                                 % predicted values
timePrediction(i) = toc/sizeT(1);

[EVFT, EVPFT, NRVFT] = errCalcFunc(yfit,yReal);
i = i+1;

%% Linear Regression
tic
[LinearModel, validationRMSET(i)] = LinearRegressionModel(Te);
timeTrain(i) = toc;

yReal = TValTest.clockCycles;                                              % real values
tic
yfit = LinearModel.predictFcn(TValTest);                                   % predicted values
timePrediction(i) = toc/sizeT(1);

[EVLR, EVPLR, NRVLR] = errCalcFunc(yfit,yReal);
i = i+1;

%% Boosted Trees
tic
[BoostedTreesModel, validationRMSET(i)] = BoostedTreesRegressionModel(Te);
timeTrain(i) = toc;

yReal = TValTest.clockCycles;                                              % real values
tic
yfit = BoostedTreesModel.predictFcn(TValTest);                             % predicted values
timePrediction(i) = toc/sizeT(1);

[EVBOT, EVPBOT, NRVBOT] = errCalcFunc(yfit,yReal);
i = i+1;

%% Bagged Trees
tic
[BaggedTreesModel, validationRMSET(i)] = BaggedTreesRegressionModel(Te);
timeTrain(i) = toc;

yReal = TValTest.clockCycles;                                              % real values
tic
yfit = BaggedTreesModel.predictFcn(TValTest);                              % predicted values
timePrediction(i) = toc/sizeT(1);

[EVBAT, EVPBAT, NRVBAT] = errCalcFunc(yfit,yReal);
i = i+1;

% %% Linear SVM
% tic
% [SVMModel, validationRMSET(i)] = SVMRegressionModel(Te);
% timeTrain(i) = toc;
% 
% yReal = TValTest.clockCycles;                                              % real values
% tic
% yfit = SVMModel.predictFcn(TValTest);                                      % predicted values
% timePrediction(i) = toc/sizeT(1);
% 
% [EVSVM, EVPSVM, NRVSVM] = errCalcFunc(yfit,yReal);

%% Clean Variables
clear i yReal yfit
clc

