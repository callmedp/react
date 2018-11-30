$(document).ready(function() {
    /******************************
        BOTTOM SCROLL TOP BUTTON
     ******************************/
  
    // declare variable
    var scrollTop = $(".scrollTop");
  
    $(window).scroll(function() {
      // declare variable
      var topPos = $(this).scrollTop();
  
      // if user scrolls down - show scroll to top button
      if (topPos > 100) {
        $(scrollTop).css("opacity", "1");
  
      } else {
        $(scrollTop).css("opacity", "0");
      }
  
    }); // scroll END
  
    //Click event to scroll to top
    $(scrollTop).click(function() {
      $('html, body').animate({
        scrollTop: 0
      }, 800);
      return false;
  
    }); // click() scroll top EMD
  
    
  }); // ready() END





(function() {
	'use strict';
	

	// Activate scrollspy to add active class to navbar items on scroll
	$('body').scrollspy({
		target: '#mainNav',
		offset: 54
	});

	// Scroll smoothly on click on learn more button
	$('.btn_outline').click(function(){
		$('html, body').animate({
			scrollTop: $('[name="' + $.attr(this, 'href').substr(1) + '"]').offset().top
		}, 800);
		return false;
	});
	
	
	// Scroll smoothly on click on learn more button
	$('.ch').click(function(){
		
		// Add select calss to li mini menu 
		$(this).addClass('menu-active').siblings().removeClass('menu-active');
		
		$('html, body').animate({
			scrollTop: $('#course-highlights').offset().top - 50
		}, 700);
		return false;
		
	});
	
	
	
	// Scroll smoothly on click on learn more button
	$('.cp').click(function(){
		
		// Add select calss to li mini menu 
		$(this).addClass('menu-active').siblings().removeClass('menu-active');
		
		$('html, body').animate({
			scrollTop: $('#course-preview').offset().top - 50
		}, 800);
		return false;
		
	});
	
	// Scroll smoothly on click on learn more button
	$('.wsa').click(function(){
		
		// Add select calss to li mini menu 
		$(this).addClass('menu-active').siblings().removeClass('menu-active');
		
		$('html, body').animate({
			scrollTop: $('#attend').offset().top - 40
		}, 800);
		return false;
		
	});


	// Scroll smoothly on click on learn more button
	$('.wb').click(function(){
		
		// Add select calss to li mini menu 
		$(this).addClass('menu-active').siblings().removeClass('menu-active');
		
		$('html, body').animate({
			scrollTop: $('#why-buy').offset().top -40
		}, 800);
		return false;
		
	});


	// Scroll smoothly on click on learn more button
	$('.ot').click(function(){
		
		// Add select calss to li mini menu 
		$(this).addClass('menu-active').siblings().removeClass('menu-active');
		
		$('html, body').animate({
			scrollTop: $('#outcomes').offset().top + 100
		}, 800);
		return false;
		
	});

	
	// Scroll smoothly on click on learn more button
	$('.learn_icon').click(function(){
		
		// Add select calss to li mini menu 
		$(this).addClass('select').siblings().removeClass('select');
		
		$('html, body').animate({
			scrollTop: $('#learn').offset().top -100
		}, 800);
		return false;
		
	});
	
	
	
	
	
	// Fixed the mini menu top while scrolling
	var stickyOffset = $('.sticky').offset().top;

	$(window).scroll(function(){
	  var sticky = $('.sticky'),
		  scroll = $(window).scrollTop();
		
	  if (scroll >= stickyOffset) sticky.addClass('fixed');
	  else sticky.removeClass('fixed');
	});
	
	

}());


