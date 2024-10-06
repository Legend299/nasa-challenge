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

if __name__ == '__main__':
    app.run(debug=True)
