import numpy as np
from scipy import stats
import statsmodels.stats.multicomp as multi
from statsmodels.tsa.stattools import adfuller
import pandas as pd 



class TimeSeriesProperties:

    def check_stationarity_ttest(self, series, split_ratio = 0.5):
    # Разделение временного ряда на две части
        split_index = int(len(series) * split_ratio)
        first_half = series[:split_index]
        second_half = series[split_index:]
        # Вычисление средних значений
        mean1 = np.mean(first_half)
        mean2 = np.mean(second_half)
        # Вычисление стандартных отклонений
        std1 = np.std(first_half, ddof=1)
        std2 = np.std(second_half, ddof=1)
        # Количество наблюдений
        n1 = len(first_half)
        n2 = len(second_half)
        # t-статистика
        t_stat = (mean1 - mean2) / np.sqrt((std1**2 / n1) + (std2**2 / n2))
        # Степени свободы
        df = n1 + n2 - 2
        # p-значение
        p_value = stats.t.sf(np.abs(t_stat), df) * 2  # Двусторонний тест
        return t_stat, p_value
    

    def check_stationarity_fisher(self, series, split_ratio = 0.5):
        # Разделение временного ряда на две части
        split_index = int(len(series) * split_ratio)
        first_half = series[:split_index]
        second_half = series[split_index:]
        # Вычисление дисперсий
        var1 = np.var(first_half, ddof=1)
        var2 = np.var(second_half, ddof=1)
        # Количество наблюдений
        n1 = len(first_half)
        n2 = len(second_half)
        # F-статистика
        f_stat = var1 / var2 if var1 > var2 else var2 / var1
        # p-значение
        p_value = stats.f.sf(f_stat, n1 - 1, n2 - 1)  # Односторонний тест
        return f_stat, p_value
    

    def check_stationarity_mannwhitney(self, series, split_ratio=0.5):
        # Разделение временного ряда на две части
        split_index = int(len(series) * split_ratio)
        first_half = series[:split_index]
        second_half = series[split_index:]
        # Выполнение теста Манна-Уитни
        u_stat, p_value = stats.mannwhitneyu(first_half, second_half, alternative='two-sided')
        return u_stat, p_value


# Функция для проверки стационарности с помощью теста Сиджелла-Тьюки
    def check_stationarity_siegel_tukey(self, series, split_ratio=0.5):
        # Разделение временного ряда на две части
        split_index = int(len(series) * split_ratio)
        first_half = series[:split_index]
        second_half = series[split_index:]
        array1 = np.full(len(first_half), 'A')
        array2 = np.full(len(second_half), 'B')
        data = np.hstack([first_half, second_half])
        classes = np.hstack([array1, array2])
        # Выполнение теста Сиджелла-Тьюки
        results = multi.pairwise_tukeyhsd(data, classes)
        return results.meandiffs[0], results.pvalues[0], results.reject[0]

    # Функция для выполнения теста Дики-Фуллера
    def adf_test(self, series):
        result = adfuller(series)
        return result[0], result[1]

    def __init__(self, data):
        self.data = data
        self.stacionarity_check_func = {'t-stat':self.check_stationarity_ttest, 'f-stat':self.check_stationarity_fisher,
                                   'mann_whitney':self.check_stationarity_mannwhitney, 'siegel_tukey': self.check_stationarity_siegel_tukey,
                                   'adfuller': self.adf_test}
    

    def stacionarity_check (self, alpha=0.05):
        results = {'name':[], 't-stat':[], 'pvalue_t-stat':[], 'f-stat':[], 'pvalue_f-stat':[], 'mann_whitney':[], 'pvalue_mann_whitney':[], 
                   'siegel_tukey':[], 'pvalue_siegel_tukey':[], 'adfuller':[], 'pvalue_adfuller':[]}
        for indicator in self.data.columns:
            results['name'].append(indicator)
            for key in list(results)[1:]:
                if 'pvalue_' in key:
                    
                    results[key].append(self.stacionarity_check_func.get(key.replace('pvalue_', ''))(self.data[indicator])[1])
                else:
                    results[key].append(self.stacionarity_check_func.get(key)(self.data[indicator])[0])
        results = pd.DataFrame(results)
        results['stationary'] = results.apply(lambda row:
        True if (row['pvalue_t-stat'] > alpha) & (row['pvalue_f-stat']> alpha) & (row['mann_whitney']> alpha)
        and (row['pvalue_siegel_tukey']> alpha) & (row['pvalue_adfuller']<alpha) else False, axis =1)
        return results



def main():
    # Генерация временного ряда (пример)
    df = pd.read_csv('horizon/social_data_last.csv')
    df = df.drop(['Period', 'Unnamed: 44'], axis=1)
    df.info()
    # Преобразование в DataFrame
    # df = pd.DataFrame(time_series, columns=['value'])
    c = TimeSeriesProperties(df)
    print(c.stacionarity_check())


if __name__ == '__main__':
    main()
