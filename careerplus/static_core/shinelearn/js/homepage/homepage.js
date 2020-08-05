$(document).ready(function(){

     $('#myCarousel1').carousel({
            interval: 4000,
        });

        $('#carousel-example-generic1').carousel({
            interval: 100000
        })


        jQuery.ajaxPrefilter( function( s ) {
    if ( s.crossDomain ) {
        s.contents.script = false;
    }
} );

})