function openCommentBox(article_id, visibility=1) {
    if (article_id){
        $('#total_comment' + article_id).addClass('disabled').removeAttr("onclick");

        var _arguments = article_id;

        if (visibility == 2) {
            _arguments += '&visibility=2';
        }
        else if (visibility == 3){
            _arguments += '&visibility=3';
        }

        $.ajax({
            url: '/article/show-comment-box/?art_id=' + _arguments,
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

function loadMoreComment(article_id,visibility=1) {
    if (article_id){
        $('#comment_load_more' + article_id).addClass('disabled').removeAttr("onclick");
        var formData = $("#loadform" + article_id).serialize();

        var _arguments = '';

        if (visibility == 2) {
            _arguments = '?visibility=2';
        }

        $.ajax({
            url: '/article/load-more-comment/'+_arguments,
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
            window.event.preventDefault();
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
                        alert('Thank you, We are processing your review. This may take sometime, so we appreciate your patience.');
                        
                    },
                    failure: function(response){
                        alert("Something went wrong. Please try again later.");
                    }
                });

            }
            
        }
    }

};

function replySubmit(comment_id, login_status){
    if (comment_id){

        if (login_status == 0){
            $('#login-model').modal('show');
            window.event.preventDefault();
        }
        else if (login_status == 1){
            window.event.preventDefault();
            $('#id_reply' + comment_id).attr({
                'data-parsley-required': 'true',
                'maxlength': 200,
            });
            $('#blog-reply-form' + comment_id).parsley().validate();

            if ($('#blog-reply-form' + comment_id).parsley().isValid()){

                var formdata = $("#blog-reply-form" + comment_id).serialize();
                $.ajax({
                    url: "/ajax/article-comment/",
                    type: 'POST',
                    data:formdata,
                    success: function(response) {
                        $('#blog-reply-form' + comment_id)[0].reset();
                        alert('Thank you, We are processing your review. This may take sometime, so we appreciate your patience.');
                        
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


var showArticleOnScroll = (function(){

    var ajaxCalled = false,
    prev_page = 0,
    ajaxOffSetDistance  = 600,
    urlUpdateOffset = 100,
    defaultUrl = top.window.location.pathname;
    defaultTitle = document.title;

    function onScroll() {
        if($('#id_ajax_article').length < 1){
            return;
        };

        $(window).scroll(function() {
            if ($(window).scrollTop() > $('#id_ajax_article').offset().top - ajaxOffSetDistance) {
               makeAjax();
            };
            
            if($('.cls_ajax_article').length) {
                $('.cls_ajax_article').each(function(index,item){
                    if(isScrolledIntoView(item)) {
                        if(upDateUrl($(item).data('url'),$(item).data('title'))){
                            firePageView($(item).data('title'));
                        }
                        return false;
                    }
                });

                if($(window).scrollTop() + window.innerHeight < $('.cls_ajax_article').first().offset().top) {
                    if(upDateUrl(defaultUrl,defaultTitle)){
                        firePageView(defaultTitle);    
                    }
                };
            };
        });
    };

    function isScrolledIntoView(element) {
        var top_of_element = $(element).offset().top;
        var bottom_of_element = $(element).offset().top + $(element).outerHeight();
        var bottom_of_screen = $(window).scrollTop() + window.innerHeight;
        var top_of_screen = $(window).scrollTop() + 54 /*navbar height */;

        if((bottom_of_screen > top_of_element) && (top_of_screen < bottom_of_element)){
            return true;
        } else {
            return false;
        }
    };

    function firePageView(pageTitle){
        var obj = {};
        obj.pageTitle = pageTitle;
        MyGA.sendVirtualPage(obj);
    };

    function makeAjax() {
        page = $("#pg_id").val();
        slug = $("#pg_slug").val();
        visibility = $("#id_visibility").val();
        if(!ajaxCalled){
            if (page != undefined & page != prev_page){
                prev_page = page;
                data = "?page="+ page+ "&slug=" + slug + "&visibility=" + visibility
                ajaxCalled = true;
                $.ajax({
                    url: "/article/ajax/article-detail-loading/" + data,
                    type: "GET",
                    dataType: "json",
                    success: function(data) {
                        $("#load_more").remove();
                        var dynamicDiv = $('<div/>',{'class' : 'cls_ajax_article','html' : data.article_detail,'data-url':data.url,'data-title':data.title});
                        $('#related-container').append(dynamicDiv);
                        ajaxCalled = false;
                    },
                    failure: function(response){}
                });
            }
        }
    };

    
    function upDateUrl(urlPath, newTitle) {
        var urlPath = urlPath,
        ret = false;
        if(urlPath != '' && top.window.location.pathname != urlPath) {
            window.history.pushState({"html":'',"pageTitle": newTitle},"", urlPath);
            ret = true;
        }
        return ret;
    };

    return {
        scroll : onScroll
    }

})();

function openReplySection(comment_id, medium){
    var val = "#comment_" + comment_id
    $('.reply-section').each(function(){
        if($(this)[0].id === $(val)[0].id){
            $(val).toggle()
        }
        else{
            $(this)[0].style.display = 'none'
        }
    })
    if(medium === '0'){
        if ($(val)[0].style.display != 'none'){
            $('#collapseExample')[0].style.display = "none"
        }
        else{
            $('#collapseExample')[0].style.display = ""
        }
    }
}