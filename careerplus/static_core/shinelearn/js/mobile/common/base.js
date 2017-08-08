
// Products Box Items JS Starts here
$(document).ready(function() { 

	$("#share-btn").click(function() {
	    $("#share-icon").slideToggle("slow");
	});// Slide toggle function ends here


	$('ul.tabs li a').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('ul.tabs li a').removeClass('current');
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
		variableWidth: true,
		infinite: false
	});

	$(".review-slide").slick({
		autoplay:false,
		autoplaySpeed:3000,
		dots: true,
		arrows: false,
		variableWidth: true,
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
		slidesToShow: 1,
		slidesToScroll: 1,
		infinite: false
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

