var openHomeSidebarContent = document.querySelector("#home");
var openLayerSidebarContent= document.querySelector("#layer");
var openBasemapSidebarContent = document.querySelector("#basemap");
var closeHomeSidebarContent = document.querySelector("#close-home-content" );
var closeLayerSidebarContent = document.querySelector("#close-layer-content" );
var closeBasemapSidebarContent = document.querySelector("#close-basemap-content" );
var sidebarContent = document.querySelector('#sidebar-content');

// Onlick expand home sidebar content area
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

// Onlick expand layer sidebar content area
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

// Onlick expand basemap sidebar content area
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

// Define map center
var MapOtions = {
    center: [19.9162, 102.9560],
    zoom: 5,
    zoomControl: false,
    minZoom: 5,
    // maxZoom: 14
}
// Create a map
var map = L.map('map', MapOtions);

// Set default basemap
var basemap_layer = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ', {
    tileSize: 256,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
// basemap_layer.bringToBack();
// Change zoom control postion to right
L.control.zoom({
    position: 'topright'
}).addTo(map);

// Add scale control to map
var scale = L.control.scale({
    position:'bottomleft'
}).addTo(map);

// Onclick change basemap active class
$(document).ready(function() {
    $(".basemap-card").click(function () {
        $(".basemap-card").removeClass("active");
        // $(".tab").addClass("active"); // instead of this do the below 
        $(this).addClass("active");   
    });
});

// Onclick switch basemap 
$('#nav-basemap div').on('click', function(e) {
    var selected_basemap = this.getAttribute('data-layer');
    //MapBox Basemap
    if((selected_basemap === "streets-v11")){
        basemap_layer.setUrl('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ');
    }else if(selected_basemap === "satellite-v9"){
        basemap_layer.setUrl('https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/512/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ');
    }else if(selected_basemap === "light-v10"){
        basemap_layer.setUrl('https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/512/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ');
    }else if(selected_basemap === "outdoors-v11"){
        basemap_layer.setUrl('https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/tiles/512/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ');
    }else if(selected_basemap === "dark-v10"){
        basemap_layer.setUrl('https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/512/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ');
    }else if(selected_basemap === "mb-galaxy"){
        basemap_layer.setUrl('https://api.mapbox.com/styles/v1/kamalh27/cl6d9l03u004o14paq58pbjmc/tiles/512/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t3b2Roc2M3MDF2bDJ2cDY0ZmppdXl0MCJ9.Gn5rUJgaap_KDcnhyROMzQ');
    }else if(selected_basemap === "osm"){
        basemap_layer.setUrl('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');  
    }else if((selected_basemap === "street")){
        basemap_layer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}');
    }else if(selected_basemap === "satellite"){
        basemap_layer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
    }else if(selected_basemap === "terrain"){
        basemap_layer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}');
    }
    else if(selected_basemap === "topo"){
        basemap_layer.setUrl('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png');
    }
    else if(selected_basemap === "dark"){
        basemap_layer.setUrl('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png');
    }
    else if(selected_basemap === "gray"){
        basemap_layer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}');
    } 
});

var latest_date = new Date().toISOString().split('T')[0];
// Get adm, precipitation, sensor, mode and date values
// var selected_adm = $('#admin_selection').val();
var prod = $('#product_selection').val();
var cmap = $('#cmap_selection').val();
var accum = prod.split('|')[0];
// var selected_date = $('#date_selection').val();
// var selected_date_depth = $('#date_selection_depth').val();
var selected_start_date = $('#date_selection_start').val();
var selected_end_date = $('#date_selection_end').val();
var pfl_sensor_selection = $('#sensor_selection').val();
var swl_sensor_selection = $('#sensor_selection_swater').val();
var selected_mode = $('#mode_selection').val();
// var selected_age_type = $('#age_type_selection').val();
// var selected_age_date = $('#date_selection_age').val();
var selected_age_sensor = $('#age_sensor_selection').val();

$('#date_selection_start').change(function() {
    $("#date_selection_end").prop('disabled', false);
});

// Show/hide date selection panel based on mode selection
$('#mode_selection').on('change', function() {
    if($(this).val() === 'historical') {
        $('#update_historical_pfwl').show();
        $('#ops_date').hide();
        $('#date_selection_ops').hide();
    } else {
        $('#update_historical_pfwl').hide();
        $('#ops_date').show();
        $('#date_selection_ops').show();
    }
});

const today = new Date();
today.setDate(today.getDate() - 1)
const ops_date = today.toISOString().split('T')[0]

document.getElementById('date_selection_ops').value = ops_date;
document.getElementById('date_selection_depth').value = ops_date;
document.getElementById('date_selection_age').value = ops_date;
document.getElementById('date_selection_simg').value = ops_date;

var popDate = new Date(ops_date).toLocaleString('en-us',{month:'long', day:'numeric', year:'numeric'});
// console.log(dateobj);

var msg_date = document.getElementById('mesg-date');
    msg_date.innerHTML = popDate;  

var d = new Date();
d.setDate(d.getDate() - 1);
var precip_date = d.toISOString().split('T')[0]
document.getElementById('date_selection').value = precip_date;

//Get slider value to add opacity to layer
$("#precip-opacity").slider();
$("#swater-opacity").slider();
$("#fwater-opacity").slider();
$("#fage-opacity").slider();
$("#fduration-opacity").slider();
$("#browse-opacity").slider();
$("#historical-opacity").slider();
$("#doy-opacity").slider();
$("#fdepth-opacity").slider();

var error = document.getElementById("error");

$("#date_selection_end").on("change",function(){
    selected_start = $('#date_selection_start').val();
    selected_end = $(this).val();

    s_day = new Date(selected_start)//.toLocaleString('en-us',{ day:'numeric' });
    e_day = new Date(selected_end)//.toLocaleString('en-us',{ day:'numeric' });
    var diffDays = parseInt((s_day - e_day) / (1000 * 60 * 60 * 24), 10); 
    var absDiff = Math.abs(diffDays)
    var sensor = $('#sensor_selection').val();
    if (absDiff <= 0 && sensor == "all" ){
        error.innerText ="* The start date and end date shouldn't be the same. At least 1 day gap between start and end date.";
        error.style.color = "red";
        $("#update-historical-pfw-button").prop('disabled', true);
    } 
    else {
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

        if (absDiff <= 1 && sensor == "all" ){
            error.innerText ="* The start date and end date shouldn't be the same. At least 1 day gap between start and end date.";
            error.style.color = "red";
            $("#update-historical-pfw-button").prop('disabled', true);
        } 
        else {
            error.innerText ="";
            $("#update-historical-pfw-button").prop('disabled', false);
        }  
    });
});

/* ================ Flood Layer ========================= */

$("#loader").show();

// Define Earth Engine Flood Layer in Leaflet
var fld_layer = L.tileLayer('', {
    attribution: '&copy; <a href="https://earthengine.google.com" target="_blank">Google Earth Engine</a> contributors'
}).addTo(map);
// Get Flood Layer
$.ajax({
    url: '/ajax/potentialfloodmap/',
    type: "GET",
    data: {
        "selected_start_date": selected_start_date,
        "selected_end_date": selected_end_date,
        //"selected_adm": selected_adm,
        "selected_mode": selected_mode,
        "selected_sensor": pfl_sensor_selection,
        "ops_date": ops_date
    },
    dataType: 'json',
    //async: false,
    success: (fld_data) => {
        fld_layer.setUrl(fld_data);  
        $("#loader").hide();
        setTimeout(function() { $("#loader").hide(); }, 8000);
    },
    error: (error) => {
        console.log(error);
        $("#error-overlay").css({ display: "block" });
        $("#loader").hide();
    }
});

// Check add or remove flood layer to overlay on map
$("#floodwaterCB").on("click", function(){
    if(this.checked) {
        updateFloodMapLayer();
        // $('#map-overlay').show(); 
        var selected_ops_date = $('#date_selection_ops').val(); 
        var popDate = new Date(selected_ops_date).toLocaleString('en-us',{month:'long', day:'numeric', year:'numeric'});
        var msg_date = document.getElementById('mesg-date');
            msg_date.innerHTML = popDate;                 
    } else {
        map.removeLayer(fld_layer);
        // $('#map-overlay').hide()
    }
});  

// Get flood slider value
$("#fwater-opacity").on("slide", function(slideEvt) {
    //console.log(slideEvt.value);
    var opac = slideEvt.value
    fld_layer.setOpacity(opac);
});

$("#update-historical-pfw-button").on("click",function(){
    updateFloodMapLayer();
}); 

// Defining function to update layer 
$('#date_selection_ops').change(function(){
    updateFloodMapLayer();
    var selected_ops_date = $('#date_selection_ops').val(); 
    document.getElementById('date_selection_depth').value = selected_ops_date;
    document.getElementById('date_selection_age').value = selected_ops_date;
    document.getElementById('date_selection_simg').value = selected_ops_date;
    document.getElementById('date_selection').value = selected_ops_date;
     
    var popDate = new Date(selected_ops_date).toLocaleString('en-us',{month:'long', day:'numeric', year:'numeric'});
    var msg_date = document.getElementById('mesg-date');
        msg_date.innerHTML = popDate;   
});

// Show/hide overlay message box

$('#mode_selection').change(function(){
    var mode = $(this).val();
    // console.log(mode)
    if (mode == "historical"){
        $('#map-overlay').hide()
    } else {
        $('#map-overlay').show()
    }
});


// Defining function to update flood layer
function updateFloodMapLayer(){
    $("#floodwaterCB").prop("checked", true);
    $("#loader").show();
    var selected_start_date = $('#date_selection_start').val();
    var selected_end_date = $('#date_selection_end').val();
    // var selected_adm = $('#admin_selection').val();
    var selected_mode = $('#mode_selection').val();
    var pfl_sensor_selection = $('#sensor_selection').val();
    var selected_ops_date = $('#date_selection_ops').val();
    $.ajax({
        url: '/ajax/potentialfloodmap/',
        type: "GET",
        data: {
            "selected_start_date": selected_start_date,
            "selected_end_date": selected_end_date,
            //"selected_adm": selected_adm,
            "selected_mode": selected_mode,
            "selected_sensor": pfl_sensor_selection,
            "ops_date": selected_ops_date
        },
        dataType: 'json',
        // async: false,
        success: (fld_data) => {
            fld_layer.setUrl(fld_data); 
            map.addLayer(fld_layer);
            $("#loader").hide();
            setTimeout(function() { $("#loader").hide(); }, 10000);
            $("#error-overlay").css({ display: "none" });
        },
        error: (error) => {
            console.log(error);
            $("#error-overlay").css({ display: "block" });
            $("#loader").hide();
        }
    });
}

/////////////////////////////////////////////////////////////////////////////

/* ============================== Flood Depth Map ============================= */
// Define Earth Engine Flood Layer in Leaflet
var depth_layer = L.tileLayer('', {
    attribution: '&copy; <a href="https://earthengine.google.com" target="_blank">Google Earth Engine</a> contributors'
});

$("#flooddepthCB").on("click", function(){
    if(this.checked) {
        updateFloodDepthMapLayer();       
    } 
    else {
        map.removeLayer(depth_layer);
    }
});  

// Get depth slider value
$("#fdepth-opacity").on("slide", function(slideEvt) {
    var opac = slideEvt.value
    depth_layer.setOpacity(opac);
});

// Defining function to update layer 
$('#date_selection_depth').change(function(){
    updateFloodDepthMapLayer();
    var selected_date_depth = $('#date_selection_depth').val();
    document.getElementById('date_selection_ops').value = selected_date_depth;
    document.getElementById('date_selection_age').value = selected_date_depth;
    document.getElementById('date_selection_simg').value = selected_date_depth;
    document.getElementById('date_selection').value = selected_date_depth;

    var selected_ops_date = $('#date_selection_ops').val(); 
    var popDate = new Date(selected_ops_date).toLocaleString('en-us',{month:'long', day:'numeric', year:'numeric'});
    var msg_date = document.getElementById('mesg-date');
        msg_date.innerHTML = popDate;   
});

// Defining function to update flood layer
function updateFloodDepthMapLayer(){
    $("#flooddepthCB").prop("checked", true);
    $("#loader").show();
    var selected_date_depth = $('#date_selection_depth').val();
    $.ajax({
        url: '/ajax/depthmap/',
        type: "GET",
        data: {
            "selected_date_depth": selected_date_depth
        },
        dataType: 'json',
        // async: false,
        success: (depth_data) => {
            depth_layer.setUrl(depth_data);  
            map.addLayer(depth_layer); 
            $("#loader").hide();
            setTimeout(function() { $("#loader").hide(); }, 8000);
        },
        error: (error) => {
            console.log(error);
            $("#error-overlay").css({ display: "block" });
            $("#loader").hide();
        }
    });
}
//////////////////////////////////////////////////////////////////////////////////////

/* ============================== Precipitation Layer ============================= */

// Define Earth Engine Precipitation Layer in Leaflet
var precip_layer = L.tileLayer('', {
    attribution: '&copy; <a href="https://earthengine.google.com" target="_blank">Google Earth Engine</a> contributors'
});

// Get Precipitation Layer 
$("#precipCB").on("click", function(){
    if(this.checked) {
        updatePrecipitationData();
    }
    else{
        map.removeLayer(precip_layer);
    }
});  

// Get precipitation slider value
$("#precip-opacity").on("slide", function(slideEvt) {
    var opac = slideEvt.value
    precip_layer.setOpacity(opac);
});

// Defining function to update layer 
$('#date_selection').change(function(){
    updatePrecipitationData();
    var selected_date_preip = $('#date_selection').val();
    document.getElementById('date_selection_ops').value = selected_date_preip;
    document.getElementById('date_selection_depth').value = selected_date_preip;
    document.getElementById('date_selection_age').value = selected_date_preip;
    document.getElementById('date_selection_simg').value = selected_date_preip;

    var selected_ops_date = $('#date_selection_ops').val(); 
    var popDate = new Date(selected_ops_date).toLocaleString('en-us',{month:'long', day:'numeric', year:'numeric'});
    var msg_date = document.getElementById('mesg-date');
        msg_date.innerHTML = popDate;   
});
$('#cmap_selection').change(function(){
    updatePrecipitationData();
});
$('#product_selection').change(function(){
    updatePrecipitationData();
});

// Defining function to update precipitation map
function updatePrecipitationData(){
    $("#precipCB").prop("checked", true);
    $("#loader").show();
    var prod = $('#product_selection').val();
    var cmap = $('#cmap_selection').val();
    var accum = prod.split('|')[0];
    var selected_date = $('#date_selection').val();
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
            //console.log(precip_data);
            precip_layer.setUrl(precip_data);  
            map.addLayer(precip_layer);
            $("#loader").hide();
            setTimeout(function() { $("#loader").hide(); }, 8000);
        },
        error: (error) => {
            console.log(error);
            $("#error-overlay").css({ display: "block" });
            $("#loader").hide();
        }
    });
}

///////////////////////////////////////////////////////////////////////////////////////////

/* =============================== Flood Age Layer ================================ */

// Define Earth Engine Precipitation Layer in Leaflet
var fage_layer = L.tileLayer('', {
    attribution: '&copy; <a href="https://earthengine.google.com" target="_blank">Google Earth Engine</a> contributors'
});
// Get Flood Age Layer
$("#floodageCB").on("click", function(){
    if(this.checked) {
        updateFloodAgeMapLayer();    
    }
    else {
        map.removeLayer(fage_layer);
    }
});  

$("#fage-opacity").on("slide", function(slideEvt) {
    var opac = slideEvt.value
    fage_layer.setOpacity(opac);
});

// Defining function to update flood age layer 
// $('#age_type_selection').change(function(){
//     updateFloodAgeMapLayer();
// });
$('#date_selection_age').change(function(){
    updateFloodAgeMapLayer();
    var selected_age_date = $('#date_selection_age').val();
    document.getElementById('date_selection_ops').value = selected_age_date;
    document.getElementById('date_selection_depth').value = selected_age_date;
    document.getElementById('date_selection_simg').value = selected_age_date;
    document.getElementById('date_selection').value = selected_age_date;

    var selected_ops_date = $('#date_selection_ops').val(); 
    var popDate = new Date(selected_ops_date).toLocaleString('en-us',{month:'long', day:'numeric', year:'numeric'});
    var msg_date = document.getElementById('mesg-date');
        msg_date.innerHTML = popDate;   
});
$('#age_sensor_selection').change(function(){
    updateFloodAgeMapLayer();
});

// Defining function to update flood age layer
function updateFloodAgeMapLayer(){
    $("#floodageCB").prop("checked", true);
    $("#loader").show();
    // var selected_age_type = $('#age_type_selection').val();
    var selected_age_date = $('#date_selection_age').val();
    var selected_age_sensor = $('#age_sensor_selection').val();
    $.ajax({
        url: '/ajax/floodagemap/',
        type: "GET",
        data: {
            // "selected_age_type": selected_age_type,
            "age_date": selected_age_date,
            "selected_age_sensor": selected_age_sensor
        },
        dataType: 'json',
        // async: false,
        success: (fage_data) => {
            fage_layer.setUrl(fage_data); 
            map.addLayer(fage_layer);
            $("#loader").hide();
            setTimeout(function() { $("#loader").hide(); }, 8000);
        },
        error: (error) => {
            console.log(error);
            $("#loader").hide();
        }
    });
}

///////////////////////////////////////////////////////////////////////////////

/* ====================== Permanent Water Layer ============================ */
// Define monthly range slider
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
// var wcolor = $('#color-picker-water').val();
// var geom = JSON.stringify(drawing_polygon);
if (startMonth === endMonth) { endMonth += 1; }

// Define Earth Engine Permanent Water Layer in Leaflet
var historical_layer = L.tileLayer('', {
    attribution: '&copy; <a href="https://earthengine.google.com" target="_blank">Google Earth Engine</a> contributors'
});

// Check add or remove historical layer to overlay on map 
$("#permanentwaterCB").on("click",function(){
    if(this.checked) {
        updatePermanentWater(); 
        $('#map-overlay').hide()              
    } else {
        map.removeLayer(historical_layer); 
        $('#map-overlay').show()
    }
});  

$("#historical-opacity").on("slide", function(slideEvt) {
    var opac = slideEvt.value
    historical_layer.setOpacity(opac);
});

// Update permanent water area layer by changing parameters
$("#update-button").on("click",function(){
    updatePermanentWater();
}); 

// Defining function to update permanent water layer
function updatePermanentWater(){
    $("#permanentwaterCB").prop("checked", true);
    $("#loader").show();
    // Get values
    var startYear = $('#start_year_selection_historical').val();
    var endYear = $('#end_year_selection_historical').val();
    var slider = $("#month_range").data("ionRangeSlider");  
    var startMonth = slider.result.from + 1;
    var endMonth= slider.result.to + 1;
    var method = 'discrete';
    //var wcolor = $('#color-picker-water').val();
    //var geom = JSON.stringify(drawing_polygon);

    if (startMonth === endMonth) { endMonth += 1; }

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
            historical_layer.setUrl(historical_data);
            map.addLayer(historical_layer);
            $("#loader").hide();
            setTimeout(function() { $("#loader").hide(); }, 20000);
        },
        error: (error) => {
            console.log(error);
            $("#loader").hide();
        }
    });
}

/////////////////////////////////////////////////////////////////////////////////////

/* ================== Raw Sattelite Imagery Layer =================== */

// var selected_date = $('#date_selection').val();
// var viirs_product = "VIIRS_SNPP_CorrectedReflectance_BandsM11-I2-I1";
// var browse_layer = addGibsLayer(browse_layer);//,viirs_product,selected_date
// Check add or remove selected raw satellite imagery to overlay on map 
var browse_layer = L.tileLayer('', {
    // layer: id,
    tileMatrixSet: 'GoogleMapsCompatible_Level9',
    maxZoom: 14,
    // time: selected_date,
    tileSize: 256,
    subdomains: 'abc',
    noWrap: true,
    continuousWorld: true,
    // Prevent Leaflet from retrieving non-existent tiles on the
    // borders.
    bounds: [
        [-85.0511287776, -179.999999975],
        [85.0511287776, 179.999999975]
    ],
    attribution: '&copy; <a href="https://wiki.earthdata.nasa.gov/display/GIBS" target="_">' +
    'NASA EOSDIS GIBS | Google Earth Engine</a>;'
});

$("#gibsCB").on("click",function(){
    if(this.checked){
        updateBrowseData();
    }
    else{
        map.removeLayer(browse_layer);
    }
});

/**
    * Change NRT Browse Imagery opacity
*/

$("#browse-opacity").on("slide", function(slideEvt) {
    var opac = slideEvt.value
    browse_layer.setOpacity(opac);
});

/**
    * Change NRT Browse Imagery
*/
$('#browse_selection').change(function(){
    updateBrowseData();
});

$('#date_selection_simg').change(function(){
    updateBrowseData();
    var selected_date_simg = $('#date_selection_simg').val();
    document.getElementById('date_selection_ops').value = selected_date_simg;
    document.getElementById('date_selection_depth').value = selected_date_simg;
    document.getElementById('date_selection_age').value = selected_date_simg;
    document.getElementById('date_selection').value = selected_date_simg;

    var selected_ops_date = $('#date_selection_ops').val(); 
    var popDate = new Date(selected_ops_date).toLocaleString('en-us',{month:'long', day:'numeric', year:'numeric'});
    var msg_date = document.getElementById('mesg-date');
        msg_date.innerHTML = popDate;   
});

// Update satellite imagery data by changing date
function updateBrowseData() {
    // if(map.hasLayer(browse_layer)){
    //     map.removeLayer(browse_layer);
    // }
    $("#loader").show();
    $("#gibsCB").prop("checked", true);
    var selected_date = $('#date_selection_simg').val();
    // console.log(selected_date)
    var prod = $('#browse_selection').val();
    var id = prod.split('|')[1];
    var template =
    '//gibs-{s}.earthdata.nasa.gov/wmts/epsg3857/best/' +
    id + '/default/' + selected_date + '/{tileMatrixSet}/{z}/{y}/{x}.jpg';
    browse_layer.setUrl(template);
    map.addLayer(browse_layer);
    // browse_layer.bringToBack();
    $("#loader").hide();
    setTimeout(function() { $("#loader").hide(); }, 20000);
}
///////////////////////////////////////////////////////
browse_layer.setZIndex(1);
precip_layer.setZIndex(2);
fage_layer.setZIndex(3);
depth_layer.setZIndex(4);
fld_layer.setZIndex(5);
/* ================= Feature Layer ========================== */
var adm0Style = {
    color: 'rgba(200, 230, 201, 1)',
    weight: 0.4,
    fillOpacity: 0.0,
    fillColor: "rgba(200, 230, 201, 1)",
};

var adm1Style = {
    color: "#bdbdbd",
    weight: 0.3,
    fillOpacity: 0.0,
    fillColor: "#bdbdbd",
};

var adm2Style = {
    color: "#fff9c4",
    weight: 0.2,
    fillOpacity: 0.0,
    fillColor: "#ffc107",
    cursor: 'pointer'
};

// highlight admin feature style
var highlightStyle = {
    color: '#ffc107', 
    weight: 1.5,
    fillOpacity: 0.0,
    fillColor: '#ffc107'
};

// function zoomToFeature(e) {
//     map.fitBounds(e.target.getBounds());
// }

var adm0_layer = L.geoJson(adm0, {
    style: adm0Style,
    onEachFeature: function(feature, admin0Layer) {
        // admin0Layer.on('mouseover', function (e) {
        //     this.setStyle(highlightStyle);
        //     this.bindPopup('<p style="padding-top: 5px;">'+ feature.properties.NAME_0+'</p>');
        // }); 
        // admin0Layer.on('mouseout', function (e) {
        //     this.setStyle(adm0Style);
        // }); 
        // admin0Layer.on('click', function(){
        //     map.fitBounds(feature.getBounds());
        // });  
        admin0Layer.on('click', function(e){
            map.fitBounds(e.target.getBounds());
        });    
    } 
}).addTo(map);

var adm1_layer = L.geoJson(adm1, {
    style: adm1Style,
    onEachFeature: function(feature, admin1Layer) {
        admin1Layer.on('mouseover', function (e) {
            this.setStyle(highlightStyle);
            this.bindTooltip(feature.properties.NAME_1);
        }); 
        admin1Layer.on('mouseout', function (e) {
            this.setStyle(adm1Style);
        });  
        admin1Layer.on('click', function(e){
            map.fitBounds(e.target.getBounds());
        });    
    } 
}); 

var adm2_layer = L.geoJson(adm2, {
    style: adm2Style,
    onEachFeature: function(feature, adm2Layer){

        // Display a popup with the name of the county.
        var district = feature.properties.NAME_2;
        var province = feature.properties.NAME_1;
        var country = feature.properties.NAME_0;
        var f_0_15 = feature.properties.F_0_15;
        var f_15_65 = feature.properties.F_15_65;
        var f_above_65 = feature.properties.F__65;
        var f_total = f_0_15 + f_15_65 + f_above_65;
        var m_0_15 = feature.properties.M_0_15;
        var m_15_65 = feature.properties.M_15_65;
        var m_above_65 = feature.properties.M__65;    
        var m_total = m_0_15+m_15_65+m_above_65;
        var hospitals = feature.properties.Hospitals;
        var primary = feature.properties.Primary;
        var secondary = feature.properties.Secondary;
        var trunks = feature.properties.Trunks;

        adm2Layer.on('mouseover', function (e) {
            this.setStyle(highlightStyle);
            this.bindPopup( 
                '<h4 style="margin-top: 20px; font-weight: bold; margin-bottom: 0px;">'+district+': '+province+', '+country+'</h4>'+
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
                                '<td>'+"Total"+'</td>'+
                                '<td>'+f_total+'</td>'+
                                '<td>'+m_total+'</td>'+
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
                '</div>'
            );
            // this.bindTooltip(feature.properties.NAME_2);
        }); 
        adm2Layer.on('mouseout', function (e) {
            this.setStyle(adm2Style);
        }); 
        adm2Layer.on('click', function(e){
            map.fitBounds(e.target.getBounds());
            // animate: true;
        });        
    }
});

map.on('mouseover zoomend', function() {
    if(map.getZoom() >= 7 ) {
        map.removeLayer(adm0_layer);
        $("#adm0CB").prop("checked", false);
    } else {
        map.addLayer(adm0_layer);
        $("#adm0CB").prop("checked", true);
    }
});
map.on('mouseover zoomend', function() {
    if(map.getZoom() <= 6) {
        map.removeLayer(adm1_layer);
        $("#adm1CB").prop("checked", false);
    } else {
        map.addLayer(adm1_layer);
        $("#adm1CB").prop("checked", true);
    }
});
map.on('mouseover zoomend', function() {
    if(map.getZoom() >= 8) {
        map.removeLayer(adm1_layer);
        $("#adm1CB").prop("checked", false);
    }
});
map.on('mouseover zoomend', function() {
    if(map.getZoom() < 8) {
        map.removeLayer(adm2_layer);
        $("#adm2CB").prop("checked", false);
    } else {
        map.addLayer(adm2_layer);
        $("#adm2CB").prop("checked", true);
    }
});

$("#adm0CB").on("click",function(){
    if(this.checked){
        map.addLayer(adm0_layer);
    }
    else{
        map.removeLayer(adm0_layer);
    }
});
$("#adm1CB").on("click",function(){
    if(this.checked){
        map.addLayer(adm1_layer);
    }
    else{
        map.removeLayer(adm1_layer);
    }
});
$("#adm2CB").on("click",function(){
    if(this.checked){
        map.addLayer(adm2_layer);
    }
    else{
        map.removeLayer(adm2_layer);
    }
});

// Icon options
var iconOptions = {
    iconUrl: '/static/images/hospital.png',
    iconSize: [10, 10]
}

// Creating a custom icon
var hospitalIcon = L.icon(iconOptions);

var hospital_layer = L.geoJson(hospital, {
    pointToLayer: function(point, latlng) {
        return L.marker(latlng, {icon: hospitalIcon});
    },
    // onEachFeature: popUp
}); 
map.on('mouseover zoomend', function() {
    if(map.getZoom() <= 12) {
        map.removeLayer(hospital_layer);
    } else {
        map.addLayer(hospital_layer);
    }
});


// Icon options
var eduIconOptions = {
    iconUrl: '/static/images/education.png',
    iconSize: [10, 10]
}

// Creating a custom icon
var eduIcon = L.icon(eduIconOptions);

var education_layer = L.geoJson(education, {
    pointToLayer: function(point, latlng) {
        return L.marker(latlng, {icon: eduIcon});
    },
    // onEachFeature: popUp
}); 

map.on('mouseover zoomend', function() {
    if(map.getZoom() <= 12) {
        map.removeLayer(education_layer);
    } else {
        map.addLayer(education_layer);
    }
});

// $("#adm2CB").on("click",function(){
//     if(this.checked){
//         map.addLayer(adm2_layer);
//     }
//     else{
//         map.removeLayer(adm2_layer);
//     }
// });