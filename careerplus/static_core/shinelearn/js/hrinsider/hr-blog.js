$(function(){

    $(document).on('click', '#load-hr-tag-article', function(event) {
        this.disabled = true;
        var formData = $("#load-hr-tag-form").serialize();
        $.ajax({
            url : "/hr-insider/tags/loadmore-article/",
            type: "GET",
            data : formData,
            dataType: 'html',
            success: function(html, textStatus, jqXHR)
            {
                $("#hrblog_tag_load_more_id").remove();
                $("#hr-tag-article-container").append(html);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert("Can't load more");
            }
        });   
    });

    $(document).on('click', '#load-hr-article-list', function(event) {
        this.disabled = true;
        var formData = $("#load-hr_article-list-form").serialize();
        $.ajax({
            url : "/hr-insider/article/loadmore-article/",
            type: "GET",
            data : formData,
            dataType: 'html',
            success: function(html, textStatus, jqXHR)
            {
                $("#hr_article_load_more_id").remove();
                $("#hr-listing-container").append(html);
            },
            error: function (jqXHR, textStatus, errorThrown)
            {
                alert("Can't load more");
            }
        });   
    });
    
});