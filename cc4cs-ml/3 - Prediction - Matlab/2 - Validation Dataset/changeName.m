T_an = nBatmega328p;
modelTab = removevars(atmega328p,{'assemblyInstr'});
Trn = removevars(T_an,{'If' 'SyntacticallyReachableFunctions'...
    'SemanticallyReachedFunctions' 'CC4CS' 'CoverageEstimation'...
    'CyclomaticComplexity' 'PointerDereferencing' 'FunctionCall' 'Function'...
    'ExitPoint' 'Loop' 'DecisionPoint' 'TotalOperators' 'ProgramVolume'...
    'ProgramLength' 'assemblyInstr'});

%nT = Trn.Properties.VariableNames;
%nTOld = leon3.Properties.VariableNames;

vecLen = size(Trn);
len = vecLen(1);

Trn.Properties.VariableNames = {'DEVICE' 'FUNCTION' 'DATA_TYPE'...    
    'DIFFICULTY_LEVEL' 'DISTINCT_OPERANDS'...
    'DSTINCT_OPERATORS' 'EFFORT' 'PROGRAM_LEVEL' 'TOTAL_OPERANDS'... 
    'VOCABULARY_SIZE' 'SLOC' 'GLOBALVARIABLES' 'GOTO' 'ASSIGNMENT'...    
    'SCALAR_INPUT' 'RANGE_SCALAR_VALUES'...   
    'SCALAR_INDEX_INPUT' 'RANGE_SCALAR_INDEX_VALUES'...    
    'ARRAY_INPUT' 'RANGE_ARRAY_INPUT'... 
    'ExecutedCInstr'...
    'clockCycles'};

    %'assemblyInstr'... per atmega si elimina!!!!

tImp = Trn{:,'EFFORT'}./18;
bugsD = ((Trn{:,'EFFORT'}).^(2/3))./3000;

Trn.FILE_CSV = modelTab.FILE_CSV(1:len);
Trn.PATH = modelTab.PATH(1:len);
Trn.TIME_TO_IMPLEMENT = tImp;
Trn.BUGS_DELIVERED = bugsD;

Trn.SCALAR_INPUT = zeros(len, 1);
Trn.RANGE_SCALAR_VALUES = zeros(len, 1);
Trn.SCALAR_INDEX_INPUT = zeros(len, 1);
Trn.RANGE_SCALAR_INDEX_VALUES = zeros(len, 1);
Trn.ARRAY_INPUT = zeros(len, 1);
Trn.RANGE_ARRAY_INPUT = zeros(len, 1);

[~, newOrder] = ismember(modelTab.Properties.VariableNames,Trn.Properties.VariableNames);
TrnN = Trn(:,newOrder);

TrnNp = rmmissing(TrnN);