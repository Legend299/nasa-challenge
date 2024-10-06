import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import numpy as np


data = pd.read_csv('lowa completo.csv')
data['MapDate'] = pd.to_datetime(data['MapDate'], format='%Y%m%d')

def entrenar_y_predecir_humedad(df):
    x = df[['min_rh', 'avg_rh', 'max_rh']]
    y = df['min_rh']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, randome_state=42)
    model.fit(X_train, y_train)

    return model

def predecir_humedad():
    fecha_futura = datetime.now()
    model_ia = entrenar_y_predecir(data)
    
    predicciones = []
    current_date = fecha_futura
    end_of_year = datetime(fecha_futura.year, 12, 31)