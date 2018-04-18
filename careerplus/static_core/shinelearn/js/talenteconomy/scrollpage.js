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
            var bottom = $(document).height() - $(window).height();
            if (position == bottom) {
               makeAjax();
            };
         });
    };

    function makeAjax() {
        page = $("#talentpg_id").val();
        slug = $("#talentpg_slug").val();
        if(!ajaxCalled){
            if (page != undefined & page != prev_page){
                prev_page = page;
                data = "?page="+ page+ "&slug=" + slug;
                ajaxCalled = true;
                $.ajax({
                    url: "/talenteconomy/ajax/talent-detail-loading/" + data,
                    type: "GET",
                    dataType: "json",
                    success: function(data) {
                        $("#talent_load_more").remove();
                        // var dynamicDiv = $('<div/>',{'class' : 'cls_ajax_article','html' : data.article_detail,'data-url':data.url,'data-title':data.title});
                        $('#related-talent-container').append(data.article_detail);
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
