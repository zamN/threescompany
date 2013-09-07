var map,
    layer;
    lon = -76.9416,
    lat = 38.9857;

$(function(){
  map = new OpenLayers.Map( 'map');
  layer = new OpenLayers.Layer.OSM( "Simple OSM Map");
  map.addLayer(layer);
  map.setCenter(
      new OpenLayers.LonLat(lon, lat).transform(
        new OpenLayers.Projection("EPSG:4326"),
        map.getProjectionObject()
        ), 16
      );
});

