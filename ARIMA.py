import pandas as pd
import numpy as np

# Генерация примера DataFrame
np.random.seed(0)
data = {
    'A': np.random.rand(100),
    'B': np.random.rand(100),
    'C': np.random.rand(100),
    'D': np.random.rand(100)
}
df = pd.DataFrame(data)

# Задание порога корреляции
threshold = 0.1

# Расчет корреляционной матрицы
correlation_matrix = df.corr()

# Функция для получения корреляций выше заданного порога
def get_high_correlations(corr_matrix, threshold):
    # Создаем список для хранения результатов
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

# Получение высоких корреляций
high_correlations_df = get_high_correlations(correlation_matrix, threshold)

# Вывод результатов
print("Корреляции выше порога:")
print(high_correlations_df)
