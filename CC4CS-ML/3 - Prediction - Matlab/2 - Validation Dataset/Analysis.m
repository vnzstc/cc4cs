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

%% Function Cycle

for i=1:len
    %%% Cycle Parameters
    TValT = ValFuncCell{i};
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
    TValT = ValDTCell{i};
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
