from flask import Flask, request, jsonify, render_template
import pandas as pd

from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predecir', methods=['GET'])
@cross_origin()
def predecir():
    fecha_input = request.args.get('fecha')
    df_predicciones = pd.read_csv('sequia_pre.csv')
    prediccion = df_predicciones[df_predicciones['fecha'] == fecha_input]

    if not prediccion.empty:
        resultado = {
            'fecha': prediccion['fecha'].values[0],
            'prediccion_IA': prediccion['prediccion_IA'].values[0],
            'prediccion_TX': prediccion['prediccion_TX'].values[0],
            'prediccion_MO': prediccion['prediccion_MO'].values[0]
        }
        return jsonify(resultado)
    return jsonify({'error': 'Fecha no encontrada'})

@app.route('/predecir_humedad', methods=['GET'])
@cross_origin()
def predecir_humedad():
    fecha_input = request.args.get('fecha')

    df_iowa = pd.read_csv('humedad_pre.csv')
    df_texas = pd.read_csv('humedad_preTX.csv')
    df_missouri = pd.read_csv('humedad_preMO.csv')

    prediccion_iowa = df_iowa[df_iowa['fecha'] == fecha_input]
    prediccion_texas = df_texas[df_texas['fecha'] == fecha_input]
    prediccion_missouri = df_missouri[df_missouri['fecha'] == fecha_input]

    if not prediccion_iowa.empty and not prediccion_texas.empty and not prediccion_missouri.empty:
        resultado = {
            'fecha': fecha_input,
            'iowa': prediccion_iowa['prediccion'].values[0],
            'texas': prediccion_texas['prediccion'].values[0],
            'missouri': prediccion_missouri['prediccion'].values[0]
        }
        return jsonify(resultado)

    return jsonify({'error': 'Fecha no encontrada en uno o más estados'})

@app.route('/predecir_temperatura', methods=['GET'])
@cross_origin()
def predecir_temperatura():
    fecha_input = request.args.get('fecha')

    df_prediccionesTX = pd.read_csv('temperaturas_futurasTX.csv')
    df_prediccionesMO = pd.read_csv('temperaturas_futuras.csv')
    df_prediccionesIA = pd.read_csv('temperaturas_futurasIA.csv')

    prediccion_tx = df_prediccionesTX[df_prediccionesTX['fecha'] == fecha_input]
    prediccion_mo = df_prediccionesMO[df_prediccionesMO['fecha'] == fecha_input]
    prediccion_ia = df_prediccionesIA[df_prediccionesIA['fecha'] == fecha_input]

    if not prediccion_tx.empty and not prediccion_mo.empty and not prediccion_ia.empty:
        resultado = {
            'fecha': fecha_input,
            'texas': {
                'max': prediccion_tx['prediccion_max'].values[0],
                'min': prediccion_tx['prediccion_min'].values[0]
            },
            'missouri': {
                'max': prediccion_mo['prediccion_max'].values[0],
                'min': prediccion_mo['prediccion_min'].values[0]
            },
            'iowa': {
                'max': prediccion_ia['prediccion_max'].values[0],
                'min': prediccion_ia['prediccion_min'].values[0]
            }
        }
        return jsonify(resultado)

    return jsonify({'error': 'Fecha no encontrada'})

if __name__ == '__main__':
    app.run(debug=True)
