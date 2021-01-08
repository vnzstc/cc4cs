
x = 1:1:20;
y = zeros(20, 5);
arLen = size(timePredictionFDT);

tpInd1 = 1;

%Ciclo time prediuction Func e DT
for i=1:arLen(1)
    y(i,1) = timePredictionFDT{i}{tpInd1}(1);
    y(i,2) = timePredictionFDT{i}{tpInd1}(2);
    y(i,3) = timePredictionFDT{i}{tpInd1}(3);
    y(i,4) = timePredictionFDT{i}{tpInd1}(4);
    y(i,5) = timePredictionFDT{i}{tpInd1}(5);
end

y(i+1,:) = timePrediction;


figure('Position', [100 100 400 400]);
%ah = axes('Units','Normalize','Position',[0.12 0.2 0.87 0.77]);
plot(x,y(:,1)','--*b',x,y(:,2)','-+g',x,y(:,3)','-ok',x,y(:,4),'-xr',x,y(:,5)','--om')
legend('BAT','BOT','FT','LR','SVM','Location','northeast','FontSize',8);
ylabel('Time [s]');
set(gca, 'YScale', 'log')
grid on
if tpInd1 == 1
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

xticklabels({tickArr{:,1},tickArr{:,2},tickArr{:,3},tickArr{:,4},tickArr{:,5},...
              tickArr{:,6},tickArr{:,7},tickArr{:,8},tickArr{:,9},tickArr{:,10},...
              tickArr{:,11},tickArr{:,12},tickArr{:,13},tickArr{:,14},tickArr{:,15},...
              tickArr{:,16},tickArr{:,17},tickArr{:,18},tickArr{:,19},tickArr{:,20}})                  

xtickangle(45)