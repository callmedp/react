$(function(){

	$(document).on('click', '#load-more-button-id', function(event) {
		var formData = $('#form-load-more-university-course').serialize();
		this.disabled = true;

        $.ajax({
            url : "/ajax/university-skill-course/loadmore/",
            type: "GET",
            data : formData,
            dataType: 'html',
            success: function(html, textStatus, jqXHR)
            {
                $("#id_load_more_course").remove();
                $("#id-university-course-list").append(html);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert("Can't load more");
                this.disabled = false;
            }
        });
    });

});