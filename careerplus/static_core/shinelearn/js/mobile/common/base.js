
// Products Box Items JS Starts here
$(document).ready(function() { 
	var showChar = 280 ;  // How many characters are shown by default
	var ellipsestext = "..." ;
	var moretext = " Read more" ;
	var lesstext = " Read less" ;

	function showMoreLess(){
	  // Configure/customize these variables.

	  $('.more1 p').each(function() {
	    var content = $(this).html();

	    if(content.length > showChar) {
	        var c = content.substr(0, showChar);
	        var h = content.substr(showChar, content.length - showChar);
	        var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span style="display: none;">' + h + '</span>&nbsp;&nbsp;<a href="#" class="morelink1" style="display:inline-block;">' + moretext + '</a></span>';


	        $(this).html(html);
	    }

	  });

	};
	showMoreLess();
    $(".morelink1").click(function(){
      if($(this).hasClass("less")) {
          $(this).removeClass("less");
          $(this).html(moretext);
      } else {
          $(this).addClass("less");
          $(this).html(lesstext);
      }
      $(this).parent().prev().toggle();
      $(this).prev().toggle();
      return false;
    });


	$("#share-btn").click(function() {
	    $("#share-icon").slideToggle("slow");
	});// Slide toggle function ends here


	$('ul.tabs li').click(function(){
		var tab_id = $(this).attr('data-tab');
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

		if (scroll >= 900) {
			$('#enrollNow').addClass('stick-enroll');
		} else {
			$('#enrollNow').removeClass('stick-enroll');
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
		dots: false,
		variableWidth: true,
		slidesToShow: 2,
		slidesToScroll: 1,
		infinite: true
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

	// Executive course Function starts here 
	$(".faculty-profile").slick({
		autoplay:false,
		arrows: true,
		dots: false,
		// variableWidth: true,
		slidesToShow: 1,
		slidesToScroll: 1,
		infinite: false
	});


	$(".youMayLike-slider").slick({
		autoplay:false,
		arrows: false,
		dots: true,
		infinite: true,
		variableWidth: true,
  		slidesToShow: 2,
  		slidesToScroll: 1
	});
	
	$(".info-slider").slick({
		autoplay:true,
		arrows: false,
		dots: false,
		infinite: true
	});

	$("#close-offer").click(function(){
		$("#offer-widget").hide();
	});

	
	$("#enroll-now").click(function(){
		$("#open-offer").addClass('show');
	});

	$("#icon_offer").click(function(){
		$("#open-offer").addClass('show');
	});
	
	$("#close-offer-modal").click(function(){
		$("#open-offer").removeClass('show');
	});

	$("#open-thanks").click(function(){
		$("#thank-modal").addClass('show');
	});

	$("#close-thanks-modal").click(function(){
		$("#thank-modal , #open-offer").removeClass('show');
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



$('.btn-openPopup, .custom-modal').each(function (idx) {
	var winnerId = "popup-" + idx;
	this.id = winnerId;
	var btn = $("#popup-" + idx);
	var closeBtn = $(".close-popup");
	var popId = $('#win-'+ idx);
	btn.click(function(e) {
		e.preventDefault();
		$(popId).addClass('block');
	}); 
	closeBtn.click(function() {
		$(popId).removeClass('block');
	});
});

$(document).ready(function(){
	var submitIcon = $('.searchbox-icon');
	var inputBox = $('.searchbox-input');
	var searchBox = $('.searchbox');
	var isOpen = false;
	submitIcon.click(function(){
		if(isOpen == false){
			searchBox.addClass('searchbox-open');
			inputBox.focus();
			isOpen = true;
		} else {
			searchBox.removeClass('searchbox-open');
			inputBox.focusout();
			isOpen = false;
		}
	});

 	submitIcon.mouseup(function(){
		return false;
	});

 	searchBox.mouseup(function(){
		return false;
	});

 	$(document).mouseup(function(){
		if(isOpen == true){
			$('.searchbox-icon').css('display','block');
			submitIcon.click();
		}
	});
});

 	function buttonUp(){
		var inputVal = $('.searchbox-input').val();
		inputVal = $.trim(inputVal).length;
		if( inputVal !== 0){
			$('.searchbox-icon').css('display','none');
		} else {
			$('.searchbox-input').val('');
			$('.searchbox-icon').css('display','block');
		}
	}


