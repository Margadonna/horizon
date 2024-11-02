from Data_model import DataSeriesDataset, Config
from Modeling import Counting, models
from recomendation import Recommendations
from sklearn.metrics import r2_score, mean_absolute_percentage_error
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf
import pandas as pd

def main ():
    config = Config()
    conf = config.read_config('horizon/config.ini')
    dataset = DataSeriesDataset(conf, 'Horizon')
    tables = dataset.query_to_db('2013-01-01T00:00:00Z', dataset.client.query_api(), '2022-10-01T00:00:00Z')
    df = dataset.df_forming(tables)
    result_df = dataset.dataframe_transform(df)
   
    result_df.columns.name = None  # Удаляем имя индекса
    
    result_df[result_df.columns[1:]] = result_df[result_df.columns[1:]].astype(float)
    result_df.to_csv('result.csv')
    result_df.info()

    # result_df = pd.read_csv('horizon/social_data_last.csv', sep=';', encoding='1251')
    r = Recommendations(result_df.drop('time', axis = 1)[:-4])
    # r.correlations_count(0.5).to_csv('correl.csv')
    result_df.drop('time', axis = 1)[:-4].corr().to_csv('correl1.csv')
    params = r.recomendations_ARIMA()
    # print(params)
    # params = {'CKG1': (3, 4, 0), 'AAPEN':(1,1,1), 'AMINC': (1,2,1), 'RMI1':(2, 0, 1), 'CE3':(1, 1, 1), 'CK1': (1,1,1), 'NNI1':(3,1,1), 'MIP': (4,2,1), 'AMAW': (2,3,1),
    #           'PBT1': (3, 1, 1), 'CKD1': (3, 4, 1)}

    for indicator in params.keys():
        x_train = result_df[indicator].iloc[:-4]
        x_test = result_df[indicator].iloc[-4:]
        y_train = result_df[indicator].iloc[:-4]
        model = Counting(models.get('ARIMA'), {'order':params[indicator], 'endog':x_train}, x_train, x_test, y_train)
        # print(model.result_counting()[0])
        y_pred = model.result_counting()[1].predict(start=0, end = len(y_train)-1, typ='levels')
        print(indicator, r2_score(y_pred[params[indicator][0]:], y_train[params[indicator][0]:]))
        print(indicator, mean_absolute_percentage_error(model.result_counting()[0], x_test))
        print(model.result_counting()[1].summary())
   


if __name__ == '__main__': 
    main()