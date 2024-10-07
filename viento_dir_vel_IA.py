import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import numpy as np

data = pd.read_csv('lowa completo.csv'),

data = data.dropna(subset='avg_wind_speed_kts')
data = data.dropna(subset='avg_wind_drct')


X = data[['max_temp_f', 'min_temp_f', 'max_dewpoint_f', 'min_dewpoint_f', 'precip_in', 'min_rh', 'avg_rh', 'max_rh']]
y_wind_speed = data['avg_wind_speed_kts']
y_wind_direction = data['avg_wind_drct']


X_train, X_test, y_wind_speed_train, y_wind_speed_test = train_test_split(X, y_wind_speed, test_size=0.2, random_state=42)
X_train, X_test, y_wind_direction_train, y_wind_direction_test = train_test_split(X, y_wind_direction, test_size=0.2, random_state=42)


model_wind_speed = RandomForestRegressor(n_estimators=100, random_state=42)
model_wind_speed.fit(X_train, y_wind_speed_train)

model_wind_direction = RandomForestRegressor(n_estimators=100, random_state=42)
model_wind_direction.fit(X_train, y_wind_direction_train)

def predict_wind():
    fecha_futura = datetime.now()
    current_date = fecha_futura
    end_of_year = datetime(fecha_futura.year, 12, 31)

    predicciones_wind_speed = []
    predicciones_wind_direction = []

    while current_date <= end_of_year:
        last_30_days_ia = data.tail(30)

        trend_ia = {col: (last_30_days_ia[col].mean(), last_30_days_ia[col].std()) for col in X.columns}

        future_data = pd.DataFrame({
            col: [trend_ia[col][0] + np.random.normal(0, trend_ia[col][1])] for col in X.columns
        })

        prediccion_wind_speed = model_wind_speed.predict(future_data)[0]
        prediccion_wind_direction = model_wind_direction.predict(future_data)[0]

        predicciones_wind_speed.append({
            'fecha': current_date.date(),
            'prediccion': prediccion_wind_speed,
        })

        predicciones_wind_direction.append({
            'fecha': current_date.date(),
            'prediccion': prediccion_wind_direction,
        })

        current_date += timedelta(days=1)

    df_predicciones_wind_speed = pd.DataFrame(predicciones_wind_speed)
    df_predicciones_wind_direction = pd.DataFrame(predicciones_wind_direction)

    df_predicciones_wind_speed.to_csv('wind_speed_predIA.csv', index=False)
    df_predicciones_wind_direction.to_csv('wind_direction_predIA.csv', index=False)

    print("Predicciones guardadas en 'wind_speed_pred.csv' y 'wind_direction_pred.csv'.")

predict_wind()