
$(document).ready(()=>{
    $(".main-banner__slider").slick({
		autoplay:false,
		arrows: false,
		dots: false,
		variableWidth: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		infinite: true
	});

	$(".popular-courses__slides").slick({
		autoplay:false,
		arrows: false,
		dots: false,
		variableWidth: true,
		slidesToShow: 2,
		slidesToScroll: 1,
		infinite: true
	});

	$(".learner-stories__slider").slick({
		autoplay:false,
		arrows: false,
		dots: false,
		variableWidth: true,
		slidesToShow: 2,
		slidesToScroll: 1,
		infinite: true
    });

    
    
})


// Toast function
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
});


