function openCommentBox(article_id) {
    if (article_id){
        $('#total_comment' + article_id).addClass('disabled').removeAttr("onclick");
        $.ajax({
            url: '/article/show-comment-box/?art_id=' + article_id,
            dataType: 'html',
            success: function(html) {
                var id = '#comment-box' + article_id;
                var total_comment_id = '#total_comment' + article_id;
                $(id).append(html);
                $(total_comment_id).hide();
                
           },
            error: function(xhr, ajaxOptions, thrownError) {
                alert(thrownError + "\r\n" + xhr.statusText + "\r\n" + xhr.responseText);
            }
        });
    }
};

function loadMoreComment(article_id) {
    if (article_id){
        $('#comment_load_more' + article_id).addClass('disabled').removeAttr("onclick");
        var formData = $("#loadform" + article_id).serialize();
        $.ajax({
            url: '/article/load-more-comment/',
            type: "GET",
            data : formData,
            dataType: 'html',
            success: function(html) {
               $("#load_more" + article_id).remove();
               $("#page_comment" + article_id).append(html);

           },
            error: function(xhr, ajaxOptions, thrownError) {
                alert("Can't load more comments.");
            }
        });
    }
};

function commentSubmit(article_id, login_status){
    if (article_id){

        if (login_status == 0){
            $('#login-model').modal('show');
        }
        else if (login_status == 1){
            $('#id_comment' + article_id).attr({
                'data-parsley-required': 'true',
                'maxlength': 200,
            });
            $('#blog-comment-form' + article_id).parsley().validate();

            if ($('#blog-comment-form' + article_id).parsley().isValid()){

                var formdata = $("#blog-comment-form" + article_id).serialize();
                $.ajax({
                    url: "/ajax/article-comment/",
                    type: 'POST',
                    data:formdata,
                    success: function(response) {
                        $('#blog-comment-form' + article_id)[0].reset();
                        alert('Thank you for sharing your opinion, your comment will be posted post moderation.');
                        
                    },
                    failure: function(response){
                        alert("Something went wrong. Please try again later.");
                    }
                });

            }
            
        }
    }

};


$(function(){

    $(document).on('click', '#article_share', function(event) {
            // console.log('click');
            // console.log($(this).attr('page-id'));
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


    $(document).ready(function() {
        var win = $(window);
        let prev_page = 0;

        win.scroll(function() {
            if ( win.scrollTop() >= ($(document).height() - win.height()) * 0.8) {
                page = $("#pg_id").val();
                slug = $("#pg_slug").val();
                if (page != undefined & page != prev_page){
                    prev_page = page;
                    data = "?page="+ page+ "&slug=" + slug;
                    $.ajax({
                        url: "/article/ajax/article-detail-loading/" + data,
                        dataType: "html",
                        success: function(html) {
                            $("#load_more").remove();
                            $('#related-container').append(html);
                            ga('send', 'pageview');
                        },
                        failure: function(response){
                            alert("Something went wrong.")
                        }
                    });
                }
                
            }
        });

        // $(document).on("scroll", function(event) {
        //     var scrollPos = $(document).scrollTop() + 50;
        //     $('.scroll-page').each(function () {
        //         var currLink = $(this);
        //         if (currLink.offset().top <= scrollPos && currLink.offset().top + currLink.outerHeight() > scrollPos) {
        //             MyGA.sendVirtualPage('page path');
        //             history.pushState(null, null, url);
        //         }
        //     });
        // });
    });

});



