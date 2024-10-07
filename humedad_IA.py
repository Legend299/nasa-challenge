import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import numpy as np

data = pd.read_csv('missouri completo.csv')

print(data['min_rh'].isnull().sum())
data = data.dropna(subset=['min_rh'])


def entrenar_y_predecir_humedad(data_estado):
    X = data_estado[['min_rh','avg_rh','max_rh']]
    y = data_estado['min_rh']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42) 
    model.fit(X_train, y_train)

    return model


def predecir_humedad():
    fecha_futura = datetime.now()
    model = entrenar_y_predecir_humedad(data)

    predicciones = []
    current_date = fecha_futura
    end_of_year = datetime(fecha_futura.year, 12, 31)

    while current_date <= end_of_year:
        last_30_days_ia = data.tail(30)

        trend_ia = {col: (last_30_days_ia[col].mean(), last_30_days_ia[col].std()) for col in ['min_rh','avg_rh','max_rh']}

        future_data = pd.DataFrame({
            'min_rh': [trend_ia['min_rh'][0] + np.random.normal(0, trend_ia['min_rh'][1])],
            'avg_rh': [trend_ia['avg_rh'][0] + np.random.normal(0, trend_ia['avg_rh'][1])],
            'max_rh': [trend_ia['max_rh'][0] + np.random.normal(0, trend_ia['max_rh'][1])],
        })

        prediccion = model.predict(future_data)[0]

        predicciones.append({
                'fecha': current_date.date(),
                'prediccion': prediccion,
            })

        current_date += timedelta(days=1)

    df_predicciones = pd.DataFrame(predicciones)
    df_predicciones.to_csv('humedad_preMO.csv', index=False)
    print("Predicciones guardadas en 'humedad_pre.csv'.")

predecir_humedad()