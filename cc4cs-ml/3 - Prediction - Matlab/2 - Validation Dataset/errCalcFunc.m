function [EV, EVP, NRV] = errCalcFunc(yfit,yReal)

    isNotMissing = ~isnan(yfit) & ~isnan(yReal);

    MAE = nansum(abs(( yfit - yReal ))) / numel(yReal(isNotMissing) );
    MSE = nansum(( yfit - yReal ).^2) / numel(yReal(isNotMissing) );
    RMSE = sqrt(nansum(( yfit - yReal ).^2) / numel(yReal(isNotMissing) ));

    NRMSEAve = RMSE /( nanmean(yReal) );
    NRMSEMaxMin = RMSE /( max(yReal) - min(yReal) );
    NRMSESd = RMSE /( std(yReal) );
    NRMSEIQ = RMSE /( quantile(yReal,0.75) - quantile(yReal,0.25) );

    MPE = nansum( (yfit - yReal) ./ yReal )  / numel(yReal(isNotMissing) ) * 100;
    MAPE = nansum( abs( (yfit - yReal) ./ yReal ) ) / numel(yReal(isNotMissing) ) * 100;
    MSPE = nansum( ( (yfit - yReal) ./ yReal ).^2) / numel(yReal(isNotMissing) ) * 100;
    RMSPE = sqrt(MSPE);
    
    EV = [RMSE, MAE, MSE];
    EVP = [RMSPE, MAPE, MSPE, MPE];
    NRV = [NRMSEAve, NRMSEMaxMin, NRMSESd, NRMSEIQ];
    
end

