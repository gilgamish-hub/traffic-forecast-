from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import random

app = Flask(__name__)
api = Api(app)

class TrafficForecast(Resource):
    def post(self):
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Check if required fields are present
            if 'hour' not in data or 'day_of_week' not in data or 'location' not in data:
                return {"error": "Missing 'hour', 'day_of_week' or 'location' in request data."}, 400

            hour = data['hour']
            day_of_week = data['day_of_week']
            location = data['location']

            # Simple logic to determine traffic level based on time and location
            if location == "downtown":
                if 7 <= hour < 9 or 16 <= hour < 18:  # Rush hour
                    traffic_level = "High"
                elif 9 <= hour < 12 or 14 <= hour < 16:  # Moderate time
                    traffic_level = "Moderate"
                else:
                    traffic_level = "Low"
            else:  # Suburban or other areas
                traffic_level = "Low" if 22 <= hour < 7 else "Moderate"
            
            # Simulate traffic data (e.g., congestion percentage and average speed)
            congestion = random.randint(60, 100) if traffic_level == "High" else random.randint(30, 60)
            avg_speed = 20 if traffic_level == "High" else 40 if traffic_level == "Moderate" else 60

            # Adjust traffic for weekends
            if day_of_week in ["Saturday", "Sunday"]:
                if traffic_level == "High":
                    traffic_level = "Moderate"  # Less traffic on weekends for downtown

            # Create the prediction response
            prediction = {
                "traffic_level": traffic_level,
                "congestion_percentage": congestion,
                "average_speed_kmh": avg_speed,
                "hour": hour,
                "day_of_week": day_of_week,
                "location": location
            }

            return jsonify(prediction)

        except Exception as error:
            return {"error": str(error)}, 500

# Add the resource to the API with the route '/forecast'
api.add_resource(TrafficForecast, '/forecast')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
