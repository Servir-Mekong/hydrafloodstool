mapboxgl.accessToken = 'pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t0bG1qMnJ5MDh0YzJ3czRiOHB1dXVwZiJ9.RHfxuNLtYaycA39uKjhARw';
    
var sidebar = document.getElementById("sidebar"); 
var sidenavOpen = document.getElementById("open-sidebar"); 
var sidenavClose = document.getElementById("close-sidebar"); 
var sidebarContent = document.getElementById("sidebar-content");

var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [100.523186, 15.736717], // starting position [lng, lat]
    zoom: 5 // starting zoom
});

function displaySidebar(){
    if (sidebarContent.style.display === "none") {
    sidebarContent.style.display = "block";
    sidebarContent.style.width = "350px";
    sidebar.style.marginLeft = "350px";
    sidenavOpen.style.display = "none"; 
    sidenavClose.style.display = "block";
    } else {
    sidebarContent.style.display = "none";
    sidebar.style.marginLeft = 0;
    sidenavOpen.style.display = "block"; 
    sidenavClose.style.display = "none";
    }
};

sidenavOpen.addEventListener("click", displaySidebar);
sidenavClose.addEventListener("click", displaySidebar);

// Add the geocoding control to the map.
map.addControl(
    new MapboxGeocoder({
    accessToken: mapboxgl.accessToken,
    mapboxgl: mapboxgl
    })
);

// Add zoom and rotation controls to the map.
map.addControl(new mapboxgl.NavigationControl());

// Add geolocate control to the map.
map.addControl(
    new mapboxgl.GeolocateControl({
    positionOptions: {
    enableHighAccuracy: true
    },
    // When active the map will receive updates to the device's location as it changes.
    trackUserLocation: true,
    // Draw an arrow next to the location dot to indicate which direction the device is heading.
    showUserHeading: true
    })
);