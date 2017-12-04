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

	 	$('.contributor-container .right').click(function() {
		    $contributorSlide.slick('slickNext');
		});

		// Prev slide button
		$('.contributor-container .left').click(function() {
		    $contributorSlide.slick('slickPrev');
		});

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