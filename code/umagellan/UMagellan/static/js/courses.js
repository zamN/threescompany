$(function() {
    $('.error-field').hide();

    $('.save-course').click(function(e) {
        var id = $(this).parents('.tab-pane').attr('id');
        var course_name = $('#' + id + ' .name-field').val();
        var course_sec = $('#' + id + ' .section-field').val();

        // Add course to DB
        if(course_name.length != 0 && course_sec.length != 0) {
            $.ajax({
                url: '/add_course',
                data: { course: course_name, section: course_sec }
            }).done(function(data) {
                if(data.error == true) {
                    $('#' + id + ' .error-field .alert').html('<button type="button" class="close" data-dismiss="alert">&times;</button>' + data.error_msg);
                    $('#' + id + ' .error-field').show();
                } else {
                    // Append course to table
                    $(this).parents('.tab-pane').children('table').append(
                        '<td>' + course_name + '</td>' +
                        '<td>' + course_sec + '</td>' +
                        '<td width="10%"><a href="#" class="rem-course">&times;</a></td>'
                    );        

                    // Re-apply remove events
                    $('.rem-course').click(function(e) {
                        $(this).parents('tr').remove();

                        // Delete course from DB
                        $.ajax({
                            url: '/delete_course/' + $(this).attr('course_id')
                        });

                        // Delete table (if neccessary)
                        if($('#' + id + ' table tr').length == 1) {
                            $('#' + id + ' table').remove();
                        }

                        // Prevent default action
                        e.preventDefault();
                    });
                }
            });   
        }

        // Prevent default action
        e.preventDefault();
    });

    $('.rem-course').click(function(e) {
        var id = $(this).parents('.tab-pane').attr('id');

        // Remove course from table
        $(this).parents('tr').remove();

        // Delete course from DB
        $.ajax({
            url: '/delete_course/' + $(this).attr('course_id')
        });

        // Delete table (if neccessary)
        if($('#' + id + ' table tr').length == 1) {
            $('#' + id + ' table').remove();
        }

        // Prevent default action
        e.preventDefault();
    });
});