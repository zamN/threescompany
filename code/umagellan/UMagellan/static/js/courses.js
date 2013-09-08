$(document).ready(function() {
    $('.save-course').click(function() {
        var course_name = $('input[name=course_name]').val();
        var course_sec = $('input[name=course_sec]').val();

        if(course_name.length != 0 && course_sec.length != 0) {
            $('.courses-list').append('<li>' + course_name + ' (' + course_sec + ') <a href="#" class="pull-right del-course">&times;</a></li>');
            $('.del-course').click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('.del-course').click(function() {
        $(this).parent().remove();
    });
});