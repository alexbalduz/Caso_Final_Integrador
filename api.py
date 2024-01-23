from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime

app = Flask(__name__)

# Cargamos el modelo entrenado
model = load_model('football_sales_model.h5')

def preprocess_date(date_str):
    # Convierte la cadena de fecha a un objeto de fecha en el formato adecuado
    date_object = datetime.strptime(date_str, "%Y-%m-%d").date()
    # Realiza cualquier preprocesamiento adicional si es necesario
    return date_object

@app.route('/predict', methods=['POST'])
def predict():
    # Obtener detalles de las camisetas de fútbol desde la solicitud POST
    request_data = request.json

    def preprocess_input(data_from_request):
        # Obtener datos de la solicitud
        quantity = data_from_request['quantity']
        unit_price = data_from_request['unit_price']
        country = data_from_request['country']
        invoice_date = data_from_request['invoice_date']

        # Realizar cualquier preprocesamiento necesario para la fecha
        processed_date = preprocess_date(invoice_date)

        encoder = OneHotEncoder(sparse=False)

        # Aplicar one-hot encoding a la columna 'Country'
        country_encoded = encoder.transform([[country]]).toarray()

        # Concatenar las características para la entrada del modelo
        input_data = np.concatenate([np.array([[quantity, unit_price]]), country_encoded], axis=1)

        return input_data

    # Supongamos que 'request_data' es la información de la solicitud
    input_data = preprocess_input(request_data)

    # Realizar la predicción con el modelo
    prediction = model.predict(input_data)

    # Devolver la predicción como JSON
    return jsonify({'prediction': prediction[0].tolist()})

if __name__ == '__main__':
    app.run(debug=True)