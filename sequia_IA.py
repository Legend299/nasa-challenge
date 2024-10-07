import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import numpy as np

data = pd.read_csv('datos2.csv')
data['MapDate'] = pd.to_datetime(data['MapDate'], format='%Y%m%d')

data_ia = data[data['StateAbbreviation'] == 'IA']
data_tx = data[data['StateAbbreviation'] == 'TX']
data_mo = data[data['StateAbbreviation'] == 'MO']

def entrenar_y_predecir_sequia(data_estado):
    X = data_estado[['D0', 'D1', 'D2', 'D3', 'D4']]
    y = data_estado['D0']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model

def predecir_sequia():
    fecha_futura = datetime.now()
    model_ia = entrenar_y_predecir_sequia(data_ia)
    model_tx = entrenar_y_predecir_sequia(data_tx)
    model_mo = entrenar_y_predecir_sequia(data_mo)

    predicciones = []
    current_date = fecha_futura
    end_of_year = datetime(fecha_futura.year, 12, 31)

    while current_date <= end_of_year:
        last_30_days_ia = data_ia.tail(30)
        last_30_days_tx = data_tx.tail(30)
        last_30_days_mo = data_mo.tail(30)

        trend_ia = {col: (last_30_days_ia[col].mean(), last_30_days_ia[col].std()) for col in ['D0', 'D1', 'D2', 'D3', 'D4']}
        trend_tx = {col: (last_30_days_tx[col].mean(), last_30_days_tx[col].std()) for col in ['D0', 'D1', 'D2', 'D3', 'D4']}
        trend_mo = {col: (last_30_days_mo[col].mean(), last_30_days_mo[col].std()) for col in ['D0', 'D1', 'D2', 'D3', 'D4']}

        future_data = pd.DataFrame({
            'D0': [trend_ia['D0'][0] + np.random.normal(0, trend_ia['D0'][1])],
            'D1': [trend_ia['D1'][0] + np.random.normal(0, trend_ia['D1'][1])],
            'D2': [trend_ia['D2'][0] + np.random.normal(0, trend_ia['D2'][1])],
            'D3': [trend_ia['D3'][0] + np.random.normal(0, trend_ia['D3'][1])],
            'D4': [trend_ia['D4'][0] + np.random.normal(0, trend_ia['D4'][1])]
        })

        prediccion_ia = model_ia.predict(future_data)[0]

        future_data_tx = pd.DataFrame({
            'D0': [trend_tx['D0'][0] + np.random.normal(0, trend_tx['D0'][1])],
            'D1': [trend_tx['D1'][0] + np.random.normal(0, trend_tx['D1'][1])],
            'D2': [trend_tx['D2'][0] + np.random.normal(0, trend_tx['D2'][1])],
            'D3': [trend_tx['D3'][0] + np.random.normal(0, trend_tx['D3'][1])],
            'D4': [trend_tx['D4'][0] + np.random.normal(0, trend_tx['D4'][1])]
        })

        prediccion_tx = model_tx.predict(future_data_tx)[0]

        future_data_mo = pd.DataFrame({
            'D0': [trend_mo['D0'][0] + np.random.normal(0, trend_mo['D0'][1])],
            'D1': [trend_mo['D1'][0] + np.random.normal(0, trend_mo['D1'][1])],
            'D2': [trend_mo['D2'][0] + np.random.normal(0, trend_mo['D2'][1])],
            'D3': [trend_mo['D3'][0] + np.random.normal(0, trend_mo['D3'][1])],
            'D4': [trend_mo['D4'][0] + np.random.normal(0, trend_mo['D4'][1])]
        })

        prediccion_mo = model_mo.predict(future_data_mo)[0]

        predicciones.append({
            'fecha': current_date.date(),
            'prediccion_IA': prediccion_ia,
            'prediccion_TX': prediccion_tx,
            'prediccion_MO': prediccion_mo
        })

        current_date += timedelta(days=1)

    df_predicciones = pd.DataFrame(predicciones)
    df_predicciones.to_csv('sequia_pre.csv', index=False)
    print("Predicciones guardadas en 'sequia_pre.csv'.")

predecir_sequia()