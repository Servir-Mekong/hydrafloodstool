var event_date = document.getElementById('eventDate');
var pfa_cambodia = document.getElementById('cambodiaFldArea');
var pfa_laos = document.getElementById('laosFldArea');
var pfa_myanmar = document.getElementById('myanmarFldArea');
var pfa_thailand = document.getElementById('thailandFldArea');
var pfa_vietnam = document.getElementById('vietnamFldArea');
var pfa_all = document.getElementById('totalFldArea');

var pfhc_cambodia = document.getElementById('cambodiaFldedHC');
var pfhc_laos = document.getElementById('laosFldedHC');
var pfhc_myanmar = document.getElementById('myanmarFldedHC');
var pfhc_thailand = document.getElementById('thailandFldedHC');
var pfhc_vietnam = document.getElementById('vietnamFldedHC');
var pfhc_total = document.getElementById('totalFldedHC');

var pfec_cambodia = document.getElementById('cambodiaFldedEC');
var pfec_laos = document.getElementById('laosFldedEC');
var pfec_myanmar = document.getElementById('myanmarFldedEC');
var pfec_thailand = document.getElementById('thailandFldedEC');
var pfec_vietnam = document.getElementById('vietnamFldedEC');
var pfec_total = document.getElementById('totalFldedEC');
   
// Cambodia Potential Flooded Area
var cambodia_fld_data;
var cambodia_flded_area;
$.ajax({
    type: "GET",
    url: "/ajax/cambodiafloodedarea/",
    dataType: 'json',
    async: false,
    success: function(response){
        //console.log(response);
        cambodia_fld_data = JSON.parse(response);
        //console.log(cambodia_fld_data)
        for (var i=0; i<cambodia_fld_data.length; i++){
            event_date.innerHTML = cambodia_fld_data[i].Date
            cambodia_flded_area = cambodia_fld_data[i].TotalAreainSqKm
            pfa_cambodia.innerHTML = cambodia_fld_data[i].TotalAreainSqKm
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Laos Potential Flooded Area
var laos_fld_data;
var laos_flded_area;
$.ajax({
    type: "GET",
    url: "/ajax/laosfloodedarea/",
    dataType: 'json',
    async: false,
    success: function(response){
        //console.log(response);
        laos_fld_data = JSON.parse(response);
        //console.log(data)
        for (var i=0; i<laos_fld_data.length; i++){
            laos_flded_area = laos_fld_data[i].TotalAreainSqKm
            pfa_laos.innerHTML = laos_fld_data[i].TotalAreainSqKm
        }
    },
    error: function(error) {
        console.log(error);
    }
});
// console.log(laos_fld_data)
console.log(laos_flded_area);

// Myanmar Potential Flooded Area
var myanmar_fld_data;
var myanmar_flded_area;
$.ajax({
    type: "GET",
    url: "/ajax/myanmarfloodedarea/",
    dataType: 'json',
    async: false,
    success: function(response){
        //console.log(response);
        myanmar_fld_data = JSON.parse(response);
        //console.log(myanmar_fld_data)
        for (var i=0; i<myanmar_fld_data.length; i++){
            myanmar_flded_area = myanmar_fld_data[i].TotalAreainSqKm
            pfa_myanmar.innerHTML = myanmar_fld_data[i].TotalAreainSqKm
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Thailand Potential Flooded Area
var thailand_fld_data;
var thailand_flded_area;
$.ajax({
    type: "GET",
    url: "/ajax/thailandfloodedarea/",
    dataType: 'json',
    async: false,
    success: function(response){
        //console.log(response);
        thailand_fld_data = JSON.parse(response);
        //console.log(thailand_fld_data)
        for (var i=0; i<thailand_fld_data.length; i++){
            thailand_flded_area = thailand_fld_data[i].TotalAreainSqKm
            pfa_thailand.innerHTML = thailand_fld_data[i].TotalAreainSqKm
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Vietnam Potential Flooded Area
var vietnam_fld_data;
var vietnam_flded_area;
$.ajax({
    type: "GET",
    url: "/ajax/vietnamfloodedarea/",
    dataType: 'json',
    async: false,
    success: function(response){
        //console.log(response);
        vietnam_fld_data = JSON.parse(response);
        //console.log(vietnam_fld_data)
        for (var i=0; i<vietnam_fld_data.length; i++){
            vietnam_flded_area = vietnam_fld_data[i].TotalAreainSqKm
            pfa_vietnam.innerHTML = vietnam_fld_data[i].TotalAreainSqKm
        }
    },
    error: function(error) {
        console.log(error);
    }
});

var total_flded_area = cambodia_flded_area + laos_flded_area + myanmar_flded_area + thailand_flded_area + vietnam_flded_area;
// console.log(total_flded_area);
pfa_all.innerHTML = total_flded_area;

/* ================== Potential Number of Flooded Health Center ====================== */

// Cambodia - Number of Potential Flooded Health Center
var cambodia_hc_data;
$.ajax({
    type: "GET",
    url: "/ajax/cambodiafloodedhealthcenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        cambodia_hc_data = JSON.parse(response);
        //console.log(cambodia_hc_data)
        for (var i=0; i<cambodia_hc_data.length; i++){
            pfhc_cambodia.innerHTML = cambodia_hc_data[i].cambodiaFloodedHealthCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

//console.log(cambodia_hc_data)

// Laos - Number of Potential Flooded Health Center
var laos_hc_data;
$.ajax({
    type: "GET",
    url: "/ajax/laosfloodedhealthcenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        laos_hc_data = JSON.parse(response);
        //console.log(data)
        for (var i=0; i<laos_hc_data.length; i++){
            pfhc_laos.innerHTML = laos_hc_data[i].laosFloodedHealthCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Myanmar - Number of Potential Flooded Health Center
var myanmar_hc_data;
$.ajax({
    type: "GET",
    url: "/ajax/myanmarfloodedhealthcenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        myanmar_hc_data = JSON.parse(response);
        //console.log(myanmar_hc_data)
        for (var i=0; i<myanmar_hc_data.length; i++){
            pfhc_myanmar.innerHTML = myanmar_hc_data[i].myanmarFloodedHealthCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Thailand - Number of Potential Flooded Health Center
var thailand_hc_data;
$.ajax({
    type: "GET",
    url: "/ajax/thailandfloodedhealthcenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        thailand_hc_data = JSON.parse(response);
        //console.log(data)
        for (var i=0; i<thailand_hc_data.length; i++){
            pfhc_thailand.innerHTML = thailand_hc_data[i].thailandFloodedHealthCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Vietnam - Number of Potential Flooded Health Center
var vietnam_hc_data;
$.ajax({
    type: "GET",
    url: "/ajax/vietnamfloodedhealthcenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        vietnam_hc_data = JSON.parse(response);
        //console.log(vietnam_hc_data)
        for (var i=0; i<vietnam_hc_data.length; i++){
            pfhc_vietnam.innerHTML = vietnam_hc_data[i].vietnamFloodedHealthCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

//console.log(vietnam_hc_data);

// Total - Number of Potential Flooded Health Center
for (var i=0; i<cambodia_hc_data.length; i++){
    pfhc_cambodia = cambodia_hc_data[0].cambodiaFloodedHealthCenter
}
for (var i=0; i<laos_hc_data.length; i++){
    pfhc_laos = laos_hc_data[0].laosFloodedHealthCenter
}
for (var i=0; i<myanmar_hc_data.length; i++){
    pfhc_myanmar = myanmar_hc_data[0].myanmarFloodedHealthCenter
}
for (var i=0; i<thailand_hc_data.length; i++){
    pfhc_thailand = thailand_hc_data[0].thailandFloodedHealthCenter
}
for (var i=0; i<vietnam_hc_data.length; i++){
    pfhc_vietnam = vietnam_hc_data[0].vietnamFloodedHealthCenter
}
// console.log(pfhc_cambodia);
// console.log(pfhc_laos);
// console.log(pfhc_myanmar);
// console.log(pfhc_thailand);
// console.log(pfhc_vietnam);

var total_flooded_hc = pfhc_cambodia + pfhc_laos + pfhc_myanmar + pfhc_thailand + pfhc_vietnam;
// console.log(total_flooded_hc)
pfhc_total.innerHTML = total_flooded_hc;

/* ================== Potential Number of Flooded Education Center ====================== */

// Cambodia - Number of Potential Flooded Education Center
var cambodia_ec_data;
$.ajax({
    type: "GET",
    url: "/ajax/cambodiafloodededucenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        cambodia_ec_data = JSON.parse(response);
        //console.log(data)
        for (var i=0; i<cambodia_ec_data.length; i++){
            pfec_cambodia.innerHTML = cambodia_ec_data[i].cambodiaFloodedEducationCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Laos - Number of Potential Flooded Education Center
var laos_ec_data;
$.ajax({
    type: "GET",
    url: "/ajax/laosfloodededucenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        laos_ec_data = JSON.parse(response);
        //console.log(laos_ec_data)
        for (var i=0; i<laos_ec_data.length; i++){
            pfec_laos.innerHTML = laos_ec_data[i].laosFloodedEducationCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Myanmar - Number of Potential Flooded Education Center
var myanmar_ec_data;
$.ajax({
    type: "GET",
    url: "/ajax/myanmarfloodededucenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        myanmar_ec_data = JSON.parse(response);
        //console.log(myanmar_ec_data)
        for (var i=0; i<myanmar_ec_data.length; i++){
            pfec_myanmar.innerHTML = myanmar_ec_data[i].myanmarFloodedEducationCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Thailand - Number of Potential Flooded Education Center
var thailand_ec_data;
$.ajax({
    type: "GET",
    url: "/ajax/thailandfloodededucenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        thailand_ec_data = JSON.parse(response);
        //console.log(data)
        for (var i=0; i<thailand_ec_data.length; i++){
            pfec_thailand.innerHTML = thailand_ec_data[i].thailandFloodedEducationCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Vietnam - Number of Potential Flooded Education Center
var vietnam_ec_data;
$.ajax({
    type: "GET",
    url: "/ajax/vietnamfloodededucenter/",
    dataType: 'json',
    'async': false,
    success: function(response){
        //console.log(response);
        vietnam_ec_data = JSON.parse(response);
        //console.log(vietnam_ec_data)
        for (var i=0; i<vietnam_ec_data.length; i++){
            pfec_vietnam.innerHTML = vietnam_ec_data[i].vietnamFloodedEducationCenter
        }
    },
    error: function(error) {
        console.log(error);
    }
});

// Total - Number of Potential Flooded Education Center
for (var i=0; i<cambodia_ec_data.length; i++){
    pfec_cambodia = cambodia_ec_data[0].cambodiaFloodedEducationCenter
}
for (var i=0; i<laos_ec_data.length; i++){
    pfec_laos = laos_ec_data[0].laosFloodedEducationCenter
}
for (var i=0; i<myanmar_ec_data.length; i++){
    pfec_myanmar = myanmar_ec_data[0].myanmarFloodedEducationCenter
}
for (var i=0; i<thailand_ec_data.length; i++){
    pfec_thailand = thailand_ec_data[0].thailandFloodedEducationCenter
}
for (var i=0; i<vietnam_ec_data.length; i++){
    pfec_vietnam = vietnam_ec_data[0].vietnamFloodedEducationCenter
}
// console.log(pfec_cambodia);
// console.log(pfec_laos);
// console.log(pfec_myanmar);
// console.log(pfec_thailand);
// console.log(pfec_vietnam);

var total_flooded_ec = pfec_cambodia + pfec_laos + pfec_myanmar + pfec_thailand + pfec_vietnam;
// console.log(total_flooded_ec)
pfec_total.innerHTML = total_flooded_ec;