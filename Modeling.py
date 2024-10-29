from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np

models = {'ARIMA':ARIMA, 'МНК':sm.OLS, 'ОМНК':sm.GLS, 'рао':sm.OLS,
          'дерево_решений':DecisionTreeRegressor, 'случайный_лес':RandomForestRegressor}


class Counting:
    def __init__(self, model_type:str, models_params:dict, x_train, y_train, x_test) ->None:
        self.model = model_type(**models_params)
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        
        
    def fit (self) ->None:
        try:
            self.model.fit(self.x_train, self.y_train)
        except ValueError:
            return self.model.fit()
        else:
            return None
            
        
        
    def predict (self, model, n:int=4):
        try:
            return self.model.predict(self.x_test)
        except NotImplementedError:
            return model.forecast(steps=n)
        
        
    
    def result_counting (self):
        if len(self.x_train) == len(self.y_train):
            model = self.fit()
            y_pred = self.predict(model)
            return y_pred, model
        print('Длина рядов данных X и y не совпадает')
        return None, None
        
        
        
        
x_train = np.array([1,2,3,4,5]).reshape(-1,1)

y_train = np.array([122, 134, 234, 245, 213]).reshape(-1, 1)
x_test = np.arange(10).reshape(-1, 1)
model = Counting(models.get('ARIMA'), {'endog':x_train, 'order':(1,1,1)}, x_train, y_train, x_test)
model1 = Counting(models.get('дерево_решений'), {'min_samples_leaf':4}, x_train, y_train, x_test)
print(model.result_counting()[0])
print(model1.result_counting()[0])
# print(model.fit().predict(4))

