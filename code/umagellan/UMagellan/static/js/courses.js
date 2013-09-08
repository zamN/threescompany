$(document).ready(function() {
    $('.add-course input').keydown(function(e) {
        if(e.which == 13) {
            $('.all-courses ul').append('<li>' + $('.add-course input[name=course_name]').text() + '</li>');
        }
    });
});