import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import numpy as np

data = pd.read_csv('missouri completo.csv')

print(data['min_dewpoint_f'].isnull().sum())
data = data.dropna(subset=['min_dewpoint_f'])

def entrenar_y_predecir_dewpoint(data_estado):
    X = data_estado[['min_dewpoint_f', 'max_dewpoint_f']]
    y = data_estado['min_dewpoint_f']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42) 
    model.fit(X_train, y_train)

    return model

def predecir_dewpoint():
    fecha_futura = datetime.now()
    model = entrenar_y_predecir_dewpoint(data)

    predicciones = []
    current_date = fecha_futura
    end_of_year = datetime(fecha_futura.year, 12, 31)

    while current_date <= end_of_year:
        last_30_days_ia = data.tail(30)

        trend_ia = {col: (last_30_days_ia[col].mean(), last_30_days_ia[col].std()) for col in ['min_dewpoint_f', 'max_dewpoint_f']}

        future_data = pd.DataFrame({
            'min_dewpoint_f': [trend_ia['min_dewpoint_f'][0] + np.random.normal(0, trend_ia['min_dewpoint_f'][1])],
            'max_dewpoint_f': [trend_ia['max_dewpoint_f'][0] + np.random.normal(0, trend_ia['max_dewpoint_f'][1])],
        })

        prediccion = model.predict(future_data)[0]

        predicciones.append({
                'fecha': current_date.date(),
                'prediccion_min': prediccion,
                'prediccion_max': prediccion + (trend_ia['max_dewpoint_f'][0] - trend_ia['min_dewpoint_f'][0]),
            })

        current_date += timedelta(days=1)

    df_predicciones = pd.DataFrame(predicciones)
    df_predicciones.to_csv('dewpoint_preMO.csv', index=False)
    print("Predicciones guardadas en 'dewpoint_pre.csv'.")

predecir_dewpoint()