from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
app = Flask(__name__)

auth_token = None

# WME Username and Password (get your account from https://dashboard.enterprise.wikimedia.com/signup/)
USERNAME = os.getenv('WME_USERNAME')
PASSWORD = os.getenv('WME_PASSWORD')

# OpenCage API key (get your own key from https://opencagedata.com/)
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')


# Login to Wikimedia API
def login_to_wikimedia():
    global access_token
    login_url = "https://auth.enterprise.wikimedia.com/v1/login"

    # Make the request with form data
    response = requests.request(
                    "POST",
                    login_url,
                    data={
                        'username': USERNAME,
                        'password': PASSWORD
                    },
                    headers={
                        'Content-Type': 'application/x-www-form-urlencoded'
                    })

    if response.status_code == 200:
        # Successfully logged in
        access_token = response.json().get('access_token')
        print("Successfully logged in!")
    else:
        # Handle failed login
        print(f"Failed to log in to Wikimedia API: {response.status_code}")
        print(response.text)  # Print the response body for debugging


# Call login at startup
login_to_wikimedia()


# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle the search input, returns geolocation from OpenCage API
@app.route('/geocode', methods=['GET'])
def geocode():
    location = request.args.get('location')
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Parse relevant results
    if data['results']:
        results = [{
            'formatted': result['formatted'],
            'lat': result['geometry']['lat'],
            'lng': result['geometry']['lng']
        } for result in data['results']]
        return jsonify(results)
    return jsonify([])


# Route to call Wikimedia API and fetch nearby articles based on coordinates
@app.route('/wikipedia', methods=['GET'])
def wikipedia():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    # Wikimedia API call for nearby articles
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}|{lng}&gsradius=10000&gslimit=1000&format=json"
    response = requests.get(url)
    return jsonify(response.json())


# Route to get infobox data
@app.route('/infobox', methods=['GET'])
def get_infobox():
    title = request.args.get('title')
    url = f"https://api.enterprise.wikimedia.com/v2/structured-contents/{title}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "fields": ["name", "url", "infobox"],
        "filters": [{"field": "is_part_of.identifier", "value": "enwiki"}],
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch infobox data"})


if __name__ == '__main__':
    app.run(debug=True)
