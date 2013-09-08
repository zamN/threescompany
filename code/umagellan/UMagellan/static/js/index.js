window.M = {
    map: {},
    markers: [],
    home: {},
    minZoom: 7,
    maxZoom: 20
};

$(function() {
  $('.success-field').hide();

  M.map = new google.maps.Map(document.getElementById('map'), {
    zoom: 18,
    center: getCoordsBy('name_short', 'MKM'),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  $('#map').height($(window).height() - 85);

  var directionsService = new google.maps.DirectionsService(),
      directionsDisplay = new google.maps.DirectionsRenderer({
        map: M.map,
        suppressMarkers: true
  });

  function setMarkers(points) {
      points.map(function(p, i) {
          var icon = "/static/img/mapMarkers/"
                    +(i+1)
                    +"ABCDEFG"[i]
                    +".png";
          M.markers.push(new google.maps.Marker({
              map: M.map,
              position: p.p,
              icon: icon,
              course: p.course
          }));
          $(p.course).find(".marker-img").html(
            "<img width='12' height='21' src="+icon+" />"
          );
      });
  }

  function resetMap() {
      directionsDisplay.set("directions", null);
      M.markers.map(function(m) {
          m.setMap(null);
      });
      $(".marker-img img").remove();
      M.markers = [];
  }

  function displayRoute(ps) {
    // If two points of the same location exist in a row, move one.
    for (var i=0; (i+1) < ps.length; i++) {
      if ((ps[i].p.ob === ps[i+1].p.ob) &&
          (ps[i].p.cb === ps[i+1].p.cb)) {
        ps[i+1].p.ob += (randomSign()*0.0001);
        ps[i+1].p.cb += (randomSign()*0.0001);
      }
    }
    var request = {
      origin: ps[0].p,
      destination: ps[ps.length-1].p,
      waypoints: ps.slice(1, -1).map(function(c) {
        return { location: c.p }
      }),
      travelMode: google.maps.DirectionsTravelMode.WALKING,
    };
    directionsService.route(request, function(response, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        resetMap();
        directionsDisplay.setDirections(response);
        setMarkers(ps);
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

      // Sort by time.
      var courses$ = $("#"+paneID+".tab-pane .course-row");
      courses$.sort(function(a, b) {
        var aTime = Date.parse('01/01/2011 '+$(a).attr("data-start_time")+':00');
        var bTime = Date.parse('01/01/2011 '+$(b).attr("data-start_time")+':00');
        return aTime > bTime;
      });

      // Get the course coords.
      var points = [];
      if (M.home.val()[0] !== '-') {
          points.push({
            p: getCoordsBy("name_long", $(".homes option:selected").val()),
            course: null
          });
      }
      courses$.each(function(i, course) {
          points.push({
            p: getCoordsBy("name_short", $(course).attr("data-build_code")),
            course: course
          });
      });

      resetMap();
      // If there are two or more courses, display their routes.
      if (points.length >= 2) {
          displayRoute(points);
      // Otherewise, reset the map to Mckeldin Mall.
      } else {
          M.map.setZoom(16);
          M.map.panTo(getCoordsBy('name_short', 'MKM'));
      }
  }

  $(".nav-tabs a:not(:last)").mouseup(function() {
      M.initRoutes($(this).attr("href").slice(1));
  });

  M.home = $('.user_curr_home');
  $('.homes').append('<option>------------</option>');
  $.each(BUILDINGS, function(i, b) {
      if(b.name_long == M.home.val()) {
        $('.homes').append('<option selected>' + b.name_long + '</option>');
      } else {
        $('.homes').append('<option>' + b.name_long + '</option>');
      }
  });

  $("#user_home input[type=submit]").click(function(e) {
      e.preventDefault();

      $.ajax({
            type: 'POST',
            url: '/user/sethome/',
            data: $('#user_home').serialize(),
            success: function () {
                $('.success-field').show();
                M.home.val($(".homes option:selected").val());
                $(".user-home-loc").text(M.home.val());
                if (M.home.val()[0] !== '-') {
                  $(".starting-from").show();
                } else {
                  $(".starting-from").hide();
                }
            }
        })
  });

});

function randomSign() {
  return (Math.random() > 0.5) ? 1 : -1;
}

