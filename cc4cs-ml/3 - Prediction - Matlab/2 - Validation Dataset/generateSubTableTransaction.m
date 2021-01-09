%% Initial Clean
clc

%% Parameters
T = TrnNp;     %100

%% Function Slice
funcArray = unique(T.FUNCTION);
len = length(funcArray);
FuncCell = {};

for i=1:len
    FuncCell{i} = removevars(T(T.FUNCTION==funcArray(i),:),[1,2,3,4,5]);
end

%% DataType Slice
datatypeArray = unique(T.DATA_TYPE);
lend = length(datatypeArray);
DTCell = {};

for i=1:lend
    DTCell{i} = removevars(T(T.DATA_TYPE==datatypeArray(i),:),[1,2,3,4,5]);
end

TTransTest = removevars(T,[1,2,3,4,5]);

%% Final Clean
clear i lend len
clc
