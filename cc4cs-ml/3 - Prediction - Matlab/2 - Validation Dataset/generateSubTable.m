%% Initial Clean
clc

%% Parameters
TVal = atmega328pVal; %20
T = atmega328p;     %80

%% Function Slice
funcArray = unique(TVal.FUNCTION);
len = length(funcArray);
ValFuncCell = {};
FuncCell = {};

for i=1:len
    FuncCell{i} = removevars(T(T.FUNCTION==funcArray(i),:),[1,2,3,4,5,26]); % il 26 si mette solo per atmega
    ValFuncCell{i} = removevars(TVal(TVal.FUNCTION==funcArray(i),:),[1,2,3,4,5,26]); % il 26 si mette solo per atmega
end

%% DataType Slice
datatypeArray = unique(TVal.DATA_TYPE);
lend = length(datatypeArray);
ValDTCell = {};
DTCell = {};

for i=1:lend
    DTCell{i} = removevars(T(T.DATA_TYPE==datatypeArray(i),:),[1,2,3,4,5,26]); % il 26 si mette solo per atmega
    ValDTCell{i} = removevars(TVal(TVal.DATA_TYPE==datatypeArray(i),:),[1,2,3,4,5,26]); % il 26 si mette solo per atmega
end

TTrain = removevars(T,[1,2,3,4,5,26]); % il 26 si mette solo per atmega
TValTest = removevars(TVal,[1,2,3,4,5,26]); % il 26 si mette solo per atmega

%% Final Clean
clear i lend len
clc
