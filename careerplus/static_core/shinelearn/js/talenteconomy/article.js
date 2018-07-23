;(function($, Article){
	function init() {

	/*	$('#myCarousel1').carousel({
	        interval: false,
	    });

	 
     $('.carousel[data-type="multi"] .item').each(function(){
        var next = $(this).next();
        if (!next.length) {
          next = $(this).siblings(':first');
        }
        next.children(':first-child').clone().appendTo($(this));

        for (var i=0;i<3;i++) {
          next=next.next();
          if (!next.length) {
            next = $(this).siblings(':first');
          }
          
          next.children(':first-child').clone().appendTo($(this));
        }
      });
*/
	    /*$('.carousel[data-type="multi"] .item').each(function(){
	        var next = $(this).next();
	    
	        if (!next.length) {
	          next = $(this).siblings(':first');
	        }
	    
	        next.children(':first-child').clone().appendTo($(this));

	        for (var i=0;i<3;i++) {
	    
	          next=next.next();
	    
	          if (!next.length) {
	            next = $(this).siblings(':first');
	          }
	          
	         // next.children(':first-child').clone().appendTo($(this));
	        }
	    });
*/
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

    	$(document).on('click', '#load-more-te-tag', function(event) {
	        this.disabled = true;
	        var formData = $("#load-te-tag-form").serialize();
	        $.ajax({
	            url : "/talenteconomy/tags/loadmore-article/",
	            type: "GET",
	            data : formData,
	            dataType: 'html',
	            success: function(html, textStatus, jqXHR)
	            {
	                $("#talent_tag_load_more_id").remove();
	                $("#te-tag-article-container-id").append(html);
	            },
	            error: function (jqXHR, textStatus, errorThrown)
	            {
	                alert("Can't load more");
	            }
	         });   
        });


        $(document).on('click', '#load-more-art', function(event) {
	        this.disabled = true;
	        var formData = $("#load-te-art-form").serialize();
	        $.ajax({
	            url : "/talenteconomy/load-more-article/",
	            type: "GET",
	            data : formData,
	            dataType: 'json',
	            success: function(data, textStatus, jqXHR)
	            {

	                $("#talent_art_load_more").remove();
	                $("#list-container-id").append(data.article_list);
	            },
	            error: function (jqXHR, textStatus, errorThrown)
	            {
	                alert("Can't load more");
	            }
	         });
        });



	}

	Article.init = init;

}($, (window.Article = window.Article || {} )))