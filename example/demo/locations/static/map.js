let map = L.map('map').setView([51.505, -0.09], 2);

// OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let markers = [];

// Function to add markers for Wikipedia articles
function addMarkers(data) {
    //markers.forEach(marker => map.removeLayer(marker));
    //markers = [];

    data.query.geosearch.forEach(article => {
        let marker = L.marker([article.lat, article.lon]).addTo(map)
            .bindPopup(`<b>${article.title}</b><br><a href="https://en.wikipedia.org/wiki/${article.title}" target="_blank">Read Article</a>`);

        // Handle mouseover event to fetch infobox data
        marker.on('mouseover', function() {
            fetchInfobox(article.title);
        });

        markers.push(marker);
    });
}

// Function to fetch infobox data and display it
function fetchInfobox(title) {
    title = title.replace(/ /g, '_'); // Replace spaces with underscores
    $.getJSON('/infobox', { title: title }, function(data) {
        if (!data) return;

        article = data[0]
        info = null
        if (article.infoboxes) {
            info = article.infoboxes[0]
        }

        renderInfobox(article.name, article.url, info);
    });
}

// Function to render the infobox HTML
function renderInfobox(name, url, infobox) {
    const infoboxContainer = document.getElementById('infobox'); // Add a div in HTML to display the infobox

    let html = '<div class="infobox-info">';
    html += `<h3><a href="${url}" target="_blank">${name}</a></h3>`;

    // Add the image
    if (infobox &&
        infobox.has_parts&&
        infobox.has_parts.length > 0) {

        // Add name-value pairs
        infobox.has_parts.forEach(section => {
            section.has_parts.forEach(part => {
                if (part.type && part.type === 'image') {
                    const imageUrl = part.images[0].content_url;
                    html += `<div><img src="${imageUrl}" style="width:220px;" onerror="this.outerHTML=''"/></div>`;
                }

                if (part.name && part.value) {
                    html += `<div><strong>${part.name}</strong>: ${part.value}</div>`;
                }
            });
        });
    } else {
        return; // Leave older infobox data in the page
    }

    html += '</div>';
    infoboxContainer.innerHTML = html;
}

// Function to handle zooming and centering when an li is clicked
$(document).on('click', '#suggestions a', function() {
    let lat = $(this).data('lat');
    let lng = $(this).data('lng');

    // Move map to the selected location and zoom in to city level (zoom level 15)
    map.setView([lat, lng], 15);

    // Fetch nearby Wikipedia articles (if you want to do that at the same time)
    $.getJSON('/wikipedia', { lat: lat, lng: lng }, function(data) {
        addMarkers(data);  // Function to add pins to the map (already defined)
    });

    // Clear the suggestions dropdown
    $('#suggestions').html('');
});

// Handle user input and auto-suggestions
$('#search-box').on('input', function() {
    let query = $(this).val();

    if (query.length < 3) return;

    $.getJSON('/geocode', { location: query }, function(data) {
        let suggestions = data.map(item =>
            `<div><a href="#" data-lat="${item.lat}" data-lng="${item.lng}">${item.formatted}</a></div>`
        );
        $('#suggestions').html(suggestions.join(''));
    });
});

// Add a double-click event listener to the map
map.on('dblclick', function(e) {
    // Get the latitude and longitude from the double-click event
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    // Center the map on the clicked location and zoom in
    //map.setView([lat, lng], 12);

    // Fetch nearby Wikipedia articles (if you want to do that at the same time)
    $.getJSON('/wikipedia', { lat: lat, lng: lng }, function(data) {
        addMarkers(data);  // Function to add pins to the map (already defined)
    });
});
