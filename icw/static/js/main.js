(function() {
    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    var osmAttrib='Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    var osm = new L.TileLayer(osmUrl, {minZoom: 3, maxZoom: 19, attribution: osmAttrib});
    var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3']
    });
    var googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
        maxZoom: 20,
        subdomains:['mt0','mt1','mt2','mt3']
    });
    var mapElems = document.getElementsByClassName('map');
    for (var i=0; i < mapElems.length; i++) {
        var mapElem = mapElems.item(i);
        map = L.map(mapElem, {
            layers: [osm]
        });
        map.setView(new L.LatLng(52, -1.2), 12);
        L.control.layers({
            "OpenStreetMap": osm,
            "Google Streets": googleStreets,
            "Google Satellite": googleSat
        }).addTo(map);

        if (mapElem.dataset.lat && mapElem.dataset.lon) {
            var latLng = new L.LatLng(mapElem.dataset.lat, mapElem.dataset.lon);
            var marker = L.marker(latLng).addTo(map);
            map.setView(latLng, 14);
        } else {
            map.setView(new L.LatLng(52, -1.2), 12);
        }



        var existingLayer = null;
        function loadData() {
            function onEachFeature(feature, layer) {
                // does this feature have a property named popupContent?
                if (feature.properties && feature.properties.name) {
                    layer.bindPopup(feature.properties.name);
                }
            }
            var url = mapElem.dataset.url;
            var bounds = map.getBounds();
            url = url + "?format=geojson&bbox=" + bounds.getWest() + "," + bounds.getSouth() + "," + bounds.getEast() + "," + bounds.getNorth();

            var xhr = new XMLHttpRequest();
            xhr.open("GET", url);
            xhr.addEventListener("load", function() {
                if (!this.response) return;
                if (existingLayer) {
                    map.removeLayer(existingLayer);
                }
                var layer = L.geoJSON(JSON.parse(this.response), {
                    pointToLayer: function (feature, latlng) {
                        var fillColor;
                        switch (feature.properties.severity) {
                            case 1: fillColor = "#ff1800"; break;
                            case 2: fillColor = "#ff7800"; break;
                            case 3: fillColor = "#fff800"; break;
                        }
                        var geojsonMarkerOptions = {
                            radius: 8,
                            fillColor: fillColor,
                            color: "#000",
                            weight: 1,
                            opacity: 1,
                            fillOpacity: 0.8
                        };
                        return L.circleMarker(latlng, geojsonMarkerOptions);
                    },
                    onEachFeature: onEachFeature
                });
                layer.addTo(map);
                existingLayer = layer;
            });
            xhr.send();
        }

        if (mapElem.classList.contains("accident-list-map")) {
            map.addEventListener("zoomend", loadData);
            map.addEventListener("moveend", loadData);
            map.addEventListener("load", loadData);
        }
    }
})();