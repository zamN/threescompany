$(function() {
    function saveCourse(e) {
        var id = $('.tab-pane.active').attr('id');
        var course_name = $('#' + id + ' .name-field').val();
        var course_sec = $('#' + id + ' .section-field').val();

        // Append course to table
        if(course_name.length != 0 && course_sec.length != 0) {
            $('.tab-pane.active').children('table').append(
                '<tr>' +
                '<td>' + course_name + '</td>' +
                '<td>' + course_sec + '</td>' +
                '<td width="10%"><a href="#" class="rem-course">&times;</a></td>' +
                '</tr>'
            );
        }

        var latestCourseRow = $('.tab-pane.active table tr:last-child');
        window.x = latestCourseRow();
        // Re-apply remove events
        console.log(latestCourseRow.children);
        latestCourseRow.children(".rem-course").click(function(e) {
            latestCourseRow.remove();
        });

        // Prevent default action
        e.preventDefault();
    }
    $(".save-course").click(saveCourse);
    Mousetrap.bind("enter", function(e) {
        if ($(".section-field").is(":focus")) {
            saveCourse.call(this, e);
        }
    });

    $('.rem-course').click(function(e) {
        // Remove course from table
        $(this).parents('tr').remove();

        // Prevent default action
        e.preventDefault();
    });
});
