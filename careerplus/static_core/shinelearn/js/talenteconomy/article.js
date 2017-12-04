;(function($, Article){
	function init() {
   
	 	var $contributorSlide =  $('.contributor-slide .item').slick({
		  slidesToShow: 3,
		  slidesToScroll: 1,
		  centerPadding: '60px',
		  lazyLoad: 'progressive',
		  variableWidth: true,
		  infinite: false,
		  arrows: false
		});

	/*	$('#myCarousel1').carousel({
	        interval: false,
	    });

	    $('.carousel[data-type="multi"] .item').each(function(){
	 
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
	}

	Article.init = init;

}($, (window.Article = window.Article || {} )))