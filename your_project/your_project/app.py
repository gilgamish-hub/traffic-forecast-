from flask import Flask, request, render_template, jsonify
import pandas as pd
import os
import requests

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle file upload and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Process the CSV file and call the external API
        try:
            # Pass the file path as a parameter to the external API
            external_api_url = 'http://127.0.0.1:5500/getPredictionOutput'
            payload = {'filepath': filepath}  # Send the file path to the API
            response = requests.get(external_api_url, params=payload, timeout=10)  # Include file path in the query parameters
            response.raise_for_status()  # Raise an error if the response status code is not 200

            # Pass the API response data to the template if needed
            data = response.json()  # Ensure the external API returns JSON
            return render_template('pred.html', data=data)

        except requests.exceptions.ConnectionError:
            return jsonify({'error': 'Failed to connect to the external API. Please check if it is running.'}), 500
        except requests.exceptions.Timeout:
            return jsonify({'error': 'The external API timed out. Please try again later.'}), 500
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'An error occurred: {e}'}), 500

    else:
        return jsonify({'error': 'Unsupported file format. Please upload a CSV file.'}), 400


@app.route('/pred')
def preds():
    return render_template("pred.html")

if __name__ == '__main__':
    app.run(debug=True)
