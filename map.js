
// Initialize map
const map = L.map('map').setView([9.145, 40.4897], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

let pickupMarker = null;
let deliveryMarker = null;

function calculateEstimatedPrice() {
    const weight = parseFloat(document.getElementById('weight').value) || 0;
    
    if (!pickupMarker || !deliveryMarker || weight <= 0) {
        document.getElementById('estimated_price').value = '';
        return;
    }
    
    const distance = pickupMarker.getLatLng().distanceTo(deliveryMarker.getLatLng()) / 1000; // in km
    
    // Basic price calculation: (base price + (distance * rate) + (weight * rate))
    const basePrice = 100; // ETB
    const distanceRate = 10; // ETB per km
    const weightRate = 5; // ETB per kg
    
    const estimatedPrice = basePrice + (distance * distanceRate) + (weight * weightRate);
    document.getElementById('estimated_price').value = Math.round(estimatedPrice);
}

// Update price when weight changes
document.getElementById('weight').addEventListener('input', calculateEstimatedPrice);

// Handle map clicks
map.on('click', function(e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    // Reverse geocoding using Nominatim
    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
        .then(response => response.json())
        .then(data => {
            const address = data.display_name;
            
            // Determine which input to update based on which was last focused
            const activeInput = document.activeElement;
            if (activeInput.id === 'pickup_location' || !pickupMarker) {
                if (pickupMarker) map.removeLayer(pickupMarker);
                pickupMarker = L.marker([lat, lng], {
                    icon: L.divIcon({className: 'pickup-marker', html: '📍'})
                }).addTo(map);
                document.getElementById('pickup_location').value = address;
            } else {
                if (deliveryMarker) map.removeLayer(deliveryMarker);
                deliveryMarker = L.marker([lat, lng], {
                    icon: L.divIcon({className: 'delivery-marker', html: '🎯'})
                }).addTo(map);
                document.getElementById('delivery_location').value = address;
            }

            calculateEstimatedPrice();
        });
});

// Focus handlers for location inputs
document.getElementById('pickup_location').addEventListener('focus', function() {
    this.select();
});

document.getElementById('delivery_location').addEventListener('focus', function() {
    this.select();
});
