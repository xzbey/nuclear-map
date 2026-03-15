function checkStrikeDetails(feature) {
    let text = `<p><b>Series: ${feature.properties.series} / Shot: ${feature.properties.shot}</b><br>` +
            `Date: ${feature.properties.date} / Time: ${feature.properties.time}<br>` +
            `Site: ${feature.properties.site}<br></p>`


    if (feature.properties.type != "Unknown")
        text += `Type: ${feature.properties.type}<br>`;

    if (feature.properties.purpose != "Unknown")
        text += `Purpose: ${feature.properties.purpose}<br>`;

    let yield_ = checkYield(feature.properties.yield)
    if (yield_ != "")
        text += `Yield (kt): ${yield_}<br>`;


    if (feature.properties.crater != "Unknown" && !isNaN(feature.properties.crater))
        text += `Crater (m): ${feature.properties.crater} m<br>`;

    if (feature.properties.warhead != "Unknown")
        text += `Warhead: ${feature.properties.warhead}<br>`;

    if (feature.properties.sponsor != "Unknown")
        text += `Sponsor: ${feature.properties.sponsor}<br>`;

    text += `<p><i>Strike by: ${feature.properties.country} / Impact: ${feature.properties.impact}</i></p>`;

    return text;
}

function checkYield(str) {
    str = str.replace('min: Unknown, ', '');
    str = str.replace(', max: Unknown', '');
    str = str.replace('max: Unknown', '');

    return str;
}



var isize = [25, 25]
var iconUSSR = L.icon({
        iconUrl: 'icons/USSR.png',
        iconSize: isize
    }),
    iconUSA = L.icon({
        iconUrl: 'icons/USA.png',
        iconSize: isize
    }),
    iconUK = L.icon({
        iconUrl: 'icons/UK.png',
        iconSize: isize
    }), 
    iconFR = L.icon({
        iconUrl: 'icons/FRANCE.png',
        iconSize: isize
    }), 
    iconPRC = L.icon({
        iconUrl: 'icons/CHINA.png',
        iconSize: isize
    }), 
    iconIndia = L.icon({
        iconUrl: 'icons/INDIA.png',
        iconSize: isize
    }), 
    iconPakistan = L.icon({
        iconUrl: 'icons/PAKISTAN.png',
        iconSize: isize
    }), 
    iconNKorea = L.icon({
        iconUrl: 'icons/NORTH-KOREA.png',
        iconSize: isize
    }), 
    iconSAfrica = L.icon({
        iconUrl: 'icons/SOUTH-AFRICA.png',
        iconSize: isize
    }),
    iconNone = L.icon({
        iconUrl: 'icons/none.png',
        iconSize: isize
    });

var name = ' contributors | <a href="https://github.com/xzbey/nuclear-map">/xzbey</a>';
var tyleLayers = {
    'osm': {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' + name,
        maxZoom: 19,
    },
    /*
    'google': {
        url: 'https://mt1.google.com/vt/lyrs=r&x={x}&y={y}&z={z}',
        attribution: '&copy; Google Maps' + name
    },
    'google satellite': {
        url: 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attribution: '&copy; Google Satellite' + name
    },
    'yandex': {
        url: 'https://core-renderer-tiles.maps.yandex.net/tiles?l=map&x={x}&y={y}&z={z}',
        attribution: '&copy; Яндекс Карты' + name
    },
    */
    // Они под лицензией, но если что можно включить
    'dark': {
        url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>' + name,
        maxZoom: 19
    },
    'satellite': {
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attribution: '&copy; Esri Satellite' + name,
        maxZoom: 19
    },
    'topo': {
        url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attribution: '&copy; OpenTopoMap' + name,
        maxZoom: 17
    }
};