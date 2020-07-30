 // When the user scrolls down 20px from the top of the document, show the button
 window.onscroll = function() {scrollFunction()};

 function scrollFunction() {
     if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
         document.getElementById("top-page").style.display = "block";
     } else {
         document.getElementById("top-page").style.display = "none";
     }
 }
 // When the user clicks on the button, scroll to the top of the document
 $('#top-page').click(function(){
 $('html,body').animate({
     scrollTop: $("#id_nav").offset().top},'slow');
 });