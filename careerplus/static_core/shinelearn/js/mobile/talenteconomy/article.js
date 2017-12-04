;(function($, Article){
	function init() {

		$(".contributors").slick({
			autoplay:true,
			autoplaySpeed:3000,
			dots: false,
			arrows: false,
			variableWidth: true,
			slidesToShow: 2,
			slidesToScroll: 1,
			infinite: true
		});

		$(".article-slider").slick({
			autoplay:false,
			autoplaySpeed:3000,
			dots: false,
			arrows: false,
			variableWidth: true,
			slidesToShow: 2,
			slidesToScroll: 1,
			infinite: true
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