var showTalentpageOnScroll = (function(){
    var ajaxCalled = false,
    prev_page = 0,
    ajaxOffSetDistance  = 600,
    urlUpdateOffset = 100,
    defaultUrl = top.window.location.pathname;
    defaultTitle = document.title;

    function onScroll() {
        if($('#id_ajax_talentpage').length < 1){
            return;
        };



        $(window).scroll(function() {
            var position = $(window).scrollTop();
            if (window.CURRENT_FLAVOUR == 'mobile'){
                var bottom = ($(document).height() - $(window).height())*0.8;
            }
            else{
                var bottom = ($(document).height() - $(window).height())*0.8;
            }
            
            if (position >= bottom) {
               makeAjax();
            };
        });
    };

    function makeAjax() {
        page = $("#te_cat_pg_id").val();
        slug = $("#te_cat_slug").val();
        if(!ajaxCalled){
            if (page != undefined & page != prev_page){
                prev_page = page;
                data = "?page="+ page+ "&slug=" + slug;
                ajaxCalled = true;
                $.ajax({
                    url: "/talenteconomy/ajax/te-category-article-load/" + data,
                    type: "GET",
                    dataType: "json",
                    success: function(data) {
                        $("#talent_cat_load_more").remove();
                        $('#related-talent-container').append(data.article_list);
                        ajaxCalled = false;
                    },
                    failure: function(response){}
                });
            }
        }
    };

    return {
        scroll : onScroll
    }

})();
