let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.82175240259666, lng: -73.9472882429056 },
    zoom: 8,
  });
}

window.initMap = initMap;
