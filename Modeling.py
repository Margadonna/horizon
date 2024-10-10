from statsmodels.tsa.arima.model import ARIMA
import statsmodels.api as sm
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


models = {'ARIMA':ARIMA, 'МНК':sm.OLS, 'ОМНК':sm.GLS, 'рао':sm.OLS,
          'дерево_решений':DecisionTreeRegressor, 'случайный лес':RandomForestRegressor}


class Counting:
    def __init__(self, model_type, models_params):
        self.model = model_type(**models_params)
        
    def fit (self, fit_params):
        self.model.fit(fit_params)
        
        
    def predict (self, predict_params):
        return self.model.predict(**predict_params)
        
        


