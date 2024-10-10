from pmdarima import auto_arima
import pandas as pd



class Recommendations:
    def __init__(self) -> None:
        pass
    
    
    def correlations_count (self, df, threshold):
        corr_matrix = df.corr()
        high_corr_list = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    high_corr_list.append({
                        'Column 1': corr_matrix.columns[i],
                        'Column 2': corr_matrix.columns[j],
                        'Correlation': corr_matrix.iloc[i, j]
                    })
        return pd.DataFrame(high_corr_list)
    
    
    def ar_value_recommend (self, ts, season=False, stepw = True):
        model = auto_arima(ts, seasonal=season, stepwise=stepw, trace=True)
        print(model.summary())
        return model.order[0]
    
    
