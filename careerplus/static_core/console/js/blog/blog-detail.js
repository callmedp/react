function openCommentBox(article_id) {
    if (article_id){
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


// $(document).on('click', '#comment-submit', function(event) {
//     event.preventDefault();
//     var login_status = $(this).attr('login-status')
//     if (login_status == 0){
//         $('#login-model').modal('show');
//     }
//     else if (login_status == 1){
//         $('#id_comment').attr({
//             'data-parsley-required': 'true',
//             'maxlength': 200,
//         });
//         $('#blog-comment-form').parsley().validate();
//         var formdata = $("#blog-comment-form").serialize();
//         $.ajax({
//             url: "/ajax/article-comment/",
//             type: 'POST',
//             data:formdata,
//             success: function(response) {
//                 alert('Thank you for sharing your opinion, your comment will be posted post moderation.');
//                 $('#blog-comment-form')[0].reset();
//             },
//             failure: function(response){
//                 alert("Something went wrong. Please try again later.");
//             }
//         });

//     }

// });



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
                    },
                    failure: function(response){
                        alert("Something went wrong.")
                    }
                });
            }
            
        }
    });
});

});



