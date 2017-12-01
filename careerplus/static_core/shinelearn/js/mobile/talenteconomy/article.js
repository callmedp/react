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

	}

	Article.init = init;

}($, (window.Article = window.Article || {} )))