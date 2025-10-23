"""Serves a web application for finding and displaying Wikimedia infoboxes."""

import os
import json
import asyncio
from contextlib import asynccontextmanager
from starlette.datastructures import State
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

load_dotenv()

# --- Globals ---
USERNAME = os.getenv("WME_USERNAME")
PASSWORD = os.getenv("WME_PASSWORD")
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY")

# --- Application Lifespan (Startup/Shutdown) ---

@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Manages the application's lifecycle.
    On startup: Creates a client, logs in, and stores them in app.state.
    On shutdown: Closes the client.
    """
    _app.state.http_client = httpx.AsyncClient()

    _app.state.token_lock = asyncio.Lock()

    access_token, refresh_token = await login_to_wikimedia(_app.state.http_client)

    _app.state.access_token = access_token
    _app.state.refresh_token = refresh_token

    # yield separates the app's startup logic from it's shutdown logic.
    # When we hit yield, the function "pauses" and hands control back to FastAPI.
    # FastAPI then finishes starting the server and begins accepting web requests (like /geocode, /wikipedia, etc.).
    # Then, the application runs normally for its entire life while the lifespan function stays paused at this yield
    # When we stop the app, FastAPI gracefully shuts down telling the lifespan function to resume executing all the code after the yield
    yield


    await _app.state.http_client.aclose()
    print("HTTP client closed.")

app = FastAPI(lifespan=lifespan)

# --- Template and Static File Setup ---
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Authentication Functions ---

async def login_to_wikimedia(client: httpx.AsyncClient):
    """Authenticates and returns the access and refresh tokens."""
    login_url = "https://auth.enterprise.wikimedia.com/v1/login"

    try:
        response = await client.post(
            login_url,
            data={"username": USERNAME, "password": PASSWORD},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        access_token = data.get("access_token")
        refresh_token = data.get("refresh_token")

        if access_token and refresh_token:
            print("Successfully logged in and stored tokens!")
        else:
            print(f"Login successful, but tokens not found: {data}")

        return access_token, refresh_token

    except httpx.HTTPStatusError as http_err:
        print(f"Failed to log in to Wikimedia API: {http_err.response.status_code}")
        print(http_err.response.text)
    except httpx.RequestError as e:
        print(f"Failed to connect to Wikimedia login service: {e}")

    return None, None

async def refresh_wikimedia_token(state: State, old_access_token: str):
    """Uses the refresh token to get new tokens (task-safe)."""


    async with state.token_lock:
        if state.access_token != old_access_token:
            return True

        if not state.http_client:
            print("CRITICAL: HTTP_CLIENT is not initialized.")
            return False

        print("Token expired. Attempting to refresh...")
        refresh_url = "https://auth.enterprise.wikimedia.com/v1/refresh"

        try:
            response = await state.http_client.post(
                refresh_url,
                data={"refresh_token": state.refresh_token},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            state.access_token = data.get("access_token")
            state.refresh_token = data.get("refresh_token")

            if state.access_token and state.refresh_token:
                print("Successfully refreshed tokens!")
                return True
            print(f"Refresh failed, no tokens in response: {data}")
            return False

        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"CRITICAL: Failed to refresh token: {e}")

            if isinstance(e, httpx.HTTPStatusError):
                print(f"Response body: {e.response.text}")


            state.access_token = None
            state.refresh_token = None
            return False

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
        if response:
            print(f"Wikipedia HTTP error: {http_err} - {response.text}")
            return JSONResponse(
                content={"error": "Failed to fetch from Wikipedia", "details": response.text},
                status_code=response.status_code
            )
        return JSONResponse(content={"error": "Failed to fetch from Wikipedia", "details": str(http_err)}, status_code=500)

    except json.JSONDecodeError:
        if response:
            print(f"Invalid JSON from Wikipedia: {response.text}")
            return JSONResponse(content={"error": "Invalid data from Wikipedia", "details": response.text}, status_code=500)
        return JSONResponse(content={"error": "Invalid data from Wikipedia"}, status_code=500)

    except httpx.RequestError as req_err:
        print(f"Wikipedia connection error: {req_err}")
        return JSONResponse(content={"error": "Failed to connect to Wikipedia", "details": str(req_err)}, status_code=503)

@app.get("/infobox")
async def get_infobox(request: Request, title: str):
    """Fetches structured infobox data, handling token refresh."""

    state = request.app.state
    http_client = state.http_client

    if not state.refresh_token:
        return JSONResponse(content={"error": "Not authenticated"}, status_code=500)

    current_access_token = state.access_token
    url = f"https://api.enterprise.wikimedia.com/v2/structured-contents/{title}"
    headers = {
        "Authorization": f"Bearer {current_access_token}",
        "Content-Type": "application/json",
    }
    json_payload = {
        "fields": ["name", "url", "infoboxes"],
        "filters": [{"field": "is_part_of.identifier", "value": "enwiki"}],
    }

    response = await http_client.post(
        url, json=json_payload, headers=headers, timeout=10
    )

    # --- HANDLE EXPIRATION (401) ---
    if response.status_code == 401:

        refresh_success = await refresh_wikimedia_token(state, current_access_token)

        if refresh_success:
            print("Retrying request with new token...")
            headers["Authorization"] = f"Bearer {state.access_token}"

            response = await http_client.post(
                url, json=json_payload, headers=headers, timeout=10
            )
        else:
            return JSONResponse(content={"error": "Token refresh failed"}, status_code=503)

    # --- FINAL RESPONSE HANDLING ---
    if response.status_code == 200:
        return JSONResponse(content=response.json())

    details = ""
    status = 500

    if response:
        details = response.text
        status = response.status_code

    return JSONResponse(
        content={"error": "Failed to fetch infobox data", "details": details},
        status_code=status
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
