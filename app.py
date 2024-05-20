from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API_KEY')

# Constants
GASOLINE_CONSUMPTION_RATES = {
    'car': 0.08,  # liters per km (example values)
    'truck': 0.25,
    'van': 0.15
}
FOOD_HOTEL_EXPENSE_PER_DAY = 50000  # MNT per day (example value)
TAX_RATE = 0.115
DRIVER_EARNING_PER_DAY = 100000  # MNT per day (example value)

@app.route('/')
def index():
    return render_template('index.html', google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    from_location = data['from']
    to_location = data['to']
    car_type = data['car_type']
    gross_weight = float(data['gross_weight'])
    size = float(data['size'])

    distance, duration = get_distance_and_duration(from_location, to_location)
    if distance is None or duration is None:
        return jsonify({'error': 'Could not calculate distance or duration'}), 400

    # Fetch gasoline price from an external API
    gasoline_price = get_gasoline_price()
    if gasoline_price is None:
        return jsonify({'error': 'Could not fetch gasoline price'}), 500

    # Gasoline usage and expense
    gasoline_consumption_rate = GASOLINE_CONSUMPTION_RATES.get(car_type, 0.08)
    gasoline_usage = distance * gasoline_consumption_rate
    gasoline_expense = gasoline_usage * gasoline_price

    # Food and hotel expense based on the duration
    food_hotel_expense = (duration / 24) * FOOD_HOTEL_EXPENSE_PER_DAY

    # Tax
    tax = (gasoline_expense + food_hotel_expense) * TAX_RATE

    # Driver's earning
    drivers_earning = (duration / 24) * DRIVER_EARNING_PER_DAY

    # Total expense
    total_expense = gasoline_expense + food_hotel_expense + tax + drivers_earning

    return jsonify({
        'duration': duration,
        'gasoline_usage': gasoline_usage,
        'gasoline_expense': gasoline_expense,
        'food_hotel_expense': food_hotel_expense,
        'tax': tax,
        'drivers_earning': drivers_earning,
        'total_expense': total_expense
    })

def get_distance_and_duration(from_location, to_location):
    api_key = app.config['GOOGLE_MAPS_API_KEY']
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        'origins': from_location,
        'destinations': to_location,
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['rows']:
            elements = result['rows'][0]['elements']
            if elements and elements[0]['status'] == 'OK':
                distance = elements[0]['distance']['value'] / 1000  # Convert meters to kilometers
                duration = elements[0]['duration']['value'] / 3600  # Convert seconds to hours
                return distance, duration
    return None, None

def get_gasoline_price():
    # Example API call to fetch gasoline price
    # Replace with actual API call if available
    url = "https://api.example.com/gasoline_price"
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        return result['price']
    return None

if __name__ == '__main__':
    app.run(debug=True)
