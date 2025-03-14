from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import requests
import os

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

access_token = None

# Login to Wikimedia API
def login_to_wikimedia():
    global access_token
    login_url = "https://auth.enterprise.wikimedia.com/v1/login"

    response = requests.post(
        login_url,
        data={"username": USERNAME, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Successfully logged in!")
    else:
        print(f"Failed to log in to Wikimedia API: {response.status_code}")
        print(response.text)

# Perform login at startup
login_to_wikimedia()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/geocode")
async def geocode(location: str = Query(..., description="Location to geocode")):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"
    response = requests.get(url)
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
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}|{lng}&gsradius=10000&gslimit=1000&format=json"
    response = requests.get(url)
    return JSONResponse(content=response.json())

@app.get("/infobox")
async def get_infobox(title: str):
    url = f"https://api.enterprise.wikimedia.com/v2/structured-contents/{title}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "fields": ["name", "url", "infoboxes"],
        "filters": [{"field": "is_part_of.identifier", "value": "enwiki"}],
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return JSONResponse(content=response.json())
    return JSONResponse(content={"error": "Failed to fetch infobox data"}, status_code=response.status_code)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
