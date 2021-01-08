x = 1:1:3;
y = zeros(3, 5);

y(1,1) = timeTrain8051(1);
y(1,2) = timeTrain8051(2);
y(1,3) = timeTrain8051(3);
y(1,4) = timeTrain8051(4);
y(1,5) = timeTrain8051(5);

y(2,1) = timeTrainAtmega(1);
y(2,2) = timeTrainAtmega(2);
y(2,3) = timeTrainAtmega(3);
y(2,4) = timeTrainAtmega(4);
y(2,5) = timeTrainAtmega(5);

y(3,1) = timeTrainLeon3(1);
y(3,2) = timeTrainLeon3(2);
y(3,3) = timeTrainLeon3(3);
y(3,4) = timeTrainLeon3(4);
y(3,5) = timeTrainLeon3(5);

figure('Position', [100 100 400 400]);
%ah = axes('Units','Normalize','Position',[0.12 0.2 0.87 0.77]);
plot(x,y(:,1)','--*b',x,y(:,2)','-+g',x,y(:,3)','-ok',x,y(:,4),'-xr',x,y(:,5)','--om')
legend('BAT','BOT','FT','LR','SVM','Location','northeast','FontSize',8);
ylabel('Time [s]');
set(gca, 'YScale', 'log')
grid on

xlim([0 4]);
xticks(1:1:3);
xticklabels({'8051','Atmega328p','Leon3'})                  

xtickangle(45)