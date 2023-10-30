from flask import Flask, request, jsonify
from joblib import load

# Cargar el modelo
pipeline = load('Modelo predictivo\model.joblib')

# Crear una aplicación Flask
app = Flask(__name__)

# Ruta para realizar predicciones
@app.route('/predict/', methods=['POST'])
def predict():
    try:
        data = request.json
        text = data.get('text')
        prediction = pipeline.predict([text])[0]
        return jsonify({'prediction': prediction})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)