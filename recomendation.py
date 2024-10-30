
import pandas as pd
from TimeSeriesProperties import TimeSeriesProperties
from statsmodels.tsa.stattools import acf, pacf
import numpy as np

class Recommendations:
    def __init__(self, df) -> None:
        self.df = df
    
    
    def correlations_count (self, threshold):
        corr_matrix = self.df.corr()
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
    
    
    def ar_ma_value_recommend (self, column):
        # Расчет ACF и PACF
        lag_acf = acf(self.df[column], nlags=10)
        lag_pacf = pacf(self.df[column], nlags=10)
        # Определение p и q
        # p - порядок авторегрессии (из PACF)
        # q - порядок скользящей средней (из ACF)
        p = np.where(lag_pacf > 0.8)[0][-1]  # Последний лаг, где PACF > 0.2
        q = np.where(lag_acf > 0.8)[0][-1]   # Последний лаг, где ACF > 0.2
        return p, q

    

    def stacionarity_recomendation (self, max_d):
        res = []
        df = self.df.copy()
        for d in range(max_d):
            if d>0:
                df = df.diff().drop(0).reset_index(drop=True)
                ts = TimeSeriesProperties(df)
            else:
                ts = TimeSeriesProperties(self.df)
            result_df = ts.stacionarity_check()
            result_df['d'] = d
            res.append(result_df)
        result = pd.concat(res)
        result = result[result.stationary == True].reset_index(drop=True)
        result = result.drop_duplicates(subset = ['name', 'stationary']  )
        recomendation = result.set_index('name')['d'].to_dict()     
        return result, recomendation

    def recomendations_ARIMA (self, q_bias=1, p_bias=2):        
        stac = self.stacionarity_recomendation(5)[1]
        res = {}
        for indicator in stac.keys():
            p,q = self.ar_ma_value_recommend(indicator)
            if q>q_bias:
                q = q_bias
            if p!=0 or q!=0:
                res[indicator] = (p, stac[indicator], q)
        return res








def main():
    df = pd.read_csv('horizon/social_data_last.csv')
    df = df.drop(['Period', 'Unnamed: 44'], axis=1)
    # df.info()
    r = Recommendations(df)
    r.stacionarity_recomendation(4)[0].to_csv('stac.csv')
    print(r.recomendations_ARIMA())
    
if __name__ == '__main__':
    main()