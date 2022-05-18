mapboxgl.accessToken = 'pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ';

var umap01 = new mapboxgl.Map({
    container: 'umap-01', // container ID
    style: 'mapbox://styles/mapbox/light-v10', // style URL
    center: [104.9999267578125, 11.549998444541838], // starting position [lng, lat]
    zoom: 8 // starting zoom
});
// disable map zoom when using scroll
umap01.scrollZoom.disable();

var umap02 = new mapboxgl.Map({
    container: 'umap-02', // container ID
    style: 'mapbox://styles/mapbox/light-v10', // style URL
    center: [101.89476013183594, 15.629649494336572], // starting position [lng, lat]
    zoom: 10 // starting zoom
});
// disable map zoom when using scroll
umap02.scrollZoom.disable();

var umap03 = new mapboxgl.Map({
    container: 'umap-03', // container ID
    style: 'mapbox://styles/mapbox/light-v10', // style URL
    center: [109.20890808105469, 13.895410435207733], // starting position [lng, lat]
    zoom: 10 // starting zoom
});
// disable map zoom when using scroll
umap03.scrollZoom.disable();

// Create a function to get unique feature
function getUniqueFeatures(features, comparatorProperty) {
    const uniqueIds = new Set();
    const uniqueFeatures = [];
    for (const feature of features) {
        const id = feature.properties[comparatorProperty];
        if (!uniqueIds.has(id)) {
            uniqueIds.add(id);
            uniqueFeatures.push(feature);
        }
    }
    return uniqueFeatures;
}

// Create a popup, but don't add it to the map yet.
const popup = new mapboxgl.Popup({
    closeButton: false
});

// Case 01 Flood Map
umap01.on('load', () => {
    //JRC Permanent Water Map
    $.ajax({
        url: '/ajax/jrcpermanentwatermap/',
        type: "GET",
        dataType: 'json',
        async: false,
        success: (data) => {
            var getPermanentWater = data;        
            umap01.addSource('jrcpermanentwater', {
                'type': 'raster',
                'tiles': [
                    getPermanentWater 
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            umap01.addLayer({
                'id': 'jrcpermanentwater', // Layer ID
                'type': 'raster',
                'source': 'jrcpermanentwater', // ID of the tile source created above
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

    var uc_01_date = '2021-10-25';
    $.ajax({
        url: '/ajax/casefloodmap/',
        type: "GET",
        data: {
            "selected_date": uc_01_date,
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            var getFloodWaterMap = data;    
            umap01.addSource('floodwater', {
                'type': 'raster',
                'tiles': [
                    getFloodWaterMap
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            umap01.addLayer({
                'id': 'floodewater', // Layer ID
                'type': 'raster',
                'source': 'floodwater', // ID of the tile source created above
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

    // // District layer
    // umap01.addSource('u01adm2-src', {
    //     type: 'geojson',
    //     data: '/static/data/uc1.geojson' 
    // });
    // umap01.addLayer({
    //     'id': 'u01adm2',
    //     'type': 'fill',
    //     'source': 'u01adm2-src',
    //     'minzoom': 8,
    //     'maxzoom': 20,
    //     'layout': {
    //         'visibility': 'visible',
    //     },
    //     'paint': {
    //         'fill-color': 'transparent',
    //         'fill-opacity': 1.0,
    //         'fill-outline-color': '#000'
    //     }
    // });
    // // umap01.addLayer({
    // //     'id': 'u01adm22',
    // //     'type': 'line',
    // //     'source': 'u01adm2-src',
    // //     'minzoom': 8,
    // //     'maxzoom': 20,
    // //     'layout': {
    // //         'visibility': 'visible',
    // //     },
    // //     'paint': {
    // //         'line-color': '#000',
    // //         'line-width': 2
    // //     }
    // // });
    // umap01.addLayer({
    //     'id': 'u01adm2-highlighted',
    //     'type': 'line',
    //     'source': 'u01adm2-src',
    //     'minzoom': 8,
    //     'maxzoom': 20,
    //     'paint': {
    //         'line-color': '#191970',
    //         'line-width': 2
    //     },
    //     'filter': ['in', 'NAME_2', '']
    // });

    // umap01.on('mousemove', 'u01adm2', (e) => {
    //     // Change the cursor style as a UI indicator.
    //     umap01.getCanvas().style.cursor = 'pointer';
         
    //     // Use the first found feature.
    //     const feature = e.features[0];
         
    //     // Add features with the same county name
    //     // to the highlighted layer.
    //     umap01.setFilter('u01adm2-highlighted', [
    //         'in',
    //         'NAME_2',
    //         feature.properties.NAME_2
    //     ]);
         
    //     // Display a popup with the name of the county.
    //     var district = e.features[0].properties.NAME_2;
    //     var province = e.features[0].properties.NAME_1;
    //     var country = e.features[0].properties.NAME_0;
    
    //     popup
    //     .setLngLat(e.lngLat)
    //     .setHTML('<h6 style="margin-top: 10px; font-weight: bold; margin-bottom: 5px;">'+district+', '+province+', '+country+'</h6>')
    //     .addTo(umap01);
    // });
         
    // umap01.on('mouseleave', 'u01adm2', () => {
    //     umap01.getCanvas().style.cursor = '';
    //     popup.remove();
    //     umap01.setFilter('u01adm2-highlighted', ['in', 'NAME_2', '']);
    // });
});

 // Case 02 Flood Map
umap02.on('load', () => {
    //JRC Permanent Water Map
    $.ajax({
        url: '/ajax/jrcpermanentwatermap/',
        type: "GET",
        dataType: 'json',
        async: false,
        success: (data) => {
            var getPermanentWater = data;        
            umap02.addSource('jrcpermanentwater', {
                'type': 'raster',
                'tiles': [
                    getPermanentWater 
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            umap02.addLayer({
                'id': 'jrcpermanentwater', // Layer ID
                'type': 'raster',
                'source': 'jrcpermanentwater', // ID of the tile source created above
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

    var uc_02_date = '2021-09-27';
    $.ajax({
        url: '/ajax/casefloodmap/',
        type: "GET",
        data: {
            "selected_date": uc_02_date,
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            var getFloodWaterMap = data;    
            umap02.addSource('floodwater', {
                'type': 'raster',
                'tiles': [
                    getFloodWaterMap
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            umap02.addLayer({
                'id': 'floodewater', // Layer ID
                'type': 'raster',
                'source': 'floodwater', // ID of the tile source created above
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

    // // District layer
    // umap02.addSource('u02adm2-src', {
    //     type: 'geojson',
    //     data: '/static/data/uc2.geojson' 
    // });
    // umap02.addLayer({
    //     'id': 'u02adm2',
    //     'type': 'fill',
    //     'source': 'u02adm2-src',
    //     'minzoom': 8,
    //     'maxzoom': 20,
    //     'layout': {
    //         'visibility': 'visible',
    //     },
    //     'paint': {
    //         'fill-color': 'transparent',
    //         'fill-opacity': 1.0,
    //         'fill-outline-color': '#000'
    //     }
    // });
    // // umap02.addLayer({
    // //     'id': 'u02adm22',
    // //     'type': 'line',
    // //     'source': 'u02adm2-src',
    // //     'minzoom': 8,
    // //     'maxzoom': 20,
    // //     'layout': {
    // //         'visibility': 'visible',
    // //     },
    // //     'paint': {
    // //         'line-color': '#000',
    // //         'line-width': 2
    // //     }
    // // });
    // umap02.addLayer({
    //     'id': 'u02adm2-highlighted',
    //     'type': 'line',
    //     'source': 'u02adm2-src',
    //     'minzoom': 8,
    //     'maxzoom': 20,
    //     'paint': {
    //         'line-color': '#191970',
    //         'line-width': 2
    //     },
    //     'filter': ['in', 'NAME_2', '']
    // });

    // umap02.on('mousemove', 'u02adm2', (e) => {
    //     // Change the cursor style as a UI indicator.
    //     umap02.getCanvas().style.cursor = 'pointer';
         
    //     // Use the first found feature.
    //     const feature = e.features[0];
         
    //     // Add features with the same county name
    //     // to the highlighted layer.
    //     umap02.setFilter('u02adm2-highlighted', [
    //         'in',
    //         'NAME_2',
    //         feature.properties.NAME_2
    //     ]);
         
    //     // Display a popup with the name of the county.
    //     var district = e.features[0].properties.NAME_2;
    //     var province = e.features[0].properties.NAME_1;
    //     var country = e.features[0].properties.NAME_0;
    
    //     popup
    //     .setLngLat(e.lngLat)
    //     .setHTML('<h6 style="margin-top: 10px; font-weight: bold; margin-bottom: 5px;">'+district+', '+province+', '+country+'</h6>')
    //     .addTo(umap02);
    // });
         
    // umap02.on('mouseleave', 'u02adm2', () => {
    //     umap02.getCanvas().style.cursor = '';
    //     popup.remove();
    //     umap02.setFilter('u02adm2-highlighted', ['in', 'NAME_2', '']);
    // });
});

// Case 03 Flood Map
umap03.on('load', () => {
    //JRC Permanent Water Map
    $.ajax({
        url: '/ajax/jrcpermanentwatermap/',
        type: "GET",
        dataType: 'json',
        async: false,
        success: (data) => {
            var getPermanentWater = data;        
            umap03.addSource('jrcpermanentwater', {
                'type': 'raster',
                'tiles': [
                    getPermanentWater 
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            umap03.addLayer({
                'id': 'jrcpermanentwater', // Layer ID
                'type': 'raster',
                'source': 'jrcpermanentwater', // ID of the tile source created above
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

    var uc_03_date = '2021-11-30';
    $.ajax({
        url: '/ajax/casefloodmap/',
        type: "GET",
        data: {
            "selected_date": uc_03_date,
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            var getFloodWaterMap = data;    
            umap03.addSource('floodwater', {
                'type': 'raster',
                'tiles': [
                    getFloodWaterMap
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            umap03.addLayer({
                'id': 'floodewater', // Layer ID
                'type': 'raster',
                'source': 'floodwater', // ID of the tile source created above
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

    // // District layer
    // umap03.addSource('u03adm2-src', {
    //     type: 'geojson',
    //     data: '/static/data/uc3.geojson' 
    // });
    // umap03.addLayer({
    //     'id': 'u03adm2',
    //     'type': 'fill',
    //     'source': 'u03adm2-src',
    //     'minzoom': 8,
    //     'maxzoom': 20,
    //     'layout': {
    //         'visibility': 'visible',
    //     },
    //     'paint': {
    //         'fill-color': 'transparent',
    //         'fill-opacity': 1.0,
    //         'fill-outline-color': '#000'
    //     }
    // });
    // // umap03.addLayer({
    // //     'id': 'u03adm22',
    // //     'type': 'line',
    // //     'source': 'u03adm2-src',
    // //     'minzoom': 8,
    // //     'maxzoom': 20,
    // //     'layout': {
    // //         'visibility': 'visible',
    // //     },
    // //     'paint': {
    // //         'line-color': '#000',
    // //         'line-width': 2
    // //     }
    // // });
    // umap03.addLayer({
    //     'id': 'u03adm2-highlighted',
    //     'type': 'line',
    //     'source': 'u03adm2-src',
    //     'minzoom': 8,
    //     'maxzoom': 20,
    //     'paint': {
    //         'line-color': '#191970',
    //         'line-width': 2
    //     },
    //     'filter': ['in', 'NAME_2', '']
    // });

    // umap03.on('mousemove', 'u03adm2', (e) => {
    //     // Change the cursor style as a UI indicator.
    //     umap03.getCanvas().style.cursor = 'pointer';
         
    //     // Use the first found feature.
    //     const feature = e.features[0];
         
    //     // Add features with the same county name
    //     // to the highlighted layer.
    //     umap03.setFilter('u03adm2-highlighted', [
    //         'in',
    //         'NAME_2',
    //         feature.properties.NAME_2
    //     ]);
         
    //     // Display a popup with the name of the county.
    //     var district = e.features[0].properties.NAME_2;
    //     var province = e.features[0].properties.NAME_1;
    //     var country = e.features[0].properties.NAME_0;
    
    //     popup
    //     .setLngLat(e.lngLat)
    //     .setHTML('<h6 style="margin-top: 10px; font-weight: bold; margin-bottom: 5px;">'+district+', '+province+', '+country+'</h6>')
    //     .addTo(umap03);
    // });
         
    // umap03.on('mouseleave', 'u03adm2', () => {
    //     umap03.getCanvas().style.cursor = '';
    //     popup.remove();
    //     umap03.setFilter('u03adm2-highlighted', ['in', 'NAME_2', '']);
    // });
});

