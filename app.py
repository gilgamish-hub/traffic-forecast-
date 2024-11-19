from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import main  # Assuming your prediction logic is in the `main` module

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class Test(Resource):
    def get(self):
        return 'Welcome to, Test App API!'

    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'Post Values': value}, 201
            return {"error":"Invalid format."}
        except Exception as error:
            return {'error': str(error)}

class GetPredictionOutput(Resource):
    def get(self):
        try:
            # Get file path from the query parameters
            filepath = request.args.get('filepath')
            
            # Check if the filepath is provided and if the file exists
            if not filepath or not os.path.exists(filepath):
                return jsonify({'error': 'Invalid or missing file path.'}), 400
            
            # Assuming `main.predict()` accepts a file path as an argument
            result = main.predict(filepath)  # Modify this line according to your `main.predict` method
            
            return jsonify(result)  # Assuming `result` is a dictionary or JSON-serializable
            
        except Exception as error:
            return jsonify({"error": str(error)}), 500

    def post(self):
        return jsonify({"error": "Invalid Method."})

# Registering the routes
api.add_resource(Test, '/')
api.add_resource(GetPredictionOutput, '/getPredictionOutput')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500, debug=True)
