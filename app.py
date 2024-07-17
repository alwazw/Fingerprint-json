from flask import Flask, request, jsonify, render_template
import json
import os
#import csv
import pandas as pd
#import pyodbc
from datetime import datetime

app = Flask(__name__)

# MSSQL Database connection setup
#server = '10.10.10.202'
#database = 'Campain'
#username = 'SA'
#password = 'abcdef!2'
#driver = '{ODBC Driver 17 for SQL Server}'

#connection_string = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'

# Define file paths
#csv_file_path = '/home/alwazw/redirect-sql/data/fingerprints.csv'
json_file_path = '/home/alwazw/redirect-sql/data/fingerprints.json'

# Function to save data to CSV
#def save_to_csv(data):
#    file_exists = os.path.isfile(csv_file_path)
#    with open(csv_file_path, mode='a', newline='') as file:
#        writer = csv.DictWriter(file, fieldnames=data.keys())
#        if not file_exists:
#            writer.writeheader()
#        writer.writerow(data)

# Function to save data to JSON
def save_to_json(data):
    if not os.path.isfile(json_file_path):
        with open(json_file_path, 'w') as file:
            json.dump([], file)
    with open(json_file_path, 'r+') as file:
        file_data = json.load(file)
        file_data.append(data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

# Function to save data to MSSQL
#def save_to_mssql(data):
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fingerprints (ip, referrer, currentUrl, userAgent, appName, appVersion, languages, colorDepth, deviceMemory, hardwareConcurrency, screenResolution, timezoneOffset, plugins, canvasFingerprint, webglFingerprint, renderer, audioFingerprint, touchSupport, screenOrientation, cookieEnabled, doNotTrack, battery, networkInfo, geolocation, localStorage, sessionStorage, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['ip'], data['referrer'], data['currentUrl'], data['userAgent'], data['appName'], data['appVersion'], ','.join(data['languages']),
            data['colorDepth'], data['deviceMemory'], data['hardwareConcurrency'], ','.join(map(str, data['screenResolution'])), data['timezoneOffset'],
            ','.join(data['plugins']), data['canvasFingerprint'], ','.join(map(str, data['webglFingerprint'])), data['renderer'], ','.join(map(str, data['audioFingerprint'])),
            data['touchSupport'], data['screenOrientation'], data['cookieEnabled'], data['doNotTrack'], json.dumps(data['battery']), json.dumps(data['networkInfo']),
            json.dumps(data['geolocation']), json.dumps(data['localStorage']), json.dumps(data['sessionStorage']), datetime.now()
        ))
        conn.commit()
    except Exception as e:
        print(f"Error saving to MSSQL: {e}")
    finally:
        conn.close()

# Endpoint to collect fingerprints
@app.route('/collect', methods=['POST'])
def collect():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Get the client's IP address
        data['ip'] = request.remote_addr

        # Save data
#        save_to_csv(data)
        save_to_json(data)
#        save_to_mssql(data)

        return jsonify({'message': 'Fingerprint collected'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve the index page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
