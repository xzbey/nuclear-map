var allFeatures = [],
    map,
    downloadingCount = 0,
    currentLayer = null,
    tyleLayer = null;


function switchTileLayer(name) { // Функция переключение типа карты по названию (console.log('*'))
    let key = name.toLowerCase().trim(),
        layer = tyleLayers[key];
    
    if (!layer) return;

    if (tyleLayer) {
        map.removeLayer(tyleLayer);
    }

    tyleLayer = L.tileLayer(layer.url, {
        attribution: layer.attribution,
        maxZoom: layer.maxZoom || 19,
        minZoom: 2
    }).addTo(map);

    if (map.getZoom() > layer.maxZoom) {
        map.setZoom(layer.maxZoom);
    }
}


function createMap() { // Функция создания карты
    map = L.map('map').setView([0, 0], 2);

    layer = tyleLayers["satellite"]
    tyleLayer = L.tileLayer(layer.url, {
        attribution: layer.attribution,
        maxZoom: layer.maxZoom || 19,
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
    const clusterGroups = {};

    currentLayer = L.layerGroup();

    validFeatures.forEach(feature => {
        const country = feature.properties.country || "Unknown";

        if (!clusterGroups[country]) {
            clusterGroups[country] = L.markerClusterGroup({
                maxClusterRadius: 40
            });
            
            clusterGroups[country].on('clustermouseover', function (map_) {
                map_.layer.bindTooltip(country, { sticky: true }).openTooltip();
            });

            clusterGroups[country].on('clustermouseout', function (map_) {
                map_.layer.unbindTooltip();
            });

            currentLayer.addLayer(clusterGroups[country]);
        }
        
        const latlng = L.latLng(
            feature.geometry.coordinates[1],
            feature.geometry.coordinates[0]
        )

        const icons = {
            'USSR': iconUSSR, 'USA': iconUSA, 'UK': iconUK,
            'FR': iconFR, 'PRC': iconPRC, 'India': iconIndia,
            'Pakistan': iconPakistan, 'North Korea': iconNKorea,
            'Unknown (Republic of South Africa?)': iconSAfrica
            };
        const icon = icons[country] || iconNone;
        
        const marker = L.marker(latlng, {
            icon: icon,
            title: `${country} / ${feature.properties.site}`
        }).bindPopup(checkStrikeDetails(feature));

        clusterGroups[country].addLayer(marker);
    });

    currentLayer.addTo(map);

    map.setZoom(2);
}

function applyFilters() { // Функция применения фильтров
    let selectedCountry = document.getElementById('country-filter').value,
        selectedYear = parseInt(document.getElementById('yearSlider').value),
        selectedImpact = document.getElementById('strike-filter').value;

    let filtered = allFeatures.filter(feature => {
        if (selectedCountry !== 'All' && feature.properties.country !== selectedCountry) {
            return false;
        }

        if (selectedImpact !== 'All' && feature.properties.impact !== selectedImpact) {
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
    document.getElementById('strike-filter').addEventListener('change', applyFilters);
});

let originalConsoleLog = console.log; // Функция переключения типа карты (console.log('*'))
console.log = function(...args) {
    originalConsoleLog.apply(console, args);
    switchTileLayer(args.join(' '));
};