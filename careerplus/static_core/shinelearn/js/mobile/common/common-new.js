
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

    $('.scrollTo').click(function(e){
        var height = $('.sticky-header').height() + 10;
        $('html, body').animate({
            scrollTop: $( $(this).attr('href') ).offset().top - height
        }, 500);
    
        e.stopPropagation();
        $(".active").removeClass("active");
        $(this).addClass("active");
        return false;
    });
    
    
    $(window).scroll(function(){
        if ($(this).scrollTop() > 10) {
           $('.sticky-header').addClass('fixed');
        } else {
           $('.sticky-header').removeClass('fixed');
        }
    });
    
})


// Toast function
const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
});


