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
        var latLng = new L.LatLng(mapElem.dataset.lat, mapElem.dataset.lon);
        map = L.map(mapElem, {
            layers: [osm]
        });
        map.setView(latLng, 14);
        L.control.layers({
            "OpenStreetMap": osm,
            "Google Streets": googleStreets,
            "Google Satellite": googleSat
        }).addTo(map);
        var marker = L.marker(latLng).addTo(map);
    }
})();