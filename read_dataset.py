import pandas as pd

# Cambia 'ruta/del/archivo.csv' por la ruta real de tu archivo CSV
df = pd.read_csv('mbsa.csv')

# Muestra las primeras 5 filas del dataset
print(df.head())