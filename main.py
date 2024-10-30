from Data_model import DataSeriesDataset, Config
from Modeling import Counting, models
from recomendation import Recommendations
from sklearn.metrics import r2_score, mean_absolute_percentage_error
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf
import pandas as pd

def main ():
    # config = Config()
    # conf = config.read_config('horizon/config.ini')
    # dataset = DataSeriesDataset(conf, 'Horizon')
    # tables = dataset.query_to_db('2013-01-01T00:00:00Z', dataset.client.query_api(), '2022-10-01T00:00:00Z')
    # df = dataset.df_forming(tables)
    # result_df = dataset.dataframe_transform(df)
   
    # result_df.columns.name = None  # Удаляем имя индекса
    
    # result_df[result_df.columns[1:]] = result_df[result_df.columns[1:]].astype(float)
    # result_df.to_csv('result.csv')
    # result_df.info()
    result_df = pd.read_csv('horizon/social_data_last.csv', sep=';', encoding='1251')
    r = Recommendations(result_df.drop('Период', axis = 1))
    params = r.recomendations_ARIMA()
    print(params)
    # for indicator in params.keys():
    #     x_train = result_df[indicator].iloc[:-4]
    #     x_test = result_df[indicator].iloc[-4:]
    #     y_train = result_df[indicator].iloc[:-4]
    #     model = Counting(models.get('ARIMA'), {'order':params[indicator], 'endog':x_train}, x_train, x_test, y_train)
    #     # print(model.result_counting()[0])
    #     y_pred = model.result_counting()[1].predict(start=0, end = len(y_train)-1, typ='levels')
    #     print(r2_score(y_pred[1:], y_train[1:]))
    #     print(mean_absolute_percentage_error(model.result_counting()[0], x_test))
    #     print(model.result_counting()[1].summary())
    result_df = pd.read_csv('horizon/social_data_last.csv', sep=';', encoding='1251')
    x_train = result_df['ZZ'].iloc[:-4]
    x_test = result_df['ZZ'].iloc[-4:]
    y_train = result_df['ZZ'].iloc[:-4]
    model = Counting(models.get('ARIMA'), {'order':(5,0,1), 'endog':x_train}, x_train, x_test, result_df['CK1'].iloc[:-4])

    print(model.result_counting()[0])
    print(model.result_counting()[1].summary())
    y_pred = model.result_counting()[1].predict(start=0, end = len(y_train)-1, typ='levels')
    print(y_pred[1:])
    print(y_train[1:])
    print(round(r2_score(y_pred[1:], y_train[1:]), 1))
    print(mean_absolute_percentage_error(model.result_counting()[0], x_test))
if __name__ == '__main__':
    main()