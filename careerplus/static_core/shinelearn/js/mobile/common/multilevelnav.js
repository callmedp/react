/*!
 * multilevelnav.js is jQuery plugin that progressively enhances
 *
 * @author Design 
 * @see 
 * 
 */

(function (factory) {
  'use strict';

  if(typeof module === 'object' && typeof module.exports === 'object') {
    factory(require('jquery'), window, document);
  } else {
    factory(jQuery, window, document);
  }
}(function ( $, window, document, undefined ) {
  'use strict';

  $(window).on('load', function(){
    $('#main-sidebar').removeClass('hide');
  })

  var
    /** Used later to scroll page to the top */
    $body = $('html, body'),

    /** Used in debug mode to console out useful warnings */
    consl = window.console,

    /** Plugin default options */
    defaults = {
        level: '.level-control',
        backButton: '.backthis',
        defaultButton: '#sidebar-main-trigger',
        rightButton: '.sidebar-secondary-trigger',
        // countriesButton: '#sidebar-countries-trigger',
        countriesButton : $('.fetch'),
        navClass: 'fixed-nav',
        opacityClass: 'opacity-add',
        menuByClass: '.sb-menu',
        timing: 200, 
        slideLeft: {
            'left': '100%',
            'display': 'none'
        },
    };
    
    $(document).ready(function(){

        $('#main-sidebar').simplerSidebar({
            opener: defaults.defaultButton,
            animation: {
                easing: "easeOutQuint"
            },
            sidebar: {
                align: 'left',
                closingLinks: '.close-sb'
            }
        });

        $('#sidebar-secondary').simplerSidebar({
            opener: defaults.rightButton,
            animation: {
                easing: "easeOutQuint"
            },
            sidebar: {
                align: 'right'
            }
        });

        $('.js_sidebar_filter').simplerSidebar({
            opener: '.js_filters_trigger',
            quitter: ".js_close_filter",
            animation: {
                easing: "easeOutQuint"
            },
            sidebar: {
                align: 'right',
                closingLinks: '.js_close_filter'
            }
        });

        $('div#sidebar-countries').each(function(ele){
            $(this).simplerSidebar({
                opener: "#" + defaults.countriesButton.get(ele).id,
                // opener : defaults.countriesButton,
                animation: {
                    easing: "easeOutQuint"
                },
                sidebar: {
                    align: 'right'
                }
            });
        }
        )

        /* inner level button */ 
        $(defaults.level).on('click', function(e){
            e.preventDefault();
            $(this).next('div').animate({ left: "0" }, {
                duration: defaults.timing,
                start: function(){
                    $(this).css('display', 'block');
                    $(defaults.menuByClass)
                        .addClass(defaults.navClass)
                        .parent()
                        .addClass(defaults.opacityClass);
                }
            });
        });

        /* back button */
        $(defaults.backButton).on('click', function(e){
            e.preventDefault();
            $(this).parent().animate(defaults.slideLeft, {
                duration: defaults.timing,
                done: function(){
                    $(this).css('display', 'none');
                }
            });

            if(parseInt($(this).data('index')) === 0) {
                $(defaults.menuByClass)
                    .removeClass(defaults.navClass)
                    .parent()
                    .removeClass(defaults.opacityClass);
            }               
        });

        $(defaults.defaultButton).on('click', function(){
            $(defaults.level).next('div').css(defaults.slideLeft);
            $(defaults.menuByClass)
                .removeClass(defaults.navClass)
                .parent()
                .removeClass(defaults.opacityClass);
        });


    });

}));