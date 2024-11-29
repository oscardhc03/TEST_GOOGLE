from flask import Flask, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)

from flask_cors import CORS
CORS(app)

# Cargar el modelo TFLite
interpreter = tf.lite.Interpreter(model_path="C:/Users/Oscar/Desktop/server/model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Etiquetas de las clases
with open("C:/Users/Oscar/Desktop/server/labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

predictions_data = {}

@app.route('/', methods=['GET'])
def home():
    return "Servidor Flask funcionando correctamente", 200

@app.route('/predict', methods=['GET','POST'])
def predict():
    global predictions_data

    # Verificar si hay una imagen en la solicitud
    if 'imageFile' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    # Leer y procesar la imagen
    image = Image.open(request.files['imageFile']).convert('RGB').resize((224, 224))
    input_data = np.expand_dims(np.array(image) / 255.0, axis=0).astype(np.float32)

    # Realizar la predicción
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]

    # Guardar las predicciones
    predictions_data = {labels[i]: float(predictions[i]) for i in range(len(labels))}
    return jsonify(predictions_data)

@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    global predictions_data
    return jsonify(predictions_data)

@app.before_request
def log_request_info():
    print(f"Solicitud recibida: {request.method} {request.url}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)