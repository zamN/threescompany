$(function() {
    $('.error-field').hide();

    function saveCourse(e) {
        var id = $('.tab-pane.active').attr('id');
        var course_name = $('#' + id + ' .name-field').val();
        var course_sec = $('#' + id + ' .section-field').val();

        // Append course to table
        if(course_name.length != 0 && course_sec.length != 0) {
            $.ajax({
                url: '/add_course',
                data: { course: course_name, section: course_sec }
            }).done(function(data) {
                if(data.error == true) {
                    $('#' + id + ' .error-field .alert').html('<button type="button" class="close" data-dismiss="alert">&times;</button>' + data.error_msg);
                    $('#' + id + ' .error-field').show();
                } else {
                    $("#course_template").Chevron("render", {
                        name: course_name,
                        sec: course_sec
                    }, function(result) {
                        $('.tab-pane.active')
                        .children('table')
                        .append(result);
                    });

                    remCourseEvents();
                    // Prevent default action
                    e.preventDefault();
                }
            });
        }
    }

    function remCourseEvents() {
        var courseRows = $('.tab-pane table tr:not(:first)');
        courseRows.each(function(i, x) {
            $(x).find(".rem-course").click(function(e) {
                $.ajax({
                    url: '/delete_course/' + $(this).attr('course_id')
                }).done(function() { $(x).remove(); });
            });
        });
    }

    // Bind to the button and the enter key.
    $(".save-course").click(saveCourse);
    Mousetrap.bind("enter", function(e) {
        if ($(".section-field").is(":focus"))
        saveCourse(e);
    });

    remCourseEvents();

});

