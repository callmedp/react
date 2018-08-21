
// Products Box Items JS Starts here
$(document).ready(function() { 

	$(window).on('load', function(){
		$('#main-sidebar').removeClass('hide')
	});


	$('ul.tabs li a').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('ul.tabs li a').removeClass('current');
		$('.tab-content').removeClass('current');

		$(this).addClass('current');
		$("#"+tab_id).addClass('current');
	})// Tabbing function ends here


	$(".article-slider").slick({
		autoplay:false,
		arrows: false,
		dots: true
	});

	$(".contributors").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: false,
		arrows: true,
		variableWidth: true,
		slidesToShow: 3,
		slidesToScroll: 1,
		infinite: true
	});

	$(".hr-speaker-slide").slick({
		autoplay:true,
		arrows: true,
		dots: false,
		// infinite: true,
		variableWidth: true,
  		slidesToShow: 3,
  		slidesToScroll: 1
	});

	$('.logo-slide').slick({
		infinite: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		arrows : false,
		autoplay: true,
		autoplaySpeed: 1500,
		variableWidth: true
	});

});// Document ready function ends here 


	  function openPopup(el) {
	     $('.modal').hide();
	     $('#' + el).fadeIn(200);   
	  }

	  function closePopup() {
	      $('.modal').fadeOut(300);
	  }