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
map.on('style.load', () => {
    // Country layer
    map.addSource('adm0-src', {
        type: 'geojson',
        data: '/static/data/adm0.geojson'
    });
    map.addLayer({
        'id': 'adm0',
        // 'type': 'fill',
        'type': 'line',
        'source': 'adm0-src',
        'minzoom': 0,
        'maxzoom': 6,
        'layout': {
            'visibility': 'visible',
        },
        // 'paint': {
        //     'fill-color': 'transparent',
        //     'fill-opacity': 1.0,
        //     'fill-outline-color': 'rgba(200, 230, 201, 1)'
        // }
        'paint': {
            'line-color': '#756bb1',
            'line-width': 1.5
        },
    });
    map.addLayer({
        'id': 'adm0-highlighted',
        'type': 'line',
        'source': 'adm0-src',
        'minzoom': 0,
        'maxzoom': 6,
        'paint': {
            'line-color': '#636363',
            'line-width': 2
        },
        'filter': ['in', 'NAME_0', '']
    });

    // Province layer
    map.addSource('adm1-src', {
        type: 'geojson',
        data: '/static/data/adm1.geojson'  
    });
    map.addLayer({
        'id': 'adm1',
        'type': 'fill',
        'source': 'adm1-src',
        'minzoom': 6,
        'maxzoom': 8,
        'layout': {
            'visibility': 'visible',
        },
        'paint': {
            'fill-color': 'transparent',
            'fill-opacity': 1.0,
            'fill-outline-color': '#636363'
        }
    });
    map.addLayer({
        'id': 'adm1-highlighted',
        'type': 'line',
        'source': 'adm1-src',
        'minzoom': 6,
        'maxzoom': 8,
        'paint': {
            'line-color': '#636363',
            'line-width': 2
        },
        'filter': ['in', 'NAME_1', '']
    });
    map.addLayer({
        'id': 'adm11',
        'type': 'line',
        'source': 'adm1-src',
        'minzoom': 6,
        'maxzoom': 8,
        'paint': {
            'line-color': '#636363',
            'line-width': 0.75
        },
    });

    // District layer
    map.addSource('adm2-src', {
        type: 'geojson',
        data: '/static/data/adm2.geojson' 
    });
    map.addLayer({
        'id': 'adm2',
        'type': 'fill',
        'source': 'adm2-src',
        'minzoom': 8,
        'maxzoom': 20,
        'layout': {
            'visibility': 'visible',
        },
        'paint': {
            'fill-color': 'transparent',
            'fill-opacity': 1.0,
            'fill-outline-color': '#756bb1'
        }
    });
    map.addLayer({
        'id': 'adm2-highlighted',
        'type': 'line',
        'source': 'adm2-src',
        'minzoom': 8,
        'maxzoom': 20,
        'paint': {
            'line-color': '#636363',
            'line-width': 2
        },
        'filter': ['in', 'NAME_2', '']
    });
    map.addLayer({
        'id': 'adm22',
        'type': 'line',
        'source': 'adm2-src',
        'minzoom': 8,
        'maxzoom': 20,
        'paint': {
            'line-color': '#756bb1',
            'line-width': 0.75
        }
    });

    // Hospital layer
    map.loadImage(
        '/static/images/hospital.png',
        (error, image) => {
            if (error) throw error;
            map.addImage('custom-marker', image);
            // Add a GeoJSON source with 2 points
            map.addSource('hospital-src', {
                'type': 'geojson',
                'data': '/static/data/hospital.geojson'
            });
        
            // Add a symbol layer
            map.addLayer({
                'id': 'hospital',
                'type': 'symbol',
                'source': 'hospital-src',
                'minzoom': 10,
                'layout': {
                    'icon-image': 'custom-marker',
                    'icon-size': 0.03
                }
            });
        }
    );

    // Education layer
    map.loadImage(
        '/static/images/education.png',
        (error, image) => {
            if (error) throw error;
            map.addImage('education-marker', image);
            // Add a GeoJSON source
            map.addSource('education-src', {
                'type': 'geojson',
                'data': '/static/data/education.geojson'
            });
        
            // Add a symbol layer
            map.addLayer({
                'id': 'education',
                'type': 'symbol',
                'source': 'education-src',
                'minzoom': 10,
                'layout': {
                    'icon-image': 'education-marker',
                    'icon-size': 0.03
                }
            });
        }
    );

    map.on('mousemove', 'adm0', (e) => {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';
         
        // Use the first found feature.
        const feature = e.features[0];
         
        // Add features with the same county name
        // to the highlighted layer.
        map.setFilter('adm0-highlighted', [
            'in',
            'NAME_0',
            feature.properties.NAME_0
        ]);
         
        // Display a popup with the name of the county.
        popup
        .setLngLat(e.lngLat)
        .setText(feature.properties.NAME_0)
        .addTo(map);
    });
         
    map.on('mouseleave', 'adm0', () => {
        map.getCanvas().style.cursor = '';
        popup.remove();
        map.setFilter('adm0-highlighted', ['in', 'NAME_0', '']);
    });

    map.on('mousemove', 'adm1', (e) => {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';
         
        // Use the first found feature.
        const feature = e.features[0];
         
        // Add features with the same county name
        // to the highlighted layer.
        map.setFilter('adm1-highlighted', [
            'in',
            'NAME_0',
            feature.properties.NAME_1
        ]);
         
        // Display a popup with the name of the county.
        popup
        .setLngLat(e.lngLat)
        .setText(feature.properties.NAME_1)
        .addTo(map);
    });
         
    map.on('mouseleave', 'adm1', () => {
        map.getCanvas().style.cursor = '';
        popup.remove();
        map.setFilter('adm1-highlighted', ['in', 'NAME_1', '']);
    });

    map.on('mousemove', 'adm2', (e) => {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';
         
        // Use the first found feature.
        const feature = e.features[0];
         
        // Add features with the same county name
        // to the highlighted layer.
        map.setFilter('adm2-highlighted', [
            'in',
            'NAME_2',
            feature.properties.NAME_2
        ]);
         
        // Display a popup with the name of the county.
        var district = e.features[0].properties.NAME_2;
        var province = e.features[0].properties.NAME_1;
        var country = e.features[0].properties.NAME_0;
        var f_0_15 = e.features[0].properties.F_0_15;
        var f_15_65 = e.features[0].properties.F_15_65;
        var f_above_65 = e.features[0].properties.F__65;
        var f_total = f_0_15 + f_15_65 + f_above_65;
        var m_0_15 = e.features[0].properties.M_0_15;
        var m_15_65 = e.features[0].properties.M_15_65;
        var m_above_65 = e.features[0].properties.M__65;    
        var m_total = m_0_15+m_15_65+m_above_65;
        var hospitals = e.features[0].properties.Hospitals;
        var primary = e.features[0].properties.Primary;
        var secondary = e.features[0].properties.Secondary;
        var trunks = e.features[0].properties.Trunks;

        popup
        .setLngLat(e.lngLat)
        .setHTML('<h6 style="margin-top: 10px; font-weight: bold; margin-bottom: 5px;">'+district+': '+province+', '+country+'</h6>'+
        '<div class="table-responsive" style="line-height: 0.5">'+
            '<table class="table">'+
                '<thead>'+
                    '<tr>'+
                        '<th>'+"Population"+'</th>'+
                        '<th>'+"Female"+'</th>'+
                        '<th>'+"Male"+'</th>'+
                    '</tr>'+
                '</thead>'+
                '<tbody>' +
                    '<tr>'+
                        '<td>'+"Age 0-15"+'</td>'+
                        '<td>'+f_0_15+'</td>'+
                        '<td>'+m_0_15+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<td>'+"Age 15-65"+'</td>'+
                        '<td>'+f_15_65+'</td>'+
                        '<td>'+m_15_65+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<td>'+"Age >65"+'</td>'+
                        '<td>'+f_above_65+'</td>'+
                        '<td>'+m_above_65+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<th>'+"Total"+'</th>'+
                        '<th>'+f_total+'</th>'+
                        '<th>'+m_total+'</th>'+
                    '</tr>'+
                '</tbody>'+
                // '<thead>'+
                //     '<tr>'+
                //         '<th>'+"Health Facilities"+'</th>'+
                //         '<th>'+"No."+'</th>'+
                //         '<th>'+""+'</th>'+
                //     '</tr>'+
                // '</thead>'+
                '<tbody>'+
                    '<tr>'+
                        '<td>'+ "Hospitals" +'</td>'+
                        '<td>'+ hospitals +'</td>'+
                        '<td>'+""+'</td>'+
                    '</tr>'+
                '</tbody>'+
                '<thead>'+
                    '<tr>'+
                        '<th>'+"Roads"+'</th>'+
                        '<th>'+"No."+'</th>'+
                        '<th>'+""+'</th>'+
                    '</tr>'+
                '</thead>'+
                '<tbody>'+
                    '<tr>'+
                        '<td>'+ "Primary" +'</td>'+
                        '<td>'+ primary +'</td>'+
                        '<td>'+""+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<td>'+ "Secondary" +'</td>'+
                        '<td>'+ secondary +'</td>'+
                        '<td>'+""+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<td>'+ "Trunks" +'</td>'+
                        '<td>'+ trunks +'</td>'+
                        '<td>'+""+'</td>'+
                    '</tr>'+
                '</tbody>'+
            '</table>'+
        '</div>')
        .addTo(map);
    });
         
    map.on('mouseleave', 'adm2', () => {
        map.getCanvas().style.cursor = '';
        popup.remove();
        map.setFilter('adm2-highlighted', ['in', 'NAME_2', '']);
    });
    // map.on('click', 'adm0', (e) => {
    //     const adm0_f = e.features[0];
    //     var adm0_coordinates = adm0_f.geometry.coordinates[0];
    //     var adm0_bounds = adm0_coordinates.reduce(function (adm0_bounds, adm0_coord) {
    //         return adm0_bounds.extend(adm0_coord);
    //     }, new mapboxgl.LngLatBounds(adm0_coordinates[0], adm0_coordinates[0]));
        
    //     map.fitBounds(adm0_bounds, {
    //         padding: 15
    //     });
    // });

    map.on('click', 'adm1', (e) => {
        const adm1_f = e.features[0];
        var adm1_coordinates = adm1_f.geometry.coordinates[0];
        var adm1_bounds = adm1_coordinates.reduce(function (adm1_bounds, adm1_coord) {
            return adm1_bounds.extend(adm1_coord);
        }, new mapboxgl.LngLatBounds(adm1_coordinates[0], adm1_coordinates[0]));
        
        map.fitBounds(adm1_bounds, {
            padding: 25
        });
    });

    map.on('click', 'adm2', (e) => {
        var district = e.features[0].properties.NAME_2;
        var province = e.features[0].properties.NAME_1;
        var country = e.features[0].properties.NAME_0;
        var f_0_15 = e.features[0].properties.F_0_15;
        var f_15_65 = e.features[0].properties.F_15_65;
        var f_above_65 = e.features[0].properties.F__65;
        var f_total = f_0_15 + f_15_65 + f_above_65;
        var m_0_15 = e.features[0].properties.M_0_15;
        var m_15_65 = e.features[0].properties.M_15_65;
        var m_above_65 = e.features[0].properties.M__65;    
        var m_total = m_0_15+m_15_65+m_above_65;
        var hospitals = e.features[0].properties.Hospitals;
        var primary = e.features[0].properties.Primary;
        var secondary = e.features[0].properties.Secondary;
        var trunks = e.features[0].properties.Trunks;

        new mapboxgl.Popup({className:'adm2-popup'})
        .setLngLat(e.lngLat)
        .setHTML('<h6 style="margin-top: 10px; font-weight: bold; margin-bottom: 5px;">'+district+': '+province+', '+country+'</h6>'+
        '<div class="table-responsive adm2-popup-table">'+
            '<table class="table">'+
                '<thead>'+
                    '<tr>'+
                        '<th>'+"Population"+'</th>'+
                        '<th>'+"Female"+'</th>'+
                        '<th>'+"Male"+'</th>'+
                    '</tr>'+
                '</thead>'+
                '<tbody>' +
                    '<tr>'+
                        '<td>'+"Age 0-15"+'</td>'+
                        '<td>'+f_0_15+'</td>'+
                        '<td>'+m_0_15+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<td>'+"Age 15-65"+'</td>'+
                        '<td>'+f_15_65+'</td>'+
                        '<td>'+m_15_65+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<td>'+"Age >65"+'</td>'+
                        '<td>'+f_above_65+'</td>'+
                        '<td>'+m_above_65+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<th>'+"Total"+'</th>'+
                        '<th>'+f_total+'</th>'+
                        '<th>'+m_total+'</th>'+
                    '</tr>'+
                '</tbody>'+
                '<thead>'+
                    '<tr>'+
                        '<th>'+"Health Facilities"+'</th>'+
                        '<th>'+"No."+'</th>'+
                        '<th>'+""+'</th>'+
                    '</tr>'+
                '</thead>'+
                '<tbody>'+
                    '<tr>'+
                        '<td>'+ "Hospitals" +'</td>'+
                        '<td>'+ hospitals +'</td>'+
                        '<td>'+""+'</td>'+
                    '</tr>'+
                '</tbody>'+
                '<thead>'+
                    '<tr>'+
                        '<th>'+"Roads"+'</th>'+
                        '<th>'+"No."+'</th>'+
                        '<th>'+""+'</th>'+
                    '</tr>'+
                '</thead>'+
                '<tbody>'+
                    '<tr>'+
                        '<td>'+ "Primary" +'</td>'+
                        '<td>'+ primary +'</td>'+
                        '<td>'+""+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<td>'+ "Secondary" +'</td>'+
                        '<td>'+ secondary +'</td>'+
                        '<td>'+""+'</td>'+
                    '</tr>'+
                    '<tr>'+
                        '<td>'+ "Trunks" +'</td>'+
                        '<td>'+ trunks +'</td>'+
                        '<td>'+""+'</td>'+
                    '</tr>'+
                '</tbody>'+
            '</table>'+
        '</div>')
        .addTo(map);

        const adm2_f = e.features[0];
        var adm2_coordinates = adm2_f.geometry.coordinates[0];
        var adm2_bounds = adm2_coordinates.reduce(function (adm2_bounds, adm2_coord) {
            return adm2_bounds.extend(adm2_coord);
        }, new mapboxgl.LngLatBounds(adm2_coordinates[0], adm2_coordinates[0]));
        
        map.fitBounds(adm2_bounds, {
            padding: 25
        });
    });
});