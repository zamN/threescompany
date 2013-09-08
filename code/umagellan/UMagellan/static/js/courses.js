Handlebars.registerHelper('ifEq', function(v1, v2, options) {
    if(v1 === v2 || (v1 === null && v2 === 'null')) {
      return options.fn(this);
    }
    return options.inverse(this);
});

$(function() {
    $('.error-field').hide();

    function saveCourse(e) {
        var id = $('.tab-pane.active').attr('id');
        var course_name = $('#' + id + ' .name-field').val();
        var course_sec = $('#' + id + ' .section-field').val();

        $('#' + id + ' .name-field').val('');
        $('#' + id + ' .section-field').val('');

        // Append course to table
        if(course_name.length != 0 && course_sec.length != 0) {
            $.ajax({
                url: '/add_course',
                data: { course: course_name, section: course_sec }
            }).done(function(data) {
                if(data.error == true) {
                    $('#' + id + ' .error-field .alert').html(
                        '<button type="button" class="close" data-dismiss="alert">&times;</button>' + data.error_msg);
                    $('#' + id + ' .error-field').show();
                } else {
                    $.get('/static/templates/course_table_row.mustache', function(source) {
                      addCoursesToHTML(data.courses);
                    });
                    e.preventDefault();
                }
            });
        }
    }

    function addCoursesToHTML(courses) {
        $.get('/static/templates/course_table_row.mustache', function(source) {
            var template = Handlebars.compile(source);
            courses.map(function(course) {
                course.section_days.map(function(day) {
                  $('#'+day+".tab-pane")
                      .children('table')
                      .append(template(course));
                });
            });
            remCourseEvents();
            M.initRoutes();
        });
    }

    function remCourseEvents() {
        var courseRows = $('.tab-pane table tr:not(:first)');
        courseRows.each(function(i, x) {
            $(x).find(".rem-course").click(function(e) {
                $.ajax({
                    url: '/delete_course/' + $(this).attr('course_id')
                }).done(function() {
                  $(".tab-pane table tr."+$(x).attr("data-course")).remove();
                  M.initRoutes()
                });
            });
        });
    }

    // Bind to the button and the enter key.
    $(".save-course").click(saveCourse);
    $(".name-field, .section-field").map(function(i, el) {
        $(el).addClass("mousetrap");
    });
    Mousetrap.bind("enter", function(e) {
        if ($(".name-field, .section-field").is(":focus")) {
            saveCourse(e);
        }
    });

    $.get('/get_courses', function(data, status) {
        if (status === "success")
            addCoursesToHTML(data.courses);
    });

    remCourseEvents();

});

