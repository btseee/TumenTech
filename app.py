from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API_KEY')

@app.route('/')
def index():
    return render_template('index.html', google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expense = float(data['gross_weight']) * 10 + float(data['size']) * 5
    return jsonify({'expense': expense})

if __name__ == '__main__':
    app.run(debug=True)
