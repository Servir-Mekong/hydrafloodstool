mapboxgl.accessToken = 'pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ';
    
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
document.getElementById('usecase1').addEventListener('click', () => {
    // Fly to a random location by offsetting the point -74.50, 40
    // by up to 5 degrees.
    map.flyTo({
        center: [104.9249267578125, 11.549998444541838],
        essential: true,
        zoom: 8
    });
});

map.on('load', () => {
    //Get Daily Surface Water Area Layer
    var selected_date = '2021-10-25';
    $.ajax({
        url: '/ajax/surfacewatermap/',
        type: "GET",
        data: {
            "selected_date": selected_date,
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            getDailySurWater = data;
            var dailySurfaceWater = getDailySurWater;        
            map.addSource('surfacewater', {
                'type': 'raster',
                'tiles': [
                    dailySurfaceWater
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'surfacewater', // Layer ID
                'type': 'raster',
                'source': 'surfacewater', // ID of the tile source created above
                'layout': {
                    // Make the layer visible by default.
                    'visibility': 'visible'
                },
            });
        },
        error: (error) => {
            console.log(error);
        }
    });
});

document.getElementById('usecase2').addEventListener('click', () => {
    // Fly to a random location by offsetting the point -74.50, 40
    // by up to 5 degrees.
    map.flyTo({
        center: [101.68533325195312, 15.489746308990687],
        essential: true,
        zoom: 8
    });
    map.removeLayer('surfacewater');
    map.removeSource('surfacewater');
    //Get Daily Surface Water Area Layer
    var selected_date = '2021-09-27';
    $.ajax({
        url: '/ajax/surfacewatermap/',
        type: "GET",
        data: {
            "selected_date": selected_date,
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            getDailySurWater = data;
            var dailySurfaceWater = getDailySurWater;        
            map.addSource('surfacewater', {
                'type': 'raster',
                'tiles': [
                    dailySurfaceWater
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'surfacewater', // Layer ID
                'type': 'raster',
                'source': 'surfacewater', // ID of the tile source created above
                'layout': {
                    // Make the layer visible by default.
                    'visibility': 'visible'
                },
            });
        },
        error: (error) => {
            console.log(error);
        }
    });  
});

document.getElementById('usecase3').addEventListener('click', () => {
    // Fly to a random location by offsetting the point -74.50, 40
    // by up to 5 degrees.
    map.flyTo({
        center: [109.13749694824219, 13.874746422868933],
        essential: true,
        zoom: 10
    });
    map.removeLayer('surfacewater');
    map.removeSource('surfacewater');
    //Get Daily Surface Water Area Layer
    var selected_date = '2021-11-30';
    $.ajax({
        url: '/ajax/surfacewatermap/',
        type: "GET",
        data: {
            "selected_date": selected_date,
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            getDailySurWater = data;
            var dailySurfaceWater = getDailySurWater;        
            map.addSource('surfacewater', {
                'type': 'raster',
                'tiles': [
                    dailySurfaceWater
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'surfacewater', // Layer ID
                'type': 'raster',
                'source': 'surfacewater', // ID of the tile source created above
                'layout': {
                    // Make the layer visible by default.
                    'visibility': 'visible'
                },
            });
        },
        error: (error) => {
            console.log(error);
        }
    });  
});