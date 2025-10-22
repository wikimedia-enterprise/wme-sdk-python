"""Serves a web application for finding and displaying Wikimedia infoboxes."""

import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

# Load environment variables
load_dotenv()

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# WME Username and Password (get your account from https://dashboard.enterprise.wikimedia.com/signup/)
USERNAME = os.getenv("WME_USERNAME")
PASSWORD = os.getenv("WME_PASSWORD")

# OpenCage API key (get your own key from https://opencagedata.com/)
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

ACCESS_TOKEN = None

# Login to Wikimedia API
def login_to_wikimedia():
    """Authenticates with the Wikimedia Enterprise API and stores the ACCESS TOKENACCESS_TOKEN.
    This function sends a POST request with the username and password from
    environment variables to the WME login endpoint. The resulting
    'ACCESS_TOKEN' is stored in the global `ACCESS_TOKEN` variable for use
    in subsequent API calls.

    This function is called once on application startup.
    """
    # pylint: disable=global-statement
    global ACCESS_TOKEN
    login_url = "https://auth.enterprise.wikimedia.com/v1/login"

    response = requests.post(
        login_url,
        data={"username": USERNAME, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )

    if response.status_code == 200:
        ACCESS_TOKEN = response.json().get("ACCESS_TOKEN")
        print("Successfully logged in!")
    else:
        print(f"Failed to log in to Wikimedia API: {response.status_code}")
        print(response.text)

# Perform login at startup
login_to_wikimedia()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serves the main HTML application page.

    This endpoint renders and returns the `index.html` template, which
    contains the client-side application.

    Args:
        request (Request): The incoming request object.

    Returns:
        HTMLResponse: The rendered HTML page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/geocode")
async def geocode(location: str = Query(..., description="Location to geocode")):
    """Geocodes a location string using the OpenCage Data API.

    Takes a text-based location and returns a list of potential matches,
    each containing the formatted name and its latitude/longitude coordinates.

    Args:
        location (str): The location name to search for (e.g., "Paris").

    Returns:
        JSONResponse: A list of matching locations or an empty list.
    """
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"
    response = requests.get(
        url,
        timeout=10)
    data = response.json()

    if data.get("results"):
        results = [
            {
                "formatted": result["formatted"],
                "lat": result["geometry"]["lat"],
                "lng": result["geometry"]["lng"],
            }
            for result in data["results"]
        ]
        return JSONResponse(content=results)
    return JSONResponse(content=[], status_code=200)

@app.get("/wikipedia")
async def wikipedia(lat: float, lng: float):
    """Finds Wikipedia articles near a given latitude and longitude.

    Uses the public Wikipedia API's 'geosearch' action to find articles
    within a 10km radius of the provided coordinates.

    Args:
        lat (float): The latitude.
        lng (float): The longitude.

    Returns:
        JSONResponse: The raw JSON response from the Wikipedia API.
    """
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}|{lng}&gsradius=10000&gslimit=1000&format=json"
    response = requests.get(
        url,
        timeout=10)
    return JSONResponse(content=response.json())

@app.get("/infobox")
async def get_infobox(title: str):
    """Fetches structured infobox data for a Wikipedia article title.

    This endpoint queries the Wikimedia Enterprise (WME) v2 API for the
    structured contents of a specific article. It uses the globally stored
    `ACCESS_TOKEN` for authentication.

    Args:
        title (str): The exact title of the Wikipedia article.

    Returns:
        JSONResponse: The structured content data on success, or an error
            message on failure.
    """
    url = f"https://api.enterprise.wikimedia.com/v2/structured-contents/{title}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "fields": ["name", "url", "infoboxes"],
        "filters": [{"field": "is_part_of.identifier", "value": "enwiki"}],
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        timeout=10
        )

    if response.status_code == 200:
        return JSONResponse(content=response.json())
    return JSONResponse(content={"error": "Failed to fetch infobox data"}, status_code=response.status_code)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
