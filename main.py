from flask import Flask, request, jsonify
import numpy as np
import joblib
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the trained model and vectorizer
logging.info("Loading model and vectorizer...")
model = joblib.load('app/SVM_model.pkl')
vectorizer = joblib.load('app/vectorizer.pkl')
logging.info("Model and vectorizer loaded successfully.")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Log the POST request
        logging.info("POST request received")

        # Extract the input data from the request
        data = request.json
        logging.info(f"Data received: {data}")
        input_text = data.get('input', '')

        if not input_text:
            logging.warning("No input provided")
            return jsonify({'error': 'No input provided'}), 400

        # Preprocess the input text
        logging.info(f"Input text received: {input_text}")
        vectorized_input = vectorizer.transform([input_text])
        logging.info("Input vectorized")

        # Make a prediction using the preprocessed input
        prediction = model.predict(vectorized_input)
        logging.info("Prediction made")

        # Convert prediction to list if it's a numpy array (JSON serializable)
        prediction_list = prediction.tolist() if isinstance(prediction, np.ndarray) else prediction
        logging.info(f"Prediction: {prediction_list}")

        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction_list})

    except Exception as e:
        # Log any errors and return a JSON error message
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/predict', methods=['GET'])
def predict_page():
    return (
        "<h1>Predict Endpoint</h1>"
        "<p>This is the predict endpoint. Please use a POST request with JSON input to get predictions.</p>"
    )

if __name__ == '__main__':
    # Enable debug mode for better error messages
    app.run(host='0.0.0.0', port=9010, debug=True)
