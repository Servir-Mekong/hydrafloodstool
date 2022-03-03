mapboxgl.accessToken = 'pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ';

var openHomeSidebarContent = document.querySelector("#home");
var openLayerSidebarContent= document.querySelector("#layer");
var openBasemapSidebarContent = document.querySelector("#basemap");
var closeHomeSidebarContent = document.querySelector("#close-home-content" );
var closeLayerSidebarContent = document.querySelector("#close-layer-content" );
var closeBasemapSidebarContent = document.querySelector("#close-basemap-content" );
var sidebarContent = document.querySelector('#sidebar-content');

var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/dark-v10', // style URL
    center: [97.9560, 17.9162], // starting position [lng, lat]
    zoom: 4 // starting zoom
});

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

//Onlick expand home sidebar content area
openHomeSidebarContent.onclick = function(){
    if (getComputedStyle(sidebarContent).display === "none"){
        sidebarContent.style.display ="block";
        sidebarContent.style.width = "350px";
        sidebarContent.style.marginLeft = "60px";
    } else if (sidebarContent.style.display === "block"){
        sidebarContent.style.width = "350px";
        sidebarContent.style.marginLeft = "60px";
    }else {
        sidebarContent.style.display = "none";
    }
};

//Onlick expand layer sidebar content area
openLayerSidebarContent.onclick = function(){
    if (getComputedStyle(sidebarContent).display === "none"){
        sidebarContent.style.display ="block";
        sidebarContent.style.width = "350px";
        sidebarContent.style.marginLeft = "60px";
    } else if (sidebarContent.style.display === "block"){
        sidebarContent.style.width = "350px";
        sidebarContent.style.marginLeft = "60px";
    } else {
        sidebarContent.style.display = "none";
    }
}

//Onlick expand basemap sidebar content area
openBasemapSidebarContent.onclick = function(){
    if (getComputedStyle(sidebarContent).display === "none"){
        sidebarContent.style.display ="block";
        sidebarContent.style.width = "350px";
        sidebarContent.style.marginLeft = "60px";
    } else if (sidebarContent.style.display === "block"){
        sidebarContent.style.width = "350px";
        sidebarContent.style.marginLeft = "60px";
    } else {
        sidebarContent.style.display = "none";
    }
}

closeHomeSidebarContent.onclick = function(){
    sidebarContent.style.display = "none";
}
closeLayerSidebarContent.onclick = function(){
    sidebarContent.style.display = "none";
}
closeBasemapSidebarContent.onclick = function(){
    sidebarContent.style.display = "none";
}

$(document).ready(function() {
    $(".basemap-card").click(function () {
        $(".basemap-card").removeClass("active");
        $(this).addClass("active");   
    });
});

// get datelist
var dateList;
$.ajax({
    url: '/ajax/date/',
    type: "GET",
    dataType: "json",
    async: false,
    success: (data) => {
        //console.log(data);
        dateList = data;
        var enableDates = data;
        var enableDatesArray=[];
        $("#date_selection").datepicker("destroy");
        for (var i = 0; i < enableDates.length; i++) {
            var dt = enableDates[i];
            var dd, mm, yyyy;
            if (parseInt(dt.split('-')[2]) <= 9 || parseInt(dt.split('-')[1]) <= 9) {
                dd = parseInt(dt.split('-')[2]);
                mm = parseInt(dt.split('-')[1]);
                yyyy = dt.split('-')[0];
                enableDatesArray.push(yyyy + '-' + mm + '-' + dd);
            }
            else {
                enableDatesArray.push(dt);
            }
        }
        $('#date_selection').datepicker({
            beforeShow: function (input, inst) {
                setTimeout(function () {
                    inst.dpDiv.css({
                        top: $(".datepicker").offset().top + 35,
                        left: $(".datepicker").offset().left
                    });
                }, 0);
            },
            beforeShowDay: function (date) {
                var dt_ddmmyyyy = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() ;
                if (enableDatesArray.indexOf(dt_ddmmyyyy) !== -1) {
                    return {
                        tooltip: 'There is data available',
                        classes: 'active'
                    };
                } else {
                    return false;
                }
            }
        });
    },
        error: (error) => {
        console.log(error);
    }
});
var latest_date = dateList.slice(-1).pop();
//console.log(latest_date);
//Get precipitation and date values
var prod = $('#product_selection').val();
var cmap = $('#cmap_selection').val();
var accum = prod.split('|')[0];
var selected_date = $('#date_selection').val();

document.getElementById('date_selection').value = latest_date;

var msg_date = document.getElementById('mesg-date');
    msg_date.innerHTML = latest_date;  

//Get slider value to add opacity to layer
$("#precip-opacity").slider();
$("#swater-opacity").slider();
$("#fwater-opacity").slider();
$("#browse-opacity").slider();
$("#historical-opacity").slider();

//Define monthly range slider
$('.js-range-slider').ionRangeSlider({
    skin: "round",
    type: "double",
    grid: true,
    from: 0,
    to: 11,
    values: [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]
});

// Get values for permanent water
var startYear = $('#start_year_selection_historical').val();
var endYear = $('#end_year_selection_historical').val();
var slider = $("#month_range").data("ionRangeSlider");
var startMonth = slider.result.from + 1;
var endMonth= slider.result.to + 1;
var method = 'discrete';
//var wcolor = $('#color-picker-water').val();
//var geom = JSON.stringify(drawing_polygon);
if (startMonth === endMonth) { endMonth += 1; }

map.on('style.load', () => {
    //Get Precipitation Layer 
    var getPrecip;
    $.ajax({
        url: '/ajax/precipmap/',
        type: "GET",
        data: {
            "selected_date": latest_date,
            "cmap": cmap,
            "accum": accum
        },
        dataType: 'json',
        success: (precip_data) => {
            getPrecip = precip_data;
            var dailyPrecip = getPrecip;   
            map.addSource('precip', {
                'type': 'raster',
                'tiles': [
                    dailyPrecip
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'precip', // Layer ID
                'type': 'raster',
                'source': 'precip', // ID of the tile source created above
                'layout': {
                    // Make the layer visible by default.
                    'visibility': 'none'
                },
            });
            $("#precip-opacity").on("slide", function(slideEvt) {
                var opac = slideEvt.value
                map.setPaintProperty(
                    'precip',
                    'raster-opacity',
                    opac
                );
            });
        },
        error: (error) => {
            console.log(error);
        }
    });

    //Get Potential Flood Layer
    var getPotentialFldWater;
    $.ajax({
        url: '/ajax/potentialfloodmap/',
        type: "GET",
        data: {
            "selected_date": latest_date,
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            getPotentialFldWater = data;
            var dailyPotentialFloodWater = getPotentialFldWater;        
            map.addSource('floodwater', {
                'type': 'raster',
                'tiles': [
                    dailyPotentialFloodWater
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'floodwater', // Layer ID
                'type': 'raster',
                'source': 'floodwater', // ID of the tile source created above
                'layout': {
                    // Make the layer visible by default.
                    'visibility': 'visible'
                },
            });
            $("#fwater-opacity").on("slide", function(slideEvt) {
                //console.log(slideEvt.value);
                var opac = slideEvt.value
                map.setPaintProperty(
                    'floodwater',
                    'raster-opacity',
                    opac
                );
            });
        },
        error: (error) => {
            console.log(error);
        }
    });

    //Get Daily Surface Water Area Layer
    var getDailySurWater;
    $.ajax({
        url: '/ajax/surfacewatermap/',
        type: "GET",
        data: {
            "selected_date": latest_date,
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
                    'visibility': 'none'
                },
            });
            $("#swater-opacity").on("slide", function(slideEvt) {
                //console.log(slideEvt.value);
                var opac = slideEvt.value
                map.setPaintProperty(
                    'surfacewater',
                    'raster-opacity',
                    opac
                );
            });
        },
        error: (error) => {
            console.log(error);
        }
    });

    //Get Permanent Water Area Layer
    var getPermanentWater; 
    $.ajax({
        url: '/ajax/permanaentwatermap/',
        type: "GET",
        data: {
            'startYear': startYear,
            'endYear': endYear,
            'startMonth': startMonth,
            'endMonth': endMonth,
            'method': method,
            //wcolor: wcolor,
            //geom: geom
        },
        dataType: 'json',
        success: (historical_data) => {
            getPermanentWater = historical_data;
            var dailyPermanentWater = getPermanentWater;
            map.addSource('permanentwater', {
                'type': 'raster',
                'tiles': [
                    dailyPermanentWater
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'permanentwater', // Layer ID
                'type': 'raster',
                'source': 'permanentwater', // ID of the tile source created above
                'layout': {
                    // Make the layer visible by default.
                    'visibility': 'visible'
                },
            });
            $("#historical-opacity").on("slide", function(slideEvt) {
                var opac = slideEvt.value
                map.setPaintProperty(
                    'permanentwater',
                    'raster-opacity',
                    opac
                );
            });
        },
        error: (error) => {
        console.log(error);
        }
    });
});

//Defining function to update layer 
$('#date_selection').change(function(){
    updatePrecipitationData()
});
$('#cmap_selection').change(function(){
    updatePrecipitationData();
});
$('#product_selection').change(function(){
    updatePrecipitationData();
});

//Defining function to update flood layer 
$('#date_selection').change(function(){
    updateFloodMapLayer()
});

//Defining function to update daily surface water layer 
$('#date_selection').change(function(){
    updateSurfaceWaterMapLayer()
});

//Update permanent water area layer by changing parameters
$("#update-button").on("click",function(){
    updatePermanentWater();
}); 

//Get values related to raw satellite imagery
var selected_date = $('#date_selection').val();
var viirs_product = "VIIRS_SNPP_CorrectedReflectance_TrueColor";

map.on('style.load', () => {   
    var layer = viirs_product;
    var tilePath = 'wmts/epsg3857/best/' +
        layer+'/default/' +
        selected_date +'/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg';
    map.addSource('gibs', {
        'type': 'raster',
        'tiles': [
            'https://gibs-a.earthdata.nasa.gov/' + tilePath,
            'https://gibs-b.earthdata.nasa.gov/' + tilePath,
            'https://gibs-c.earthdata.nasa.gov/' + tilePath
        ],
        'tileSize': 256,
        'minzoom': 0,
        'maxzoom': 10,
        'attribution': '<a href="https://wiki.earthdata.nasa.gov/display/GIBS" target="_">' + 'NASA EOSDIS GIBS</a>;'
    });
    map.addLayer({
        'id': 'gibs', // Layer ID
        'type': 'raster',
        'source': 'gibs', // ID of the tile source created above
        'layout': {
            // Make the layer visible by default.
            'visibility': 'none'
        },
    });
    $("#browse-opacity").on("slide", function(slideEvt) {
        var opac = slideEvt.value
        map.setPaintProperty(
            'gibs',
            'raster-opacity',
            opac
        );
    });
});

$('#browse_selection').change(function(){
    var selected_date = $('#date_selection').val();
    var prod = $('#browse_selection').val();
    var id = prod.split('|')[1];
    map.removeLayer('gibs');
    map.removeSource('gibs');
    var tilePath = 'wmts/epsg3857/best/' +
        id+'/default/' +
        selected_date +'/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg';
    //console.log(tilePath);
    map.addSource('gibs', {
        'type': 'raster',
        'tiles': [
            'https://gibs-a.earthdata.nasa.gov/' + tilePath,
            'https://gibs-b.earthdata.nasa.gov/' + tilePath,
            'https://gibs-c.earthdata.nasa.gov/' + tilePath
        ],
        'tileSize': 256,
        'minzoom': 0,
        'maxzoom': 10,
        'attribution': '<a href="https://wiki.earthdata.nasa.gov/display/GIBS" target="_">' + 'NASA EOSDIS GIBS</a>;'
    });
    map.addLayer({
        'id': 'gibs', // Layer ID
        'type': 'raster',
        'source': 'gibs', // ID of the tile source created above
        'layout': {
            // Make the layer visible by default.
            'visibility': 'visible'
        },
    });
});

//Update precipitation layer
function updatePrecipitationData(){
    map.removeLayer('precip');
    map.removeSource('precip');
    var prod = $('#product_selection').val();
    var cmap = $('#cmap_selection').val();
    var accum = prod.split('|')[0];
    var selected_date = $('#date_selection').val();
    var getPrecip;
    $.ajax({
        url: '/ajax/precipmap/',
        type: "GET",
        data: {
            "selected_date": selected_date,
            "cmap": cmap,
            "accum": accum
        },
        dataType: 'json',
        success: (precip_data) => {
            getPrecip = precip_data;
            var dailyPrecip = getPrecip;   
            map.addSource('precip', {
                'type': 'raster',
                'tiles': [
                    dailyPrecip
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'precip', // Layer ID
                'type': 'raster',
                'source': 'precip', // ID of the tile source created above
                'layout': {
                    // Make the layer visible by default.
                    'visibility': 'none'
                },
            });
        },
        error: (error) => {
            console.log(error);
        }
    });
}

//Defining function to update flood layer
function updateFloodMapLayer(){
    //var flood_color = $('#color-picker-flood').val();
    var selected_date = $('#date_selection').val();
    //Update flood layer
    map.removeLayer('floodwater');
    map.removeSource('floodwater');
    var getPotentialFldWater;
    $.ajax({
        url: '/ajax/surfacewatermap/',
        type: "GET",
        data: {
            "selected_date": selected_date,
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            getPotentialFldWater = data;
            var dailyPotentialFloodWater = getPotentialFldWater;
            map.addSource('surfacewater', {
                'type': 'raster',
                'tiles': [
                    dailyPotentialFloodWater
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'floodwater', // Layer ID
                'type': 'raster',
                'source': 'floodwater', // ID of the tile source created above
                // 'layout': {
                //     // Make the layer visible by default.
                //     'visibility': 'visible'
                // },
            });
        },
        error: (error) => {
            console.log(error);
        }
    });
}
//Defining function to update surface water layer
function updateSurfaceWaterMapLayer(){
    //var flood_color = $('#color-picker-flood').val();
    var selected_date = $('#date_selection').val();
    //Update flood layer
    map.removeLayer('surfacewater');
    map.removeSource('surfacewater');
    var getDailySurWater;
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
                // 'layout': {
                //     // Make the layer visible by default.
                //     'visibility': 'visible'
                // },
            });
        },
        error: (error) => {
            console.log(error);
        }
    });
}
//Defining function to update permanent water area layer
function updatePermanentWater(){
    map.removeLayer('permanentwater');
    map.removeSource('permanentwater');
    var startYear = $('#start_year_selection_historical').val();
    var endYear = $('#end_year_selection_historical').val();
    var slider = $("#month_range").data("ionRangeSlider");  
    var startMonth = slider.result.from + 1;
    var endMonth= slider.result.to + 1;
    var method = 'discrete';
    //var wcolor = $('#color-picker-water').val();
    //var geom = JSON.stringify(drawing_polygon);
    var getPermanentWater; 
    $.ajax({
        url: '/ajax/permanaentwatermap/',
        type: "GET",
        data: {
            'startYear': startYear,
            'endYear': endYear,
            'startMonth': startMonth,
            'endMonth': endMonth,
            'method': method,
            //wcolor: wcolor,
            //geom: geom
        },
        dataType: 'json',
        success: (historical_data) => {
            getPermanentWater = historical_data;
            var dailyPermanentWater = getPermanentWater;
            map.addSource('permanentwater', {
                'type': 'raster',
                'tiles': [
                    dailyPermanentWater
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 10
            });
            map.addLayer({
                'id': 'permanentwater', // Layer ID
                'type': 'raster',
                'source': 'permanentwater', // ID of the tile source created above
                // 'layout': {
                //     // Make the layer visible by default.
                //     'visibility': 'none'
                // },
            });
        },
        error: (error) => {
        console.log(error);
        }
    });
}

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
        type: 'vector',
        url: 'mapbox://kamalh27.adm0',
        'minzoom': 0,
        'maxzoom': 6
    });
    map.addLayer(
        {
        'id': 'adm0',
        'type': 'fill',
        'source': 'adm0-src',
        'source-layer': 'adm0',
        'layout': {
            'visibility': 'visible',
        },
        'paint': {
            'fill-color': 'transparent',
            'fill-opacity': 1.0,
            'fill-outline-color': 'rgba(200, 230, 201, 1)'
        }
    });
    map.addLayer(
        {
            'id': 'adm0-highlighted',
            'type': 'line',
            'source': 'adm0-src',
            'source-layer': 'adm0',
            'paint': {
                'line-color': '#ffc107',
                'line-width': 1.5
            },
            // Display none by adding a
            // filter with an empty string.
            'filter': ['in', 'NAME_0', '']
        },    
    );

    // Province layer
    map.addSource('adm1-src', {
        type: 'vector',
        url: 'mapbox://kamalh27.adm1',
        minZoom: 6,
        maxZoom: 8
    });
    map.addLayer(
        {
        'id': 'adm1',
        'type': 'fill',
        'source': 'adm1-src',
        'source-layer': 'adm1',
        'layout': {
            'visibility': 'visible',
        },
        'paint': {
            'fill-color': 'transparent',
            'fill-opacity': 1.0,
            'fill-outline-color': '#69f0ae'
        }
    });
    map.addLayer(
        {
            'id': 'adm1-highlighted',
            'type': 'line',
            'source': 'adm1-src',
            'source-layer': 'adm1',
            'paint': {
                'line-color': '#ffc107',
                'line-width': 1.5
            },
            // Display none by adding a
            // filter with an empty string.
            'filter': ['in', 'NAME_1', '']
        },    
    );

    // District layer
    map.addSource('adm2-src', {
        type: 'vector',
        url: 'mapbox://kamalh27.adm2',
        'minzoom': 8,
        'maxzoom': 16
    });
    map.addLayer(
        {
        'id': 'adm2',
        'type': 'fill',
        'source': 'adm2-src',
        'source-layer': 'adm2',
        'layout': {
            'visibility': 'visible',
        },
        'paint': {
            'fill-color': 'transparent',
            'fill-opacity': 1.0,
            'fill-outline-color': '#fff9c4'
        }
    });
    map.addLayer(
        {
            'id': 'adm2-highlighted',
            'type': 'line',
            'source': 'adm2-src',
            'source-layer': 'adm2',
            'paint': {
                'line-color': '#ffc107',
                'line-width': 1.5
            },
            'filter': ['in', 'NAME_2', '']
        },    
    );
    
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
        const f = e.features[0];
        var coordinates = f.geometry.coordinates[0];
        var bounds = coordinates.reduce(function (bounds, coord) {
            return bounds.extend(coord);
        }, new mapboxgl.LngLatBounds(coordinates[0], coordinates[0]));
        
        map.fitBounds(bounds, {
            padding: 20
        });
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

    // map.on('click', 'adm1', (e) => {
    //     const adm1_f = e.features[0];
    //     var adm1_coordinates = adm1_f.geometry.coordinates[0];
    //     var adm1_bounds = adm1_coordinates.reduce(function (adm1_bounds, adm1_coord) {
    //         return adm1_bounds.extend(adm1_coord);
    //     }, new mapboxgl.LngLatBounds(adm1_coordinates[0], adm1_coordinates[0]));
        
    //     map.fitBounds(adm1_bounds, {
    //         padding: 25
    //     });
    // });

    map.on('mousemove', 'adm0', (e) => {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';
         
        // Use the first found feature.
        const feature = e.features[0];
         
        // Add features with the same county name
        // to the highlighted layer.
        // map.setFilter('adm0-highlighted', [
        //     'in',
        //     'NAME_0',
        //     feature.properties.NAME_0
        // ]);
         
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
        //overlay.style.display = 'none';
    });

    map.on('mousemove', 'adm1', (e) => {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';
         
        // Use the first found feature.
        const feature = e.features[0];
         
        // Add features with the same county name
        // to the highlighted layer.
        // map.setFilter('adm1-highlighted', [
        //     'in',
        //     'NAME_0',
        //     feature.properties.NAME_1
        // ]);
         
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
        //overlay.style.display = 'none';
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
        popup
        .setLngLat(e.lngLat)
        .setText(feature.properties.NAME_2)
        .addTo(map);
    });
         
    map.on('mouseleave', 'adm2', () => {
        map.getCanvas().style.cursor = '';
        popup.remove();
        map.setFilter('adm2-highlighted', ['in', 'NAME_2', '']);
        //overlay.style.display = 'none';
    });
});

switchlayer = function (lname) {
    if (document.getElementById(lname + "CB").checked) {
        map.setLayoutProperty(lname, 'visibility', 'visible');
    } else {
        map.setLayoutProperty(lname, 'visibility', 'none');
    }
}

/**
* Toggle layer visualizing
*/

toggleLayer = function (lname) {
    if (document.getElementById(lname + "CB").checked) {
        map.setLayoutProperty(lname, 'visibility', 'visible');
    } else {
        map.setLayoutProperty(lname, 'visibility', 'none');
    }
}

$('#nav-basemap div').on('click', function(e) {
    var selected_basemap = this.getAttribute('data-layer');
    //MapBox Basemap
    if((selected_basemap === "streets-v11")){
        map.setStyle('mapbox://styles/mapbox/streets-v11'); 
    }else if(selected_basemap === "satellite-v9"){
        map.setStyle('mapbox://styles/mapbox/satellite-v9');    
    }else if(selected_basemap === "light-v10"){
        map.setStyle('mapbox://styles/mapbox/light-v10');
    }else if(selected_basemap === "dark-v10"){
        map.setStyle('mapbox://styles/mapbox/dark-v10');
    }else if(selected_basemap === "outdoors-v11"){
        map.setStyle('mapbox://styles/mapbox/outdoors-v11');
    }
});

//Legend
const legendEl = document.getElementById('legend');
map.on('load', () => {
    legendEl.style.display = 'block';
});

var fwater_legend = document.getElementById('fwater-legend');
var swater_legend = document.getElementById('swater-legend');
var pwater_legend = document.getElementById('pwater-legend');

$('#floodwaterCB').change(function(){
    if(this.checked) {
        fwater_legend.style.display="block";
    } else {
        fwater_legend.style.display="none";
    }
});

$('#surfacewaterCB').change(function(){
    if(this.checked) {
        swater_legend.style.display="block";
    } else {
        swater_legend.style.display="none";
    }
});

$('#permanentwaterCB').change(function(){
    if(this.checked) {
        pwater_legend.style.display="block";
    } else {
        pwater_legend.style.display="none";
    }
});

// //Defining function to update layer 
// $('#date_selection').change(function(){
//     //Update precipitation layer
//     map.removeLayer('precip');
//     map.removeSource('precip');
//     var getPrecip;
//     $.ajax({
//         url: '/ajax/precipmap/',
//         type: "GET",
//         data: {
//             "selected_date": selected_date,
//             "cmap": cmap,
//             "accum": accum
//         },
//         dataType: 'json',
//         success: (precip_data) => {
//             getPrecip = precip_data;
//             var dailyPrecip = getPrecip;   
//             map.addSource('precip', {
//                 'type': 'raster',
//                 'tiles': [
//                     dailyPrecip
//                 ],
//                 'tileSize': 256,
//                 'minzoom': 0,
//                 'maxzoom': 10
//             });
//             map.addLayer({
//                 'id': 'precip', // Layer ID
//                 'type': 'raster',
//                 'source': 'precip', // ID of the tile source created above
//                 'layout': {
//                     // Make the layer visible by default.
//                     'visibility': 'none'
//                 },
//             });
//         },
//         error: (error) => {
//             console.log(error);
//         }
//     });

//     //Update flood layer
//     map.removeLayer('surfacewater');
//     map.removeSource('surfacewater');
//     var getDailySurWater;
//     $.ajax({
//         url: '/ajax/surfacewatermap/',
//         type: "GET",
//         data: {
//             "selected_date": selected_date,
//         },
//         dataType: 'json',
//         async: false,
//         success: (data) => {
//             getDailySurWater = data;

//             var dailySurfaceWater = getDailySurWater;
//             // Add a new vector tile source with ID 'mapillary'.
//             map.addSource('surfacewater', {
//                 'type': 'raster',
//                 'tiles': [
//                     dailySurfaceWater
//                 ],
//                 'tileSize': 256,
//                 'minzoom': 0,
//                 'maxzoom': 10
//             });
//             map.addLayer({
//                 'id': 'surfacewater', // Layer ID
//                 'type': 'raster',
//                 'source': 'surfacewater', // ID of the tile source created above
//                 'layout': {
//                     // Make the layer visible by default.
//                     'visibility': 'none'
//                 },
//             });
//         },
//         error: (error) => {
//             console.log(error);
//         }
//     });
    
//     //Update permanent water layer
//     map.removeLayer('permanentwater');
//     map.removeSource('permanentwater');
//     var getPermanentWater; 
//     $.ajax({
//         url: '/ajax/permanaentwatermap/',
//         type: "GET",
//         data: {
//             'startYear': startYear,
//             'endYear': endYear,
//             'startMonth': startMonth,
//             'endMonth': endMonth,
//             'method': method,
//             //wcolor: wcolor,
//             //geom: geom
//         },
//         dataType: 'json',
//         success: (historical_data) => {
//             getPermanentWater = historical_data;
//             var dailyPermanentWater = getPermanentWater;
//             map.addSource('permanentwater', {
//                 'type': 'raster',
//                 'tiles': [
//                     dailyPermanentWater
//                 ],
//                 'tileSize': 256,
//                 'minzoom': 0,
//                 'maxzoom': 10
//             });
//             map.addLayer({
//                 'id': 'permanentwater', // Layer ID
//                 'type': 'raster',
//                 'source': 'permanentwater', // ID of the tile source created above
//                 'layout': {
//                     // Make the layer visible by default.
//                     'visibility': 'none'
//                 },
//             });
//         },
//         error: (error) => {
//         console.log(error);
//         }
//     });
// });