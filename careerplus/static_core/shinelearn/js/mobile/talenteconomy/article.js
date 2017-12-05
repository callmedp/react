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

	$(document).on('click', '.js_redirect', function(event) {
		event.preventDefault();
        window.location.href = window.MOBILE_LOGIN_URL + "?next="+window.location.pathname;
    });

	}

	Article.init = init;

}($, (window.Article = window.Article || {} )))