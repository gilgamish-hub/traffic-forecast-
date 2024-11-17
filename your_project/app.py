from flask import Flask, request, render_template, jsonify
import pandas as pd
import os

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

        # Process the CSV file
        try:
            data = pd.read_csv(filepath)
            # Example: Perform analysis
            analysis_result = {
                'row_count': len(data),
                'column_count': len(data.columns),
                'columns': list(data.columns)
            }
            os.remove(filepath)  # Clean up the uploaded file
            return jsonify(analysis_result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Unsupported file format. Please upload a CSV file.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
