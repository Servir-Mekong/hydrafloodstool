
mapboxgl.accessToken = 'pk.eyJ1Ijoia2FtYWxoMjciLCJhIjoiY2t0bG1qMnJ5MDh0YzJ3czRiOHB1dXVwZiJ9.RHfxuNLtYaycA39uKjhARw';

var sidenav = document.querySelector('#home');
var sidebarContent = document.querySelector('#sidebar-content');
var closeHomeSidebarContent = document.querySelector("#close-home-content" );
var closeLayerSidebarContent = document.querySelector("#close-layer-content" );
var closeBasemapSidebarContent = document.querySelector("#close-basemap-content" );


var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [95.9560, 21.9162], // starting position [lng, lat]
    zoom: 5 // starting zoom
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

function showNavHomeContent(){
    if (sidebarContent.style.display === "none"){
        sidebarContent.style.display ="block";
        sidebarContent.style.width = "350px";
        sidebarContent.style.marginLeft = "60px";
    } else if (sidebarContent.style.display === "block"){
        sidebarContent.style.width = "350px";
        sidebarContent.style.marginLeft = "60px";
    }else {
        sidebarContent.style.display = "none";
    }
}

function showNavLayerContent(){
    if (sidebarContent.style.display === "none"){
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

function showNavBasemapContent(){
    if (sidebarContent.style.display === "none"){
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



// var basemap_layer = mapboxgl.tiles('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// }).addTo(map);

var basemap_layer = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

$(document).ready(function() {
    $(".basemap-card").click(function () {
        $(".basemap-card").removeClass("active");
        // $(".tab").addClass("active"); // instead of this do the below 
        $(this).addClass("active");   
    });
});

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
    // if(selected_basemap === "osm"){
    //     basemap_layer.setUrl('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');   
    // }else if((selected_basemap === "street")){
    //     basemap_layer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}');
    // }else if(selected_basemap === "satellite"){
    //     basemap_layer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}');
    // }else if(selected_basemap === "terrain"){
    //     basemap_layer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}');
    // }
    // else if(selected_basemap === "topo"){
    //     basemap_layer.setUrl('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png');
    // }
    // else if(selected_basemap === "dark"){
    //     basemap_layer.setUrl('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png');
    // }
    // else if(selected_basemap === "gray"){
    //     basemap_layer.setUrl('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}');
    // } 

});

//slider
// Without JQuery
var slider_precip = new Slider('#precip-opacity', {
	formatter: function(value) {
		return value;
	}
});
var slider_flood1 = new Slider('#flood1-opacity', {
	formatter: function(value) {
		return value;
	}
});
var slider_historical = new Slider('#historical-opacity', {
	formatter: function(value) {
		return value;
	}
});
var slider_browse = new Slider('#browse-opacity', {
	formatter: function(value) {
		return value;
	}
});


// get datelist
$.ajax({
    url: '/ajax/date/',
    type: "GET",
    dataType: "json",
    success: (data) => {
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

