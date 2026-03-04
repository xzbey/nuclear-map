var iconNuke = L.icon({
    iconUrl: 'icons/nuke.png',
    iconSize: [64, 64]
}),
    iconTestNuke = L.icon({
    iconUrl: 'icons/test_nuke.png',
    iconSize: [32, 32]
}),
    iconNone = L.icon({
    iconUrl: 'icons/none.png',
    iconSize: [32, 32]
});

var allFeatures = [],
    map,
    downloadingCount = 0,
    currentLayer = null,
    tyleLayer = null;

var name = ' contributors | <a href="https://github.com/xzbey/nuclear-map">/xzbey</a>';
var tyleLayers = {
    'osm': {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' + name
    },
    /*'google': {
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
    },*/ 
    // Они под лицензией, но если что можно включить
    'dark': {
        url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>' + name
    },
    'satellite': {
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attribution: '&copy; Esri Satellite' + name
    },
    'topo': {
        url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attribution: '&copy; OpenTopoMap' + name
    }
};

function switchTileLayer(name) { // Функция переключение типа карты по названию (console.log('*'))
    let key = name.toLowerCase().trim(),
        layer = tyleLayers[key];
    
    if (!layer) return;

    if (tyleLayer) {
        map.removeLayer(tyleLayer);
    }

    tyleLayer = L.tileLayer(layer.url, {
        attribution: layer.attribution,
        maxZoom: 19,
        minZoom: 2
    }).addTo(map);
}

function hasValidCoordinates(feature) { // Функция проверки наличия и правильности координат
    let coords = feature.geometry && feature.geometry.coordinates;
    if (!coords || coords.length < 2) {
        return false;
    }
    let lon = parseFloat(coords[0]),
        lat = parseFloat(coords[1]);

    return typeof lon === 'number' && typeof lat === 'number' && isFinite(lon) && isFinite(lat);
}

function createMap() { // Функция создания карты
    map = L.map('map').setView([0, 0], 2);

    tyleLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | <a href="https://github.com/xzbey/nuclear-map">/xzbey</a>',
        maxZoom: 19,
        minZoom: 2
    }).addTo(map);

    return map;
}

function loadGeoJson(url) { // Функция загрузки одного GeoJSON и добавления в список
    downloadingCount++;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.features) {
                allFeatures = allFeatures.concat(data.features);
            }
        })
        .catch(error => console.error('Ошибка загрузки GeoJSON:', error))
        .finally(() => {
            downloadingCount--;
            if (downloadingCount === 0) {
                applyFilters();
            }
        });
}

function renderMarkers(features) { // Функция отображения маркеров на карте с учетом фильтров
    if (currentLayer) {
        map.removeLayer(currentLayer);
    }

    let validFeatures = features.filter(hasValidCoordinates);

    currentLayer = L.geoJSON({type: 'FeatureCollection', features: validFeatures}, {
        pointToLayer: function (feature, latlng) {
            let icon;
            if (feature.properties.impact === 'strike') {
                icon = iconNuke;
            } else if (feature.properties.impact === 'test') {
                icon = iconTestNuke;
            } else {
                icon = iconNone;
            }
            return L.marker(latlng, {
                icon: icon,
                title: `${feature.properties.country} / ${feature.properties.site}`
            });
        },
        onEachFeature: function (feature, layer) {
            layer.bindPopup(`<b>Series: ${feature.properties.series} / Shot: ${feature.properties.shot}</b><br>
                            Date: ${feature.properties.date} / Time: ${feature.properties.time}<br>
                            Site: ${feature.properties.site}<br><br>
                            Type: ${feature.properties.type}<br>
                            Purpose: ${feature.properties.purpose}<br>
                            Yield (kt): ${feature.properties.yield}<br>
                            Crater (m): ${feature.properties.crater}<br>
                            Warhead: ${feature.properties.warhead}<br>
                            Sponsor: ${feature.properties.sponsor}<br><br>
                            <i>Strike by: ${feature.properties.country} / Impact: ${feature.properties.impact}</i>`);
        }
    }).addTo(map);
}

function applyFilters() { // Функция применения фильтров
    let selectedCountry = document.getElementById('country-filter').value,
        selectedYear = parseInt(document.getElementById('yearSlider').value);

    let filtered = allFeatures.filter(feature => {
        if (selectedCountry !== 'All' && feature.properties.country !== selectedCountry) {
            return false;
        }
        
        if (feature.properties.date) {
            let year = parseInt(feature.properties.year);
            if (!isNaN(year) && year > selectedYear) {
                return false;
            }
        }
        return true;
    });
    renderMarkers(filtered);
    document.getElementById('yearValue').textContent = selectedYear;
}

function placeMarkers() { // Функция загрузки всех GeoJSON
    let paths = [
        '../db/geojson/USA-ntests1.geojson',
        '../db/geojson/USA-ntests2.geojson',
        '../db/geojson/USA-ntests3.geojson',
        '../db/geojson/USSR-ntests1.geojson',
        '../db/geojson/USSR-ntests2.geojson',
        '../db/geojson/USSR-ntests3.geojson',
        '../db/geojson/UK-ntests1.geojson',
        '../db/geojson/FR-ntests1.geojson',
        '../db/geojson/PRC-ntests1.geojson',
        '../db/geojson/OTH-ntests1.geojson'
    ]
    for (let path of paths) {
        loadGeoJson(path);
    }
}

document.addEventListener('DOMContentLoaded', function () { // Установка обработчиков событий
    document.getElementById('country-filter').addEventListener('change', applyFilters);
    document.getElementById('yearSlider').addEventListener('input', applyFilters);
});

let originalConsoleLog = console.log; // Функция переключения типа карты (console.log('*'))
console.log = function(...args) {
    originalConsoleLog.apply(console, args);
    switchTileLayer(args.join(' '));
};