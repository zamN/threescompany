$(document).ready(function() {
    // Hide login divs
    $('.user-links .logged-in').hide();
    $('.user-links .not-logged-in').hide();

    // Determine if user is logged in
    if($.cookie('umagellan_user') === null) {
        // Show appropriate div
        $('.user-links .not-logged-in').show();
    } else {
        // Capture user from cookie
        var umagellan_user = $.cookie('umagellan_user');

        // Add user name to navbar
        $('.umagellan-user-name').text(umagellan_user);

        // Show appropriate div
        $('.user-links .logged-in').show();
    }
});