import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import numpy as np

# Cargar los datos del archivo CSV
data = pd.read_csv('lowa completo.csv')

# Verificar si hay valores nulos en las columnas de temperatura
print(data['max_temp_f'].isnull().sum(), data['min_temp_f'].isnull().sum())
data = data.dropna(subset=['max_temp_f', 'min_temp_f'])

# Función para entrenar y predecir la temperatura
def entrenar_y_predecir_temperatura(data_estado):
    # Seleccionamos las columnas de entrada (features) y la salida (target)
    X = data_estado[['max_temp_f', 'min_temp_f']]  # Puedes agregar más columnas si lo deseas
    y_max = data_estado['max_temp_f']  # La variable objetivo será la temperatura máxima
    y_min = data_estado['min_temp_f']  # Y también predecimos la mínima
    
    # Dividir los datos en entrenamiento y prueba (80%-20%)
    X_train, X_test, y_max_train, y_max_test, y_min_train, y_min_test = train_test_split(
        X, y_max, y_min, test_size=0.2, random_state=42
    )

    # Crear y entrenar el modelo Random Forest para ambas temperaturas
    model_max = RandomForestRegressor(n_estimators=100, random_state=42)
    model_min = RandomForestRegressor(n_estimators=100, random_state=42)
    
    model_max.fit(X_train, y_max_train)  # Entrenamos para la máxima
    model_min.fit(X_train, y_min_train)  # Entrenamos para la mínima

    return model_max, model_min


# Función para predecir las temperaturas futuras
def predecir_temperatura():
    fecha_futura = datetime.now()
    model_max, model_min = entrenar_y_predecir_temperatura(data)

    predicciones = []
    current_date = fecha_futura
    end_of_year = datetime(fecha_futura.year, 12, 31)  # Predecir hasta el final del año

    while current_date <= end_of_year:
        # Tomar los últimos 30 días para analizar la tendencia de la temperatura
        last_30_days = data.tail(30)

        # Calcular la tendencia (media y desviación estándar) para generar datos futuros
        trend_temp = {col: (last_30_days[col].mean(), last_30_days[col].std()) for col in ['max_temp_f', 'min_temp_f']}

        # Generar datos simulados para la fecha futura
        future_data = pd.DataFrame({
            'max_temp_f': [trend_temp['max_temp_f'][0] + np.random.normal(0, trend_temp['max_temp_f'][1])],
            'min_temp_f': [trend_temp['min_temp_f'][0] + np.random.normal(0, trend_temp['min_temp_f'][1])],
        })

        # Hacer la predicción de temperatura máxima y mínima
        prediccion_max = model_max.predict(future_data[['max_temp_f', 'min_temp_f']])[0]
        prediccion_min = model_min.predict(future_data[['max_temp_f', 'min_temp_f']])[0]

        # Guardar la predicción en la lista
        predicciones.append({
                'fecha': current_date.date(),
                'prediccion_max': prediccion_max,
                'prediccion_min': prediccion_min,
            })

        # Avanzar al siguiente día
        current_date += timedelta(days=1)

    # Convertir las predicciones en un DataFrame y guardarlas en un archivo CSV
    df_predicciones = pd.DataFrame(predicciones)
    df_predicciones.to_csv('temperaturas_futurasIA.csv', index=False)
    print("Predicciones guardadas en 'temperaturas_futuras.csv'.")

# Llamada a la función para generar predicciones futuras
predecir_temperatura()