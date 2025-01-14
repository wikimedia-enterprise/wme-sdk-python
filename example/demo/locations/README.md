# GeoSearch Wiki Map Application

This project is a web application that allows users to search for a location by name, zoom into the map, and display nearby Wikipedia articles. It uses the following services:
- **OpenCage** for geolocation (converting place names into latitude and longitude).
- **Wikipedia API** for fetching articles near a specific latitude and longitude.
- **Wikimedia Enterprise API** to populate detailed Wikipedia infobox data when hovering over map pins.

## Features:
1. Search for a location using the search box.
2. Zoom into the selected location.
3. Display Wikipedia articles as pins on the map within a certain radius of the selected location.
4. Hover over map pins to see infobox details and images from Wikimedia Enterprise.

![screenshot of 15 Central Park West](image-1.png)

### 1. Run the Web Server:
After the dependencies are installed, you can start the web server by running:

```bash
cd locations
python app.py
```

### 2. Open the Application in Your Browser:
Open your browser and go to the following URL:

```bash
http://127.0.0.1::8000/
```

## How the Application Works:
- **Search Box**: Type the name of a location in the search box. The application will use the OpenCage API to suggest places based on the input.
- **Zoom to Location**: Once you select a location, the map will automatically zoom in to that place and display Wikipedia articles as map pins around it.
- **Article Pins**: Each pin on the map represents a Wikipedia article. Clicking a pin opens a popup with the article title and a link to the Wikipedia page.
- **Infobox Details**: Hover over any pin to fetch and display infobox details such as the article's image, key facts, and other related data. (Note: Not all Wikipedia articles have infoboxes, so some articles may not display details in the right panel.)

## API Integrations:
1. **OpenCage API**: Used for geolocation and place name suggestions based on user input.
2. **Wikipedia API**: Used to fetch nearby Wikipedia articles given a latitude and longitude.
3. **Wikimedia Enterprise API**: Used to fetch detailed infobox data when hovering over pins.

## Troubleshooting:
1. **Invalid API Keys**: Ensure you have valid API keys in the `.env` file for both OpenCage and Wikimedia Enterprise.
2. **Environment Issues**: If you have trouble with dependencies or activating the virtual environment, make sure that Python and `pip` are installed correctly on your system.
3. **Missing Infoboxes**: Not all Wikipedia articles have infoboxes, so the right panel may not update for some pins.

## License:
This project is licensed under the MIT License.
