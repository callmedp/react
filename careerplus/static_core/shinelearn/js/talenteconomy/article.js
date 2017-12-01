;(function($, Article){
	function init() {

		$('#myCarousel1').carousel({
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
	          
	         // next.children(':first-child').clone().appendTo($(this));
	        }
	    });
	}

	Article.init = init;

}($, (window.Article = window.Article || {} )))