var map;

// Init map.
function initialize() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 18,
    center: findBuildingCoordsBy('name_short', 'MKM'),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  var directionsService = new google.maps.DirectionsService();
  var directionsDisplay = new google.maps.DirectionsRenderer({ map: map });

  var request = {
    origin:      findBuildingCoordsBy('name_short', 'SYM'),
    destination: findBuildingCoordsBy('name_short', 'MCK'),
    waypoints: [
      {location: findBuildingCoordsBy('name_short', 'SSU')},
      {location: findBuildingCoordsBy('name_short', 'WIC')},
      {location: findBuildingCoordsBy('name_short', 'ARC')},
      {location: findBuildingCoordsBy('name_short', 'MTH')}
    ],
    travelMode: google.maps.DirectionsTravelMode.WALKING
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
    } else { alert ('Failed to route!'); }
  });
}

function findBuildingCoordsBy(attrName, attrValue) {
  for (var i=0; i < BUILDINGS.length; i++) {
    if (attrValue === BUILDINGS[i][attrName])
      return new google.maps.LatLng(BUILDINGS[i].y, BUILDINGS[i].x);
  }
  return null;
}

// Run the `initialize` function.
google.maps.event.addDomListener(window, 'load', initialize);

