// Initialize the tracking map
const trackingMap = L.map('tracking-map').setView([9.145, 40.4897], 6);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(trackingMap);

let currentMarker = null;
let path = L.polyline([], {color: 'blue'}).addTo(trackingMap);

// Function to update location on map
function updateLocation() {
    fetch(`/api/location/latest/${bookingId}`)
        .then(response => response.json())
        .then(data => {
            if (data.latitude && data.longitude) {
                const position = [data.latitude, data.longitude];
                
                // Update or create marker
                if (currentMarker) {
                    currentMarker.setLatLng(position);
                } else {
                    currentMarker = L.marker(position).addTo(trackingMap);
                }
                
                // Add point to path
                path.addLatLng(position);
                
                // Center map on current position
                trackingMap.setView(position);
            }
        });
}

// Update location every 30 seconds
setInterval(updateLocation, 30000);

// Initial location update
updateLocation();
