
%EVBAT EVBOT EVFT EVSVM EVLR prima componente RMSE ALL
%ErrFuncBat .... RMSE Function prima cella e prima componente del vettore
%nella cella
%ErrDataBat .... RMSE DataType
%ValidationRMSET RMSE Training

x = 1:1:21;
y = zeros(21, 5);
arLen = size(FuncCell);

%Scelata dell'errore da graficare 
errInd1 = 1; % 1 RMSE 2 RMSEP
errInd2 = 1;
indTrans = 1; % 0 non uso dataset transaction

%Cilco errore funzione
for i=1:arLen(2)
    y(i,1) = ErrFuncBAT{i}{errInd1}(errInd2);
    y(i,2) = ErrFuncBOT{i}{errInd1}(errInd2);
    y(i,3) = ErrFuncFT{i}{errInd1}(errInd2);
    y(i,4) = ErrFuncLM{i}{errInd1}(errInd2);
    y(i,5) = ErrFuncSVM{i}{errInd1}(errInd2);
end

%Cilco errore Tipo di Dato
j=1;
for i=arLen(2)+1:arLen(2)+lend
    y(i,1) = ErrDataBAT{j}{errInd1}(errInd2);
    y(i,2) = ErrDataBOT{j}{errInd1}(errInd2);
    y(i,3) = ErrDataFT{j}{errInd1}(errInd2);
    y(i,4) = ErrDataLM{j}{errInd1}(errInd2);
    y(i,5) = ErrDataSVM{j}{errInd1}(errInd2);
    j=j+1;
end

%Errore totale
if errInd1 == 1
    y(arLen(2)+lend+1,1) = EVBAT(errInd2);
    y(arLen(2)+lend+1,2) = EVBOT(errInd2);
    y(arLen(2)+lend+1,3) = EVFT(errInd2);
    y(arLen(2)+lend+1,4) = EVLR(errInd2);
    y(arLen(2)+lend+1,5) = EVSVM(errInd2);
else    
    y(arLen(2)+lend+1,1) = EVPBAT(errInd2);
    y(arLen(2)+lend+1,2) = EVPBOT(errInd2);
    y(arLen(2)+lend+1,3) = EVPFT(errInd2);
    y(arLen(2)+lend+1,4) = EVPLR(errInd2);
    y(arLen(2)+lend+1,5) = EVPSVM(errInd2);
end

%Errore training sui 5 modelli usati
if (errInd1 == 1) && (indTrans == 0)
    y(arLen(2)+lend+2,1) = validationRMSET(1);
    y(arLen(2)+lend+2,2) = validationRMSET(2);
    y(arLen(2)+lend+2,3) = validationRMSET(3);
    y(arLen(2)+lend+2,4) = validationRMSET(4);
    y(arLen(2)+lend+2,5) = validationRMSET(5);
end

figure('Position', [100 100 400 400]);
%ah = axes('Units','Normalize','Position',[0.12 0.2 0.87 0.77]);
plot(x,y(:,1)','--*b',x,y(:,2)','-+g',x,y(:,3)','-ok',x,y(:,4),'-xr',x,y(:,5)','--om')
legend('BAT','BOT','FT','LR','SVM','Location','northeast','FontSize',8);
ylabel('RMSE');
set(gca, 'YScale', 'log')
grid on
if errInd1 == 1
    xlim([0 22]);
else
    xlim([0 21]);
end
% ylim([0 100]);
xticks(1:1:21);
for j=1:length(funcArray)
    tickArr(j) = cellstr(funcArray(j,1));
end
tickArr{j+1} = string({'int8'});
tickArr{j+2} = string({'int16'});
tickArr{j+3} = string({'int32'});
tickArr{j+4} = string({'float'});
tickArr{j+5} = string({'All'});
tickArr{j+6} = string({'Train'});

if (errInd1 == 1) && (indTrans == 0)
    xticklabels({tickArr{:,1},tickArr{:,2},tickArr{:,3},tickArr{:,4},tickArr{:,5},...
                  tickArr{:,6},tickArr{:,7},tickArr{:,8},tickArr{:,9},tickArr{:,10},...
                  tickArr{:,11},tickArr{:,12},tickArr{:,13},tickArr{:,14},tickArr{:,15},...
                  tickArr{:,16},tickArr{:,17},tickArr{:,18},tickArr{:,19},tickArr{:,20},tickArr{:,21}})
elseif (indTrans == 0)
    xticklabels({tickArr{:,1},tickArr{:,2},tickArr{:,3},tickArr{:,4},tickArr{:,5},...
                  tickArr{:,6},tickArr{:,7},tickArr{:,8},tickArr{:,9},tickArr{:,10},...
                  tickArr{:,11},tickArr{:,12},tickArr{:,13},tickArr{:,14},tickArr{:,15},...
                  tickArr{:,16},tickArr{:,17},tickArr{:,18},tickArr{:,19},tickArr{:,20}})         
end          

xtickangle(45)