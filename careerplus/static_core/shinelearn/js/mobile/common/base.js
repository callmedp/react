
// Products Box Items JS Starts here
$(document).ready(function() { 

	$("#share-btn").click(function() {
	    $("#share-icon").slideToggle("slow");
	});// Slide toggle function ends here


	$('ul.tabs li').click(function(){
		var tab_id = $(this).attr('data-tab');
		console.log(tab_id);
		$('ul.tabs li').removeClass('current');
		$('.tab-content').removeClass('current');

		$(this).addClass('current');
		$("#"+tab_id).addClass('current');
	}); // Tabbing function ends here

	// Header Scroll
	$(window).on('scroll', function() {
		var scroll = $(window).scrollTop();

		if (scroll >= 460) {
			$('#hide-second').addClass('remove-second');
		} else {
			$('#hide-second').removeClass('remove-second');
		}
	});

	$("#search-inupt").click(function() {
	    $("#close").css("display", "table-cell");
	    $("#list").slideToggle("fast");
	});
	

	$(".home-slider").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: false,
		arrows: false,
		infinite: false
	});

	$(".blog-slider").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: false,
		arrows: false,
		infinite: false,
		variableWidth: true,
	});

	$(".skill-provider").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: false,
		arrows: false,
		infinite: false,
		variableWidth: true,
	});

	$(".review-slide").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: true,
		arrows: false,
		// variableWidth: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		infinite: false
	});

	$(".login-slider").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: false,
		arrows: false,
		variableWidth: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		infinite: false
	});

	$(".trending-slide").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: false,
		arrows: false,
		variableWidth: true,
		slidesToShow: 2,
		slidesToScroll: 2,
		infinite: false
	});

	$(".slide-provide").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: false,
		arrows: false,
		slidesToShow: 1,
		slidesToScroll: 1,
		variableWidth: true,
		slideWidth: 240,
		infinite: true
	});

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

});// Document ready function ends here

function goBack() {
	window.history.back();
}// Go back function ends here

document.ontouchmove = function ( event ) {

    var isTouchMoveAllowed = true, target = event.target;

    while ( target !== null ) {
        if ( target.classList && target.classList.contains( 'disable-scrolling' ) ) {
            isTouchMoveAllowed = false;
            break;
        }
        target = target.parentNode;
    }

    if ( !isTouchMoveAllowed ) {
        event.preventDefault();
    }
};


$("#uploadBtn").onchange = function () {
    $("#uploadFile").value = this.value;
};
