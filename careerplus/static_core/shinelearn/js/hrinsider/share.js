$(function(){

    $(document).on('click', '#article_share', function(event) {
            console.log('click');
            // console.log($(this).attr('page-id'));
            console.log($(this).attr('article-slug'));
            $.ajax({
                url: "/ajax/article-share/",
                type: 'GET',
                data: {
                  article_slug: $(this).attr('article-slug'),
                },
                success: function(data) {
                    console.log('success');
                }
            });
    });
});