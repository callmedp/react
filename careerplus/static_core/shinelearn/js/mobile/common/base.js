
// Products Box Items JS Starts here
$(document).ready(function() { 

// Trending articles JS Starts here
$('.trending').bxSlider({
	slideWidth: 220,
    minSlides: 1,
    maxSlides: 2,
    moveSlides: 1,
    slideMargin: 15,
	pager: false,
	controls: false,
	infiniteLoop: false
	
});// end of Trending articles

// Trending articles JS Starts here
$('.related').bxSlider({
	slideWidth: 290,
    minSlides: 1,
    maxSlides: 2,
    moveSlides: 1,
    slideMargin: 15,
	pager: false,
	controls: false,
	infiniteLoop: false
	
});// end of Trending articles

// skill provider JS Starts here
$('.skill-provider').bxSlider({
	slideWidth: 180,
    minSlides: 1,
    maxSlides: 2,
    moveSlides: 1,
    slideMargin: 0,
	pager: false,
	controls: false,
	infiniteLoop: false
	
});// end of skill provider

// skill provider JS Starts here
$('.review-slide').bxSlider({
	pager: false,
	controls: false,
	infiniteLoop: false
});// end of skill provider

$("#share-btn").click(function() {
    $("#share-icon").slideToggle("slow");
});


	$('ul.tabs li a').click(function(){
		var tab_id = $(this).attr('data-tab');

		$('ul.tabs li a').removeClass('current');
		$('.tab-content').removeClass('current');

		$(this).addClass('current');
		$("#"+tab_id).addClass('current');
	})// Tabbing function ends here

});// Document ready function ends here 



function goBack() {
    window.history.back();
}


// Gallery Slider Starts here
$('.gallery').bxSlider({
    pager: false,
    infiniteLoop: false,
    hideControlOnEnd: true,
    controls: true
});
// Gallery Slider Ends here



// Other related colleges JS Starts here
  $('.related_college').bxSlider({
    slideWidth: 280,
    minSlides: 1,
    maxSlides: 3,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: false,
	hideControlOnEnd: true,
	infiniteLoop: false
  });
// Other related colleges JS Starts here

// Other related colleges JS Starts here
  $('.review-wrap').bxSlider({
    slideWidth: 250,
    minSlides: 1,
    maxSlides: 2,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: false,
	hideControlOnEnd: true,
	infiniteLoop: false
  });
// Other related colleges JS Starts here


// listed colleges JS Starts here
  $('.listed_college_slider').bxSlider({
    slideWidth: 273,
    minSlides: 1,
    maxSlides: 3,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: false,
	infiniteLoop: false
  });
// Other related colleges JS Starts here



// Other related colleges JS Starts here
  $('.leaderboard').bxSlider({
    slideWidth:140,
    minSlides: 1,
    maxSlides: 3,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: false,
	infiniteLoop: false
  });
// Other related colleges JS Starts here


// LeaderBoard JS Starts here
  $('.leaderboard-slide').bxSlider({
    slideWidth:210,
    minSlides: 1,
    maxSlides: 3,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: false,
	infiniteLoop: false
  });
// LeaderBoard JS Starts here

// featured college JS Starts here
//   $('.feautred-college ul').bxSlider({
//     minSlides: 1,
//     maxSlides: 1,
//     moveSlides: 1,
//     slideMargin: 10,
// 	pager: false,
// 	controls: false,
// 	infiniteLoop: false,
// 	hideControlOnEnd: true
//   });
// featured college JS Starts here
// exam-list JS Starts here

  $('.exam-list ul').bxSlider({
    minSlides: 1,
    maxSlides: 1,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: true,
	infiniteLoop: false,
	hideControlOnEnd: true
  });
// exam-list JS Starts here

  $('.authors-list ul').bxSlider({
    slideWidth:166,
    minSlides: 1,
    maxSlides: 2,
    moveSlides: 2,
    slideMargin: 10,
	pager: false,
	controls: true,
	infiniteLoop: false,
	hideControlOnEnd: true
  });
// exam-list JS Starts here


  $('.recommended-article ul').bxSlider({
    slideWidth:260,
    minSlides: 1,
    maxSlides: 2,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: true,
	infiniteLoop: false,
	hideControlOnEnd: true
  });
// recommended-article JS Ends here

// latest_questions JS Starts here
  $('.latest_questions').bxSlider({
    //slideWidth:260,
    minSlides: 1,
    maxSlides: 1,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: true,
	infiniteLoop: false,
	hideControlOnEnd: true
  });
// latest_questions JS Starts here

// partner-bank JS Starts here
  $('.partner-bank').bxSlider({
    //slideWidth:260,
    minSlides: 1,
    maxSlides: 1,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: true,
	infiniteLoop: false,
	hideControlOnEnd: true
  });
// partner-bank JS Starts here

$('.review-slide').bxSlider({
	pager: false,
	infiniteLoop: false,
	hideControlOnEnd: true,
	controls: true,
	minSlides: 1,
	maxSlides: 1,
	slideMargin: 10
});

// Important dates Slider Starts here
    $('.entrance-exam').bxSlider({
        slideWidth: 200,
        minSlides: 3,
        maxSlides: 2,
        moveSlides: 1,
        slideMargin: 0,
        pager: false,
        infiniteLoop: false,
        hideControlOnEnd: true,
        controls: false
    });
    // Important dates Slider Ends here

// Other related colleges JS Starts here
  $('.college-review-box').bxSlider({
    slideWidth: 260,
    minSlides: 1,
    maxSlides: 2,
    moveSlides: 1,
    slideMargin: 10,
	pager: false,
	controls: false,
	hideControlOnEnd: true,
	infiniteLoop: false
  });
// Other related colleges JS Starts here

$('.testi').bxSlider({
	controls: false
	
});// Products Box Items JS Starts here

$('.cat-testimonials').bxSlider({
	controls: false
	
});// CAT Testimonals JS Starts here

$('.dates').bxSlider({
	controls: true,
	pager: false
	
});// CAT Testimonals JS Starts here

$(document).ready(function() {
	// Header Scroll
	$(window).on('scroll', function() {
		var scroll = $(window).scrollTop();

		if (scroll >= 220) {
			//$('#navbar').addClass('nav-fixed');
			$('#detail-nav').addClass('paddingTop-65');
		} else {
			//$('#navbar').removeClass('nav-fixed');
			$('#detail-nav').removeClass('paddingTop-65');
		}
	});

});


$(document).ready(function() {
	// Header Scroll
	$(window).on('scroll', function() {
		var scroll = $(window).scrollTop();

		if (scroll >= 50) {
			$('#hide-second').addClass('remove-second');
		} else {
			$('#hide-second').removeClass('remove-second');
		}
	});

});


// New Ticker Satrts here 	
// $(window).load(function(e) {
// 	try {
// 		$("#bn4").breakingNews({
// 			effect		:"slide-v",
// 			autoplay	:true,
// 			timer		:3000,
// 		});
// 	} catch(e) {
// 		console.log(e);
// 	}
// });// New Ticker Ends here 	

// Notification open and close Starts here  
$('#theNotif').click(function() { return false; });
	$('#notifikasi').click(function(){
		$('#theNotif, .aro').fadeIn('fast', function() {
			$(document).one('click', function(e) {
				$('#theNotif, .aro').fadeOut('fast');
			});
		});
});// Notification open and close Ends here


// Notification open and close Starts here 

$(".related_list").click(function() { return false; });
	$('#related').click(function(){
		$(".related_list").fadeIn('fast', function() {
			$(document).one('click', function(e) {
				$(".related_list").fadeOut('fast');
			});
		});
});// Notification open and close Ends here



// Close through cross buttn Starts here
$(function() {
    $('.close').click(function() {
        $('#theNotif, .aro').hide();
        return false;
    });
});// Close through cross buttn Ends here

// Refine search open and close Starts here  
$('#refine_cont').click(function() { return false; });
	$('#refine').click(function(){
		$('#refine_cont').fadeIn('fast', function() {
			$(document).one('click', function(e) {
				$('#refine_cont').fadeOut('fast');
			});
		});
});// Refine search open and close Ends here


// Close through cross buttn Starts here
$(function() {
    $('#close').click(function() {
        $('#refine_cont').hide();
        return false;
    });
});// Close through cross buttn Ends here

// Refine search open and close Starts here  
$('.other').click(function() { return false; });
	$('.twenty').click(function(){
		$('.other').fadeIn('fast', function() {
			$(document).one('click', function(e) {
				$('.other').fadeOut('fast');
			});
		});
});// Refine search open and close Ends here



	
	$(".setting-list").hide();
	$(".setting-content").click(function(e){
    	$(this).toggleClass("set-active");
		$(this).next("ul").toggle();
		e.stopPropagation();
		//$(".setting-list").toggle();
	});
	
	$(document).click(function(){
		$(".setting-list").hide();
		$(".setting-content").removeClass("set-active");
	});
		
		
// Notification open and close Starts here  
$('.exam_items').click(function() { return false; });
	$('.exam_dot').click(function(){
		$('.exam_items').fadeIn('fast', function() {
		$('.exam_dot').addClass('active')
			$(document).one('click', function(e) {
				$('.exam_items').fadeOut('fast');
				$('.exam_dot').removeClass('active')
			});
		});
});// Notification open and close Ends here

	


$("body").on('click', function(e) {
		if($(e.target).attr("id") == "call_icon" || $(e.target).attr("id") == "call_icon"){
			$('#'+$(e.target).data("open")).slideDown('fast');}
		else{
			$('#call_icon, #call_icon, #call_icon, #call_icon, #share').each(function(){
					$('#'+$(this).data("open")).slideUp('fast');
				});
		}
});


// QNQ Detail Share icon open and close Starts here  
$('#container1').click(function() { return false; });
	$('.share_icon').click(function(){
		$('#container1').fadeIn('fast', function() {
			$('.share_icon').addClass('active')
			$(document).one('click', function(e) {
				$('#container1').fadeOut('fast');
				$('.share_icon').removeClass('active')
			});
		});
});// NQ Detail Share icon open and close Ends here


//// College listing More links in dotted icon open and close Starts here  
//$('.more_link_list').click(function() { return false; });
//	$('.more_links').click(function(){
//		$('.more_link_list').fadeIn('fast', function() {
//			$('.more_links').addClass('active')
//			$(document).one('click', function(e) {
//				$('.more_link_list').fadeOut('fast');
//				$('.more_links').removeClass('active')
//			});
//		});
//});// College listing More links in dotted icon open and close Ends here



$(document).ready(function(){

  $('.college_contact').each(function() {
    var $dropdown = $(this);
	var $dropact = $(this);

    $(".more_links, .sort", $dropdown, $dropact).click(function(e) {
      e.preventDefault();
      $(".more_link_list", $dropdown).toggle();
	  $(".more_links, .sort", $dropact).toggleClass("active");
      return false;
    });

});
    
  $('html').click(function(){
    $(".more_link_list").hide();
	$(".more_links, .sort").removeClass("active");
  });
  
  
  function inio2(){
		
		 if(($(".college_navi li:eq(2)").hasClass("select") || $(".college_navi li:eq(3)").hasClass("select"))){
			$(".college_navi").scrollLeft(400);
				
		}else{
			$(".college_navi").scrollLeft(0);
		}

		$(window).resize(inio2);
	}
	inio2();
     
});