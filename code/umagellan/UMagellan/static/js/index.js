window.M = {};

M.map = {};

$(function() {
  M.map = new google.maps.Map(document.getElementById('map'), {
    zoom: 18,
    center: getCoordsBy('name_short', 'MKM'),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  var directionsService = new google.maps.DirectionsService(),
      directionsDisplay = new google.maps.DirectionsRenderer({ map: M.map });

  function displayRoute(classes) {
    var request = {
      origin: classes[0],
      destination: classes[classes.length-1],
      waypoints: classes.slice(1, -1).map(function(c) {
        return { location: c }
      }),
      travelMode: google.maps.DirectionsTravelMode.WALKING
    };
    directionsService.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsDisplay.setDirections(response);
      } else { alert ('Failed to route!'); }
    });
  }

  function getCoordsBy(attrName, attrValue) {
    for (var i=0; i < BUILDINGS.length; i++) {
      if (attrValue === BUILDINGS[i][attrName])
        return new google.maps.LatLng(BUILDINGS[i].y, BUILDINGS[i].x);
    }
    return null;
  }

  // Test data.
  var myClasses = [
    getCoordsBy('name_short', 'SYM'),
    getCoordsBy('name_short', 'MCK'),
    getCoordsBy('name_short', 'SSU'),
    getCoordsBy('name_short', 'WIC'),
    getCoordsBy('name_short', 'ARC'),
    getCoordsBy('name_short', 'MTH')
  ];

  displayRoute(myClasses);

});

