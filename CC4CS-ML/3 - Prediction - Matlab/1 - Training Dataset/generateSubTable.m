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

%pnew= removevars(p,[1,2,3,4,5]);

for i=1:len
%     FuncCell{i} = removevars(T(T.FUNCTION==funcArray(i),:),[1,2,3,4,5]);
%     ValFuncCell{i} = removevars(TVal(TVal.FUNCTION==funcArray(i),:),[1,2,3,4,5]);
    FuncCell{i} = T(T.FUNCTION==funcArray(i),:);
    ValFuncCell{i} = TVal(TVal.FUNCTION==funcArray(i),:);
end

%% DataType Slice
datatypeArray = unique(TVal.DATA_TYPE);
lend = length(datatypeArray);
ValDTCell = {};
DTCell = {};

for i=1:lend
%     DTCell{i} = removevars(T(T.DATA_TYPE==datatypeArray(i),:),[1,2,3,4,5]);
%     ValDTCell{i} = removevars(TVal(TVal.DATA_TYPE==datatypeArray(i),:),[1,2,3,4,5]);
    DTCell{i} = T(T.DATA_TYPE==datatypeArray(i),:);
    ValDTCell{i} = TVal(TVal.DATA_TYPE==datatypeArray(i),:);
end

%TTrain = removevars(T,[1,2,3,4,5]);
%TValTest = removevars(TVal,[1,2,3,4,5]);

TTrain = T;
TValTest = TVal;

%% Final Clean
clear i lend len
clc
