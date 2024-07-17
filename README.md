-------------------
# Fingerprint-json


The index.html will load, collect the fingerprint data, send it to the Flask server, and then redirect to the desired url (here ex: Google.com). 
The collected data will be recorded in fingerprints.json.
After starting the Flask app, navigate to http://localhost:8080 or (Server-IP:8080) in your browser. 

### Folder Structure:
    Main
    ├── app.py
    ├── fingerprints.log
    ├── requirements.txt
    │
    ├── static
    │   └── js
    │      └── fingerprint.js
    │
    ├── templates
    │    └── index.html
    │
    ├── data    
         └── fingerprints.json

### Deploy:

1. Clone Repo
```
git clone https://github.com/alwazw/Fingerprint-json
```

2. Install Dependencies:
``` bash
sudo apt update && sudo apt install python3 python3-pip
pip install -r requirements.txt
```

3. Run app.py
``` python
python3 app.py
```

4. In your web browser, visit:
```
http://localhost:8080
```

5. Export 
JSON located main/data/fingerprints.json
