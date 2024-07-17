from flask import Flask, request, jsonify, render_template
import json
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Define file paths
json_file_path = '/home/alwazw/Fingerprint-json//data/fingerprints.json'

# Function to save data to JSON
def save_to_json(data):
    try:
        if not os.path.isfile(json_file_path):
            with open(json_file_path, 'w') as file:
                json.dump([], file)

	# Read existing data
        with open(json_file_path, 'r') as file:
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                file_data = []

 # Add timestamp to the data
        data['timestamp'] = datetime.now().isoformat()

        # Append new data
        file_data.append(data)

        # Write updated data back to file
        with open(json_file_path, 'w') as file:
            json.dump(file_data, file, indent=4)
        logging.info("Data successfully written to JSON file.")
    except Exception as e:
        logging.error(f"Error writing to JSON file: {e}")

# Endpoint to collect fingerprints
@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.json
        if not data:
            logging.error("No data provided.")
            return jsonify({'error': 'No data provided'}), 400

        # Get the client's IP address
        if request.headers.get('X-Forwarded-For'):
            data['ip'] = request.headers.get('X-Forwarded-For').split(',')[0]
        else:
            data['ip'] = request.remote_addr
        logging.debug(f"Received data: {data}")

        # Save data
        save_to_json(data)

        return jsonify({'message': 'Fingerprint collected'}), 200
    except Exception as e:
        logging.error(f"Error in /collect endpoint: {e}")
        return jsonify({'error': str(e)}), 500

# Serve the index page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
