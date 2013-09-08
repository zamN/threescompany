$(document).ready(function() {
    // Hide login divs
    $('.user-links .logged-in').hide();
    $('.user-links .not-logged-in').hide();

    // Determine if user is logged in
    if($.cookie('umagellan_user') === null) {
        // Show appropriate div
        $('.user-links .not-logged-in').show();
    } else {
        // Show appropriate div
        $('.user-links .logged-in').show();
    }
});