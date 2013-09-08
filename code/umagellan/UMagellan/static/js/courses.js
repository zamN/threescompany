$(function() {
    $('.save-course').click(function(e) {
        var id = $(this).parents('.tab-pane').attr('id');
        var course_name = $('#' + id + ' .name-field').val();
        var course_sec = $('#' + id + ' .section-field').val();

        // Append course to table
        if(course_name.length != 0 && course_sec.length != 0) {
            $(this).parents('.tab-pane').children('table').append(
                '<td>' + course_name + '</td>' +
                '<td>' + course_sec + '</td>' +
                '<td width="10%"><a href="#" class="rem-course">&times;</a></td>'
            );
        }

        // Re-apply remove events
        $('.rem-course').click(function(e) {
            $(this).parents('tr').remove();
        });

        // Prevent default action
        e.preventDefault();
    });

    $('.rem-course').click(function(e) {
        // Remove course from table
        $(this).parents('tr').remove();

        // Prevent default action
        e.preventDefault();
    });
});