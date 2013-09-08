window.M = {};

M.map = {};

$(function() {
  M.map = new google.maps.Map(document.getElementById('map'), {
    zoom: 18,
    center: getCoordsBy('name_short', 'MKM'),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  $('#map').height($(window).height() - 85);

  var directionsService = new google.maps.DirectionsService(),
      directionsDisplay = new google.maps.DirectionsRenderer({ map: M.map });

  function displayRoute(courses) {
    var request = {
      origin: courses[0],
      destination: courses[courses.length-1],
      waypoints: courses.slice(1, -1).map(function(c) {
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

  M.initRoutes = function(paneID) {
      if (paneID === null || paneID === undefined)
          paneID = $(".tab-pane.active").attr("id");
      var courses = [];
      $("#"+paneID+".tab-pane .course-row").each(function(i, course) {
          courses.push(
              getCoordsBy("name_short", $(course).attr("data-build_code"))
          );
      });

      // Clear the map
      directionsDisplay.set("directions", null);
      // If there are two or more courses, display their routes.
      if (courses.length >= 2)
          displayRoute(courses);
      // Otherewise, reset the map to Mckeldin Mall.
      else
          M.map.panTo(getCoordsBy('name_short', 'MKM'));
  }

  $(".nav-tabs a").mouseup(function() {
      M.initRoutes($(this).attr("href").slice(1));
  });

  var user_curr_home = $('.user_curr_home').val();
  $.each(BUILDINGS, function(i, b) {
    if(b.name_short.length != 0) {
      if(b.name_short == user_curr_home) {
        $('.homes').append('<option value="' + b.name_short + '" selected>' + b.name_long + '</option>');
      } else {
        $('.homes').append('<option value="' + b.name_short + '">' + b.name_long + '</option>');
      }
    }
  });

});

