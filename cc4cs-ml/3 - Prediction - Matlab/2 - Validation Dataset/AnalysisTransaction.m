%% Variables
timeTrain = [0 0 0 0 0];
timePrediction = [0 0 0 0 0];

%% Parameters
len = length(funcArray);
lend = length(datatypeArray);
timePredictionFDT = cell(len+lend,3);

ErrFuncFT = cell(len,3);
ErrFuncLM = cell(len,3);
ErrFuncBOT = cell(len,3);
ErrFuncBAT = cell(len,3);
ErrFuncSVM = cell(len,3);

ErrDataFT = cell(lend,3);
ErrDataLM = cell(lend,3);
ErrDataBOT = cell(lend,3);
ErrDataBAT = cell(lend,3);
ErrDataSVM = cell(lend,3);

i = 1;
Te = TTransTest;
sizeT = size(TTransTest);

%% Fine Tree All
yReal = TTransTest.clockCycles;                                            % real values
tic
yfit = FineTreeModel.predictFcn(TTransTest);                               % predicted values
timePrediction(i) = toc/sizeT(1);

[EVFT, EVPFT, NRVFT] = errCalcFunc(yfit,yReal);
i = i+1;

%% Linear Regression All
yReal = TTransTest.clockCycles;                                            % real values
tic
yfit = LinearModel.predictFcn(TTransTest);                                 % predicted values
timePrediction(i) = toc/sizeT(1);

[EVLR, EVPLR, NRVLR] = errCalcFunc(yfit,yReal);
i = i+1;

%% Boosted Trees All
yReal = TTransTest.clockCycles;                                            % real values
tic
yfit = BoostedTreesModel.predictFcn(TTransTest);                           % predicted values
timePrediction(i) = toc/sizeT(1);

[EVBOT, EVPBOT, NRVBOT] = errCalcFunc(yfit,yReal);
i = i+1;

%% Bagged Trees All
yReal = TTransTest.clockCycles;                                            % real values
tic
yfit = BaggedTreesModel.predictFcn(TTransTest);                            % predicted values
timePrediction(i) = toc/sizeT(1);

[EVBAT, EVPBAT, NRVBAT] = errCalcFunc(yfit,yReal);
i = i+1;

% %% Linear SVM All
% yReal = TTransTest.clockCycles;                                            % real values
% tic
% yfit = SVMModel.predictFcn(TTransTest);                                    % predicted values
% timePrediction(i) = toc/sizeT(1);
% 
% [EVSVM, EVPSVM, NRVSVM] = errCalcFunc(yfit,yReal);

%% Function Cycle

for i=1:len
    %%% Cycle Parameters
    TValT = FuncCell{i};
    sizeT = size(TValT);
    predPar = [0 0 0 0 0];
    
    %%% Prediction
    yReal = TValT.clockCycles;                                             % real values
    tic
    yfitFT = FineTreeModel.predictFcn(TValT);                              % predicted values
    predPar(1) = toc/sizeT(1);
    tic
    yfitLM = LinearModel.predictFcn(TValT);
    predPar(2) = toc/sizeT(1);
    tic
    yfitBOT = BoostedTreesModel.predictFcn(TValT);
    predPar(3) = toc/sizeT(1);
    tic
    yfitBAT = BaggedTreesModel.predictFcn(TValT);
    predPar(4) = toc/sizeT(1);
%     tic
%     yfitSVM = SVMModel.predictFcn(TValT);
%     predPar(5) = toc/sizeT(1);
    
    %%%% Evaluate errors 
    [EVFTv, EVPFTv, NRVFTv] = errCalcFunc(yfitFT,yReal);
    [EVLMv, EVPLMv, NRVLMv] = errCalcFunc(yfitLM,yReal);
    [EVBOTv, EVPBOTv, NRVBOTv] = errCalcFunc(yfitBOT,yReal);
    [EVBATv, EVPBATv, NRVBATv] = errCalcFunc(yfitBAT,yReal);
%     [EVSVMv, EVPSVMv, NRVSVMv] = errCalcFunc(yfitSVM,yReal);
    
    timePredictionFDT{i} = {predPar};
    ErrFuncFT{i} = {EVFTv EVPFTv NRVFTv};
    ErrFuncLM{i} = {EVLMv EVPLMv NRVLMv};
    ErrFuncBOT{i} = {EVBOTv EVPBOTv NRVBOTv};
    ErrFuncBAT{i} = {EVBATv EVPBATv NRVBATv};
%     ErrFuncSVM{i} = {EVSVMv EVPSVMv NRVSVMv};
    
end

%% Data Type Cycle

for i=1:lend
    %%% Cycle Parameters
    TValT = DTCell{i};
    sizeT = size(TValT);
    predPar = [0 0 0 0 0];
    
    %%% Prediction
    yReal = TValT.clockCycles;                                             % real values
    tic
    yfitFT = FineTreeModel.predictFcn(TValT);                              % predicted values
    predPar(1) = toc/sizeT(1);
    tic
    yfitLM = LinearModel.predictFcn(TValT);
    predPar(2) = toc/sizeT(1);
    tic
    yfitBOT = BoostedTreesModel.predictFcn(TValT);
    predPar(3) = toc/sizeT(1);
    tic
    yfitBAT = BaggedTreesModel.predictFcn(TValT);
    predPar(4) = toc/sizeT(1);
%     tic
%     yfitSVM = SVMModel.predictFcn(TValT);
%     predPar(5) = toc/sizeT(1);
    
    %%%% Evaluate errors 
    [EVFTv, EVPFTv, NRVFTv] = errCalcFunc(yfitFT,yReal);
    [EVLMv, EVPLMv, NRVLMv] = errCalcFunc(yfitLM,yReal);
    [EVBOTv, EVPBOTv, NRVBOTv] = errCalcFunc(yfitBOT,yReal);
    [EVBATv, EVPBATv, NRVBATv] = errCalcFunc(yfitBAT,yReal);
%     [EVSVMv, EVPSVMv, NRVSVMv] = errCalcFunc(yfitSVM,yReal);
    
    timePredictionFDT{len + i} = {predPar};
    ErrDataFT{i} = {EVFTv EVPFTv NRVFTv};
    ErrDataLM{i} = {EVLMv EVPLMv NRVLMv};
    ErrDataBOT{i} = {EVBOTv EVPBOTv NRVBOTv};
    ErrDataBAT{i} = {EVBATv EVPBATv NRVBATv};
%     ErrDataSVM{i} = {EVSVMv EVPSVMv NRVSVMv};
    
end

%% Clean Variables
clear i len yReal yfitLM yfitBOT yfitBAT yfitSVM
clear EVFTv EVPFTv NRVFTv EVFLMv EVPLMv NRVLMv EVBOTv EVPBOTv NRVBOTv
clear EVBATv EVPBATv NRVBATv EVSVMv EVPSVMv NRVSVMv
clc
