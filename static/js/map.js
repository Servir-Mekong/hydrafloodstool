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
    zoom: 4, // starting zoom
    minZoom: 4,
    maxZoom: 10
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

var latest_date = new Date().toISOString().split('T')[0];
// var latest_date = dateList.slice(-1).pop();
// console.log(latest_date);
// Get adm, precipitation, sensor, mode and date values
var selected_adm = $('#admin_selection').val();
var prod = $('#product_selection').val();
var cmap = $('#cmap_selection').val();
var accum = prod.split('|')[0];
var selected_date = $('#date_selection').val();
var selected_start_date = $('#date_selection_start').val();
var selected_end_date = $('#date_selection_end').val();
var pfl_sensor_selection = $('#sensor_selection').val();
var swl_sensor_selection = $('#sensor_selection_swater').val();
var selected_mode = $('#mode_selection').val();
// var selected_age_type = $('#age_type_selection').val();
var selected_age_sensor = $('#age_sensor_selection').val();

$('#date_selection_start').change(function() {
    $("#date_selection_end").prop('disabled', false);
});

const spinnerEl = document.getElementById('spinner');
const backgroundEl = document.getElementById('loading-background');

// Show/hide date selection panel based on mode selection
$('#mode_selection').on('change', function() {
    if($(this).val() === 'historical') {
        $('#update_historical_pfwl').show();
        //$('#update_his_pfwl_button').show();
    } else {
        $('#update_historical_pfwl').hide();
        //$('#update_his_pfwl_button').hide();
    }
});

var popDate = new Date(latest_date).toLocaleString('en-us',{month:'long', day:'numeric', year:'numeric'});
// console.log(dateobj);


var msg_date = document.getElementById('mesg-date');
    msg_date.innerHTML = popDate;  

//Get slider value to add opacity to layer
$("#precip-opacity").slider();
$("#swater-opacity").slider();
$("#fwater-opacity").slider();
$("#fage-opacity").slider();
$("#fduration-opacity").slider();
$("#browse-opacity").slider();
$("#historical-opacity").slider();
$("#doy-opacity").slider();

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

var d = new Date();
d.setDate(d.getDate() - 1);
var precip_date = d.toISOString().split('T')[0]

document.getElementById('date_selection').value = precip_date;
document.getElementById('date_selection_simg').value = latest_date;

var error = document.getElementById("error");

$("#date_selection_end").on("change",function(){
    selected_start = $('#date_selection_start').val();
    selected_end = $(this).val();

    s_day = new Date(selected_start)//.toLocaleString('en-us',{ day:'numeric' });
    e_day = new Date(selected_end)//.toLocaleString('en-us',{ day:'numeric' });
    var diffDays = parseInt((s_day - e_day) / (1000 * 60 * 60 * 24), 10); 
    var absDiff = Math.abs(diffDays)
    var sensor = $('#sensor_selection').val();
    if (absDiff <= 30 && sensor == "all" ){
        error.innerText ="* The start date and end date should be 30 days gap for merged sensor.";
        error.style.color = "red";
        $("#update-historical-pfw-button").prop('disabled', true);
    } else if (absDiff < 1 && sensor == "sentinel1" ){
        error.innerText ="* The start date and end date should be at least 1 days gap for sentinel 1 sensor.";
        error.style.color = "red";
        $("#update-historical-pfw-button").prop('disabled', true);
    } else if (absDiff <= 7 && sensor == "sentinel2" ){
        error.innerText ="* The start date and end date should be at least 7 days gap for sentinel 2 sensor.";
        error.style.color = "red";
        $("#update-historical-pfw-button").prop('disabled', true);
    }  else if (absDiff <= 7 && sensor == "landsat8" ){
        error.innerText ="* The start date and end date should be at least 30 days gap for landsat 8 sensor.";
        error.style.color = "red";
        $("#update-historical-pfw-button").prop('disabled', true);
    }  else {
        error.innerText ="";
        $("#update-historical-pfw-button").prop('disabled', false);
    }  
    $("#sensor_selection").on("change",function(){
        var sensor = $(this).val();
        var selected_start = $('#date_selection_start').val();
        var selected_end = $('#date_selection_end').val();

        s_day = new Date(selected_start);
        e_day = new Date(selected_end);

        var diffDays = parseInt((s_day - e_day) / (1000 * 60 * 60 * 24), 10); 
        var absDiff = Math.abs(diffDays)

        if (absDiff <= 30 && sensor == "all" ){
            error.innerText ="* The start date and end date should be 30 days gap for merged sensor.";
            error.style.color = "red";
            $("#update-historical-pfw-button").prop('disabled', true);
        } else if (absDiff < 1 && sensor == "sentinel1" ){
            error.innerText ="* The start date and end date should be at least 1 days gap for sentinel 1 sensor.";
            error.style.color = "red";
            $("#update-historical-pfw-button").prop('disabled', true);
        } else if (absDiff <= 7 && sensor == "sentinel2" ){
            error.innerText ="* The start date and end date should be at least 7 days gap for sentinel 2 sensor.";
            error.style.color = "red";
            $("#update-historical-pfw-button").prop('disabled', true);
        }  else if (absDiff <= 7 && sensor == "landsat8" ){
            error.innerText ="* The start date and end date should be at least 30 days gap for sentinel 2 sensor.";
            error.style.color = "red";
            $("#update-historical-pfw-button").prop('disabled', true);
        }  else {
            error.innerText ="";
            $("#update-historical-pfw-button").prop('disabled', false);
        }  
    });
    //console.log(absDiff)
    
    // if (selected_start == selected_end){
    //     error.innerText ="* The start date and end date shouldn't be the same.";
    //     error.style.color = "red";
    //     $("#update-historical-pfw-button").prop('disabled', true);
    // } else {
    //     $("#update-historical-pfw-button").prop('disabled', false);
    //     error.innerText = "";
    // }
});


map.on('style.load', () => {

    //Get Potential Flood Layer
    var getPotentialFldWater;
    $.ajax({
        url: '/ajax/potentialfloodmap/',
        type: "GET",
        data: {
            "selected_start_date": selected_start_date,
            "selected_end_date": selected_end_date,
            //"selected_adm": selected_adm,
            "selected_mode": selected_mode,
            "selected_sensor": pfl_sensor_selection
        },
        dataType: 'json',
        //async: false,
        success: (data) => {
            // console.log(data)
            getPotentialFldWater = data;
            var dailyPotentialFloodWater = getPotentialFldWater;        
            map.addSource('floodwater', {
                'type': 'raster',
                'tiles': [
                    dailyPotentialFloodWater
                ],
                'tileSize': 256,
                'minzoom': 4,
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

    // Get Flood Age Layer
    var getFloodAgeLayer;
    $.ajax({
        url: '/ajax/floodagemap/',
        type: "GET",
        data: {
            //"selected_date": latest_date,
            // "selected_age_type": selected_age_type,
            "selected_age_sensor": selected_age_sensor
        },
        dataType: 'json',
        //async: false,
        success: (data) => {
            // console.log(data)
            getFloodAgeLayer = data;
            var dailyFloodAgeLayer = getFloodAgeLayer;        
            map.addSource('floodage', {
                'type': 'raster',
                'tiles': [
                    dailyFloodAgeLayer
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 14
            });
            map.addLayer({
                'id': 'floodage', // Layer ID
                'type': 'raster',
                'source': 'floodage', // ID of the tile source created above
                'layout': {
                    // Make the layer visible by default.
                    'visibility': 'none'
                },
            });
            $("#fage-opacity").on("slide", function(slideEvt) {
                //console.log(slideEvt.value);
                var opac = slideEvt.value
                map.setPaintProperty(
                    'floodage',
                    'raster-opacity',
                    opac
                );
            });
        },
        error: (error) => {
            console.log(error);
        }
    });

    //Get Precipitation Layer 
    var getPrecip;
    $.ajax({
        url: '/ajax/precipmap/',
        type: "GET",
        data: {
            "selected_date": precip_date,
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

    // // Get Daily Surface Water Area Layer
    // var getDailySurWater;
    // $.ajax({
    //     url: '/ajax/surfacewatermap/',
    //     type: "GET",
    //     data: {
    //         "selected_date": latest_date,
    //         "sensor": swl_sensor_selection,
    //     },
    //     dataType: 'json',
    //     async: false,
    //     success: (data) => {
    //         getDailySurWater = data;
    //         var dailySurfaceWater = getDailySurWater;        
    //         map.addSource('surfacewater', {
    //             'type': 'raster',
    //             'tiles': [
    //                 dailySurfaceWater
    //             ],
    //             'tileSize': 256,
    //             'minzoom': 0,
    //             'maxzoom': 10
    //         });
    //         map.addLayer({
    //             'id': 'surfacewater', // Layer ID
    //             'type': 'raster',
    //             'source': 'surfacewater', // ID of the tile source created above
    //             'layout': {
    //                 // Make the layer visible by default.
    //                 'visibility': 'none'
    //             },
    //         });
    //         $("#swater-opacity").on("slide", function(slideEvt) {
    //             //console.log(slideEvt.value);
    //             var opac = slideEvt.value
    //             map.setPaintProperty(
    //                 'surfacewater',
    //                 'raster-opacity',
    //                 opac
    //             );
    //         });
    //     },
    //     error: (error) => {
    //         console.log(error);
    //     }
    // });

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
    //Hide loading bar once tiles from geojson are loaded
    map.on('data', function (e) {
        if (e.dataType === 'source' && e.sourceId === 'floodwater') {
            document.getElementById("loader").style.visibility = "hidden";
        }
    })
});

// Defining function to update layer 
$('#date_selection').change(function(){
    updatePrecipitationData();
});
$('#cmap_selection').change(function(){
    updatePrecipitationData();
});
$('#product_selection').change(function(){
    updatePrecipitationData();
});

// Defining function to update flood layer 
// $('#admin_selection').change(function(){
//     updateFloodMapLayer();
// });
// $('#mode_selection').change(function(){
//     updateFloodMapLayer();
// });
// $('#sensor_selection').change(function(){
//     updateFloodMapLayer();
// });
$("#update-historical-pfw-button").on("click",function(){
    updateFloodMapLayer();
}); 

// Defining function to update flood age layer 
// $('#age_type_selection').change(function(){
//     updateFloodAgeMapLayer();
// });
$('#age_sensor_selection').change(function(){
    updateFloodAgeMapLayer();
});

// Defining function to update daily surface water layer 
// $('#date_selection').change(function(){
//     updateSurfaceWaterMapLayer();
// });

// $('#sensor_selection_swater').change(function(){
//     updateSurfaceWaterMapLayer();
// });

// Update permanent water area layer by changing parameters
$("#update-button").on("click",function(){
    updatePermanentWater();
}); 

//Get values related to raw satellite imagery
var td = new Date();
td.setDate(td.getDate() - 1);
var td = td.toISOString().split('T')[0]

document.getElementById('date_selection_simg').value = td;
var selected_simg_date = $('#date_selection_simg').val();
var viirs_product = "VIIRS_SNPP_CorrectedReflectance_TrueColor";

map.on('style.load', () => {   
    var layer = viirs_product;
    var tilePath = 'wmts/epsg3857/best/' +
        layer+'/default/' +
        selected_simg_date +'/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg';
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
    updateBrowseData();
});
$('#date_selection_simg').change(function(){
    updateBrowseData();
});

// Update satellite imagery
function updateBrowseData() {
    map.removeLayer('gibs');
    map.removeSource('gibs');
    var selected_simg_date = $('#date_selection_simg').val();
    var prod = $('#browse_selection').val();
    var id = prod.split('|')[1];

    var tilePath = 'wmts/epsg3857/best/' +
        id+'/default/' +
        selected_simg_date +'/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg';
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
    map.moveLayer('gibs', 'floodwater');
}

// Update precipitation layer
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
    // Update flood layer
    map.removeLayer('floodwater');
    map.removeSource('floodwater');
    var selected_start_date = $('#date_selection_start').val();
    var selected_end_date = $('#date_selection_end').val();
    // var selected_adm = $('#admin_selection').val();
    var selected_mode = $('#mode_selection').val();
    var pfl_sensor_selection = $('#sensor_selection').val();
    var getPotentialFldWater;
    document.getElementById("loader").style.visibility = "visible";
    $.ajax({
        url: '/ajax/potentialfloodmap/',
        type: "GET",
        data: {
            "selected_start_date": selected_start_date,
            "selected_end_date": selected_end_date,
            //"selected_adm": selected_adm,
            "selected_mode": selected_mode,
            "selected_sensor": pfl_sensor_selection
        },
        dataType: 'json',
        // async: false,
        success: (data) => {
            getPotentialFldWater = data;
            var dailyPotentialFloodWater = getPotentialFldWater;
            map.addSource('floodwater', {
                'type': 'raster',
                'tiles': [
                    dailyPotentialFloodWater
                ],
                'tileSize': 256,
                'minzoom': 5,
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
            document.getElementById("loader").style.visibility = "hidden";
            // //Hide loading bar once tiles from geojson are loaded
            // map.on('data', function (e) {
            //     if (e.dataType === 'source' && e.sourceId === 'floodwater') {
            //         document.getElementById("loader").style.visibility = "hidden";
            //     } else{
            //         document.getElementById("loader").style.visibility = "visible";
            //     }
            // });
        },
        error: (error) => {
            console.log(error);
        }
    });
}

// Defining function to update flood age layer
function updateFloodAgeMapLayer(){
    // Update flood age layer
    map.removeLayer('floodage');
    map.removeSource('floodage');
    
    //Hide loading bar once tiles from geojson are loaded
    // map.on('data', function (e) {
    //     if (e.dataType === 'source' && e.sourceId === 'floodage') {
    //         document.getElementById("loader").style.visibility = "hidden";
    //     } else{
    //         document.getElementById("loader").style.visibility = "visible";
    //     }
    // });

    // var selected_age_type = $('#age_type_selection').val();
    var selected_age_sensor = $('#age_sensor_selection').val();
    // Get Flood Age Layer
    var getFloodAgeLayer;
    $.ajax({
        url: '/ajax/floodagemap/',
        type: "GET",
        data: {
            // "selected_age_type": selected_age_type,
            "selected_age_sensor": selected_age_sensor
        },
        dataType: 'json',
        async: false,
        success: (data) => {
            // console.log(data)
            getFloodAgeLayer = data;
            var dailyFloodAgeLayer = getFloodAgeLayer;        
            map.addSource('floodage', {
                'type': 'raster',
                'tiles': [
                    dailyFloodAgeLayer
                ],
                'tileSize': 256,
                'minzoom': 0,
                'maxzoom': 14
            });
            map.addLayer({
                'id': 'floodage', // Layer ID
                'type': 'raster',
                'source': 'floodage', // ID of the tile source created above
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
}

// //Defining function to update surface water layer
// function updateSurfaceWaterMapLayer(){
//     // Update flood layer
//     map.removeLayer('surfacewater');
//     map.removeSource('surfacewater');
//     // var flood_color = $('#color-picker-flood').val();
//     var selected_date = $('#date_selection').val();
//     var swl_sensor_selection = $('#sensor_selection_swater').val();
//     var getDailySurWater;
//     $.ajax({
//         url: '/ajax/surfacewatermap/',
//         type: "GET",
//         data: {
//             "selected_date": selected_date,
//             "sensor": swl_sensor_selection
//         },
//         dataType: 'json',
//         async: false,
//         success: (data) => {
//             getDailySurWater = data;
//             var dailySurfaceWater = getDailySurWater;
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
//                     'visibility': 'visible'
//                 },
//             });
//         },
//         error: (error) => {
//             console.log(error);
//         }
//     });
// }
// Defining function to update permanent water area layer
function updatePermanentWater(){
    map.removeLayer('permanentwater');
    map.removeSource('permanentwater');
    //Hide loading bar once tiles from geojson are loaded
    map.on('data', function (e) {
        if (e.dataType === 'source' && e.sourceId === 'permanentwater') {
            document.getElementById("loader").style.visibility = "hidden";
        } else{
            document.getElementById("loader").style.visibility = "visible";
        }
    });
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
        type: 'geojson',
        data: '/static/data/adm0.geojson'
    });
    map.addLayer({
        'id': 'adm0',
        'type': 'fill',
        'source': 'adm0-src',
        'minzoom': 0,
        'maxzoom': 6,
        'layout': {
            'visibility': 'visible',
        },
        'paint': {
            'fill-color': 'transparent',
            'fill-opacity': 1.0,
            'fill-outline-color': 'rgba(200, 230, 201, 1)'
        }
    });
    // map.addLayer({
    //     'id': 'adm0-highlighted',
    //     'type': 'line',
    //     'source': 'adm0-src',
    //     'minzoom': 0,
    //     'maxzoom': 6,
    //     'paint': {
    //         'line-color': '#ffc107',
    //         'line-width': 1.5
    //     },
    //     'filter': ['in', 'NAME_0', '']
    // });

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
            'fill-outline-color': '#bdbdbd'
        }
    });
    map.addLayer({
        'id': 'adm1-highlighted',
        'type': 'line',
        'source': 'adm1-src',
        'minzoom': 6,
        'maxzoom': 8,
        'paint': {
            'line-color': '#ffc107',
            'line-width': 1.5
        },
        'filter': ['in', 'NAME_1', '']
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
            'fill-outline-color': '#fff9c4'
        }
    });
    map.addLayer({
        'id': 'adm2-highlighted',
        'type': 'line',
        'source': 'adm2-src',
        'minzoom': 8,
        'maxzoom': 20,
        'paint': {
            'line-color': '#ffc107',
            'line-width': 1.5
        },
        'filter': ['in', 'NAME_2', '']
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

    // map.on('mousemove', 'adm0', (e) => {
    //     // Change the cursor style as a UI indicator.
    //     map.getCanvas().style.cursor = 'pointer';
         
    //     // Use the first found feature.
    //     const feature = e.features[0];
         
    //     // Add features with the same county name
    //     // to the highlighted layer.
    //     map.setFilter('adm0-highlighted', [
    //         'in',
    //         'NAME_0',
    //         feature.properties.NAME_0
    //     ]);
         
    //     // Display a popup with the name of the county.
    //     popup
    //     .setLngLat(e.lngLat)
    //     .setText(feature.properties.NAME_0)
    //     .addTo(map);
    // });
         
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
            'NAME_1',
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
        // popup.remove();
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
         
        // // Display a popup with the name of the county.
        // var district = e.features[0].properties.NAME_2;
        // var province = e.features[0].properties.NAME_1;
        // var country = e.features[0].properties.NAME_0;
        // var f_0_15 = e.features[0].properties.F_0_15;
        // var f_15_65 = e.features[0].properties.F_15_65;
        // var f_above_65 = e.features[0].properties.F__65;
        // var f_total = f_0_15 + f_15_65 + f_above_65;
        // var m_0_15 = e.features[0].properties.M_0_15;
        // var m_15_65 = e.features[0].properties.M_15_65;
        // var m_above_65 = e.features[0].properties.M__65;    
        // var m_total = m_0_15+m_15_65+m_above_65;
        // var hospitals = e.features[0].properties.Hospitals;
        // var primary = e.features[0].properties.Primary;
        // var secondary = e.features[0].properties.Secondary;
        // var trunks = e.features[0].properties.Trunks;

        // popup
        // .setLngLat(e.lngLat)
        // .setHTML('<h6 style="margin-top: 10px; font-weight: bold; margin-bottom: 5px;">'+district+': '+province+', '+country+'</h6>'+
        // '<div class="table-responsive" style="line-height: 0.5">'+
        //     '<table class="table">'+
        //         '<thead>'+
        //             '<tr>'+
        //                 '<th>'+"Population"+'</th>'+
        //                 '<th>'+"Female"+'</th>'+
        //                 '<th>'+"Male"+'</th>'+
        //             '</tr>'+
        //         '</thead>'+
        //         '<tbody>' +
        //             '<tr>'+
        //                 '<td>'+"Age 0-15"+'</td>'+
        //                 '<td>'+f_0_15+'</td>'+
        //                 '<td>'+m_0_15+'</td>'+
        //             '</tr>'+
        //             '<tr>'+
        //                 '<td>'+"Age 15-65"+'</td>'+
        //                 '<td>'+f_15_65+'</td>'+
        //                 '<td>'+m_15_65+'</td>'+
        //             '</tr>'+
        //             '<tr>'+
        //                 '<td>'+"Age >65"+'</td>'+
        //                 '<td>'+f_above_65+'</td>'+
        //                 '<td>'+m_above_65+'</td>'+
        //             '</tr>'+
        //             '<tr>'+
        //                 '<th>'+"Total"+'</th>'+
        //                 '<th>'+f_total+'</th>'+
        //                 '<th>'+m_total+'</th>'+
        //             '</tr>'+
        //         '</tbody>'+
        //         // '<thead>'+
        //         //     '<tr>'+
        //         //         '<th>'+"Health Facilities"+'</th>'+
        //         //         '<th>'+"No."+'</th>'+
        //         //         '<th>'+""+'</th>'+
        //         //     '</tr>'+
        //         // '</thead>'+
        //         '<tbody>'+
        //             '<tr>'+
        //                 '<td>'+ "Hospitals" +'</td>'+
        //                 '<td>'+ hospitals +'</td>'+
        //                 '<td>'+""+'</td>'+
        //             '</tr>'+
        //         '</tbody>'+
        //         '<thead>'+
        //             '<tr>'+
        //                 '<th>'+"Roads"+'</th>'+
        //                 '<th>'+"No."+'</th>'+
        //                 '<th>'+""+'</th>'+
        //             '</tr>'+
        //         '</thead>'+
        //         '<tbody>'+
        //             '<tr>'+
        //                 '<td>'+ "Primary" +'</td>'+
        //                 '<td>'+ primary +'</td>'+
        //                 '<td>'+""+'</td>'+
        //             '</tr>'+
        //             '<tr>'+
        //                 '<td>'+ "Secondary" +'</td>'+
        //                 '<td>'+ secondary +'</td>'+
        //                 '<td>'+""+'</td>'+
        //             '</tr>'+
        //             '<tr>'+
        //                 '<td>'+ "Trunks" +'</td>'+
        //                 '<td>'+ trunks +'</td>'+
        //                 '<td>'+""+'</td>'+
        //             '</tr>'+
        //         '</tbody>'+
        //     '</table>'+
        // '</div>')
        // .addTo(map);
    });
         
    map.on('mouseleave', 'adm2', () => {
        map.getCanvas().style.cursor = '';
        // popup.remove();
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

// var fwater_legend = document.getElementById('fwater-legend');
// var swater_legend = document.getElementById('swater-legend');
// var pwater_legend = document.getElementById('pwater-legend');

// $('#floodwaterCB').change(function(){
//     if(this.checked) {
//         fwater_legend.style.display="block";
//     } else {
//         fwater_legend.style.display="none";
//     }
// });

// $('#surfacewaterCB').change(function(){
//     if(this.checked) {
//         swater_legend.style.display="block";
//     } else {
//         swater_legend.style.display="none";
//     }
// });

// $('#permanentwaterCB').change(function(){
//     if(this.checked) {
//         pwater_legend.style.display="block";
//     } else {
//         pwater_legend.style.display="none";
//     }
// });
