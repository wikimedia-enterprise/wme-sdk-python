# pylint: disable=R0801,C0103,W0621, W0718, R0914, R0915, W0611

"""
Serves a web application for finding and displaying Wikimedia infoboxes,
using the official WME API Client SDK.
"""

import os
import json
from pathlib import Path
from contextlib import asynccontextmanager
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

# --- Import SDK Modules ---
from modules.auth.auth_client import AuthClient
from modules.auth.helper import Helper
from modules.api.api_client import Client, Request as ApiRequest, API
from modules.api.structuredcontent import StructuredContent
from modules.api.exceptions import APIRequestError, APIStatusError, APIDataError, DataModelError

load_dotenv()

# --- Globals ---
USERNAME = os.getenv("WME_USERNAME")
PASSWORD = os.getenv("WME_PASSWORD")
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

APP_ROOT = Path(__file__).parent

# --- Application Lifespan (Startup/Shutdown) ---

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Manages the application's lifecycle.
    On startup: Creates an HTTP client for non-SDK calls,
                and initializes the SDK's Auth Helper and API Client.
    On shutdown: Closes clients and stops the auth helper.
    """
    # 1. Client for non-SDK calls (OpenCage, Wikipedia Geosearch)
    _app.state.http_client = httpx.AsyncClient()

    # 2. SDK Auth and API Clients
    def sync_sdk_startup():
        """Initializes and returns SDK components."""
        print("Initializing SDK AuthClient and Helper...")
        auth_client = AuthClient()
        helper = Helper(auth_client)
        api_client = Client()

        token = helper.get_access_token()
        api_client.set_access_token(token)
        print("SDK Auth Helper and API Client are initialized and ready.")
        return auth_client, helper, api_client

    auth_client, helper, api_client = await run_in_threadpool(sync_sdk_startup)

    _app.state.auth_client = auth_client
    _app.state.helper = helper
    _app.state.api_client = api_client

    # App starts and runs here
    yield

    # --- Shutdown Logic ---
    print("Shutting down...")
    await _app.state.http_client.aclose()
    print("External HTTP client closed.")

    def sync_sdk_shutdown():
        """Stops the auth helper thread."""
        if _app.state.helper:
            print("Stopping SDK Auth Helper thread...")
            _app.state.helper.stop()
            print("Auth Helper stopped.")

    await run_in_threadpool(sync_sdk_shutdown)

app = FastAPI(lifespan=lifespan)

# --- Template and Static File Setup ---
templates = Jinja2Templates(directory=APP_ROOT / "templates")
app.mount("/static", StaticFiles(directory=APP_ROOT / "static"), name="static")


# --- API Endpoints ---

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Serves the main HTML application page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/geocode")
async def geocode(request: Request, location: str = Query(..., description="Location to geocode")):
    """Geocodes a location string using the OpenCage Data API."""

    http_client = request.app.state.http_client
    url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={OPENCAGE_API_KEY}"

    try:
        response = await http_client.get(url, timeout=10)
        response.raise_for_status()
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

    except httpx.HTTPStatusError as http_err:
        print(f"OpenCage HTTP error: {http_err} - {http_err.response.text}")
        return JSONResponse(
            content={"error": "Failed to geocode", "details": http_err.response.text},
            status_code=http_err.response.status_code
        )
    except httpx.RequestError as req_err:
        print(f"OpenCage connection error: {req_err}")
        return JSONResponse(
            content={"error": "Failed to connect to geocoding service", "details": str(req_err)},
            status_code=503
        )


@app.get("/wikipedia")
async def wikipedia(request: Request, lat: float, lng: float):
    """Finds Wikipedia articles near a given latitude and longitude."""

    http_client = request.app.state.http_client
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gscoord={lat}|{lng}&gsradius=10000&gslimit=1000&format=json"

    response = None
    try:
        response = await http_client.get(
            url,
            timeout=10,
            headers={"User-Agent": "DemoLocationsWebApp (myemail@example.com)"}
        )
        response.raise_for_status()
        return JSONResponse(content=response.json())

    except httpx.HTTPStatusError as http_err:
        details = str(http_err)
        status = 500
        if response:
            details = response.text
            status = response.status_code
            print(f"Wikipedia HTTP error: {http_err} - {details}")
        return JSONResponse(
            content={"error": "Failed to fetch from Wikipedia", "details": details},
            status_code=status
        )
    except json.JSONDecodeError:
        details = response.text if response else "No response"
        print(f"Invalid JSON from Wikipedia: {details}")
        return JSONResponse(content={"error": "Invalid data from Wikipedia", "details": details}, status_code=500)

    except httpx.RequestError as req_err:
        print(f"Wikipedia connection error: {req_err}")
        return JSONResponse(content={"error": "Failed to connect to Wikipedia", "details": str(req_err)}, status_code=503)

@app.get("/infobox")
async def get_infobox(request: Request, title: str):
    """Fetches structured infobox data using the SDK, handling auth."""

    api_client: API = request.app.state.api_client
    helper: Helper = request.app.state.helper

    if not helper:
        return JSONResponse(content={"error": "Not authenticated"}, status_code=500)

    filters = {
            "is_part_of.identifier": "enwiki"
        }

    sdk_request = ApiRequest(
        fields=["name", "url", "infoboxes"],
        filters=filters
    )

    try:
        def sync_api_call():
            token = helper.get_access_token()
            api_client.set_access_token(token)

            return api_client.get_structured_contents(title, sdk_request)

        structured_contents = await run_in_threadpool(sync_api_call)

        if structured_contents:
            response_data = [StructuredContent.to_json(sc) for sc in structured_contents]
            return JSONResponse(content=response_data)

        return JSONResponse(content=[], status_code=404)

    except (APIRequestError, APIStatusError, APIDataError, DataModelError) as e:
        print(f"SDK Error: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return JSONResponse(content={"error": "An unexpected error occurred"}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
